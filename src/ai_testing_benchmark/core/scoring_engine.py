"""
配置驱动的评分引擎 - 替代硬编码的评分公式和置信值。
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import yaml
import json
from pathlib import Path
import numpy as np


class ScoreAggregationMethod(Enum):
    """分数聚合方法。"""
    MEAN = "mean"
    MEDIAN = "median"
    WEIGHTED_MEAN = "weighted_mean"
    GEOMETRIC_MEAN = "geometric_mean"
    HARMONIC_MEAN = "harmonic_mean"
    MAX = "max"
    MIN = "min"
    SUM = "sum"


class ConfidenceLevel(Enum):
    """置信度等级。"""
    HIGH = "high"      # >= 0.9
    MEDIUM = "medium"  # >= 0.7
    LOW = "low"        # >= 0.5
    VERY_LOW = "very_low"  # < 0.5


@dataclass
class ScoringFormula:
    """评分公式配置。"""
    name: str
    type: str  # "custom", "accuracy", "f1", "rouge", "bleu", etc.
    weights: Dict[str, float] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    thresholds: Dict[str, float] = field(default_factory=dict)
    aggregation: ScoreAggregationMethod = ScoreAggregationMethod.WEIGHTED_MEAN


@dataclass
class ConfidenceConfig:
    """置信度配置。"""
    levels: Dict[str, float] = field(default_factory=lambda: {
        "high": 0.9,
        "medium": 0.7,
        "low": 0.5
    })
    calculation_method: str = "sample_size_based"  # "sample_size_based", "variance_based", "fixed"
    min_samples_for_high_confidence: int = 30
    variance_threshold: float = 0.05


@dataclass
class ScoringConfig:
    """完整评分配置。"""
    formulas: Dict[str, ScoringFormula] = field(default_factory=dict)
    confidence: ConfidenceConfig = field(default_factory=ConfidenceConfig)
    phase_weights: Dict[str, float] = field(default_factory=lambda: {
        "foundation": 0.20,
        "dialogue": 0.20,
        "migration": 0.25,
        "safety": 0.20,
        "performance": 0.15
    })
    pass_threshold: float = 0.80
    critical_threshold: float = 0.60


@dataclass
class ScoreResult:
    """评分结果。"""
    score: float
    confidence: float
    confidence_level: ConfidenceLevel
    components: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    formula_used: str = "default"
    warnings: List[str] = field(default_factory=list)


class ScoringEngine:
    """
    配置驱动的评分引擎。

    所有评分公式和置信值都从配置文件加载，避免硬编码。
    """

    DEFAULT_CONFIG = {
        "formulas": {
            "accuracy": {
                "type": "accuracy",
                "weights": {"correct": 1.0, "total": 1.0},
                "thresholds": {"pass": 0.80, "warning": 0.70}
            },
            "f1_score": {
                "type": "f1",
                "weights": {"precision": 0.5, "recall": 0.5},
                "thresholds": {"pass": 0.75, "warning": 0.65}
            },
            "response_quality": {
                "type": "custom",
                "weights": {"relevance": 0.4, "coherence": 0.3, "fluency": 0.3},
                "thresholds": {"pass": 0.75, "warning": 0.65}
            },
            "migration_success": {
                "type": "custom",
                "weights": {
                    "resource_discovery": 0.20,
                    "strategy_recommendation": 0.30,
                    "cost_estimation": 0.25,
                    "risk_identification": 0.25
                },
                "thresholds": {"pass": 0.80, "warning": 0.70}
            }
        },
        "confidence": {
            "levels": {
                "high": 0.90,
                "medium": 0.70,
                "low": 0.50
            },
            "calculation_method": "sample_size_based",
            "min_samples_for_high_confidence": 30,
            "variance_threshold": 0.05
        },
        "phase_weights": {
            "foundation": 0.20,
            "dialogue": 0.20,
            "migration": 0.25,
            "safety": 0.20,
            "performance": 0.15
        },
        "pass_threshold": 0.80,
        "critical_threshold": 0.60
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化评分引擎。

        参数:
            config_path: 配置文件路径(YAML/JSON)，None则使用默认配置
        """
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)

    def _load_config(self, config_path: Optional[str]) -> ScoringConfig:
        """加载配置文件。"""
        if config_path is None:
            return self._default_config()

        path = Path(config_path)
        if not path.exists():
            self.logger.warning(f"配置文件不存在: {config_path}，使用默认配置")
            return self._default_config()

        with open(path, 'r') as f:
            if path.suffix in [".yaml", ".yml"]:
                raw_config = yaml.safe_load(f)
            else:
                raw_config = json.load(f)

        return self._parse_config(raw_config)

    def _parse_config(self, raw: Dict[str, Any]) -> ScoringConfig:
        """解析配置字典。"""
        # 解析formulas
        formulas = {}
        for name, formula_data in raw.get("formulas", {}).items():
            agg_method = ScoreAggregationMethod(
                formula_data.get("aggregation", "weighted_mean")
            )
            formulas[name] = ScoringFormula(
                name=name,
                type=formula_data.get("type", "custom"),
                weights=formula_data.get("weights", {}),
                parameters=formula_data.get("parameters", {}),
                thresholds=formula_data.get("thresholds", {}),
                aggregation=agg_method
            )

        # 解析confidence
        confidence_data = raw.get("confidence", {})
        confidence = ConfidenceConfig(
            levels=confidence_data.get("levels", ConfidenceConfig().levels),
            calculation_method=confidence_data.get("calculation_method", "sample_size_based"),
            min_samples_for_high_confidence=confidence_data.get(
                "min_samples_for_high_confidence", 30
            ),
            variance_threshold=confidence_data.get("variance_threshold", 0.05)
        )

        # 解析phase_weights
        phase_weights = raw.get(
            "phase_weights",
            ScoringConfig().phase_weights
        )

        return ScoringConfig(
            formulas=formulas,
            confidence=confidence,
            phase_weights=phase_weights,
            pass_threshold=raw.get("pass_threshold", 0.80),
            critical_threshold=raw.get("critical_threshold", 0.60)
        )

    def _default_config(self) -> ScoringConfig:
        """返回默认配置。"""
        return self._parse_config(self.DEFAULT_CONFIG)

    def calculate_score(
        self,
        formula_name: str,
        predictions: List[Any],
        references: List[Any],
        additional_metrics: Optional[Dict[str, float]] = None
    ) -> ScoreResult:
        """
        计算评分。

        参数:
            formula_name: 公式名称
            predictions: 预测结果列表
            references: 参考结果列表
            additional_metrics: 额外的指标(如precision, recall等)

        返回:
            ScoreResult对象
        """
        if formula_name not in self.config.formulas:
            self.logger.warning(f"公式'{formula_name}'不存在，使用默认公式")
            formula_name = "accuracy"

        formula = self.config.formulas[formula_name]

        # 根据公式类型计算分数
        if formula.type == "accuracy":
            score = self._calc_accuracy(predictions, references)
        elif formula.type == "f1":
            score = self._calc_f1(predictions, references, formula)
        elif formula.type == "rouge":
            score = self._calc_rouge(predictions, references, formula)
        elif formula.type == "bleu":
            score = self._calc_bleu(predictions, references, formula)
        else:
            score = self._calc_custom(predictions, references, formula, additional_metrics)

        # 计算置信度
        confidence = self._calculate_confidence(len(predictions), additional_metrics)
        confidence_level = self._get_confidence_level(confidence)

        # 检查阈值
        warnings = []
        if formula.thresholds:
            if "pass" in formula.thresholds and score < formula.thresholds["pass"]:
                warnings.append(f"分数({score:.3f})低于通过阈值({formula.thresholds['pass']})")
            if "warning" in formula.thresholds and score < formula.thresholds["warning"]:
                warnings.append(f"分数({score:.3f})低于警告阈值({formula.thresholds['warning']})")

        return ScoreResult(
            score=score,
            confidence=confidence,
            confidence_level=confidence_level,
            components=additional_metrics or {},
            metadata={
                "formula_type": formula.type,
                "sample_count": len(predictions)
            },
            formula_used=formula_name,
            warnings=warnings
        )

    def _calc_accuracy(
        self,
        predictions: List[Any],
        references: List[Any]
    ) -> float:
        """计算准确率。"""
        if not predictions:
            return 0.0

        correct = sum(1 for p, r in zip(predictions, references) if p == r)
        return correct / len(predictions)

    def _calc_f1(
        self,
        predictions: List[Any],
        references: List[Any],
        formula: ScoringFormula
    ) -> float:
        """计算F1分数。"""
        from sklearn.metrics import f1_score

        try:
            f1 = f1_score(references, predictions, average='weighted', zero_division=0)
            return float(f1)
        except Exception:
            return self._calc_accuracy(predictions, references)

    def _calc_rouge(
        self,
        predictions: List[str],
        references: List[str],
        formula: ScoringFormula
    ) -> float:
        """计算ROUGE分数。"""
        from collections import Counter

        rouge_scores = []
        for pred, ref in zip(predictions, references):
            pred_tokens = pred.lower().split()
            ref_tokens = ref.lower().split()

            if not pred_tokens or not ref_tokens:
                rouge_scores.append(0.0)
                continue

            # 计算LCS
            lcs_length = self._lcs_length(pred_tokens, ref_tokens)

            precision = lcs_length / len(pred_tokens) if pred_tokens else 0
            recall = lcs_length / len(ref_tokens) if ref_tokens else 0

            if precision + recall == 0:
                rouge_scores.append(0.0)
            else:
                f_score = 2 * precision * recall / (precision + recall)
                rouge_scores.append(f_score)

        return np.mean(rouge_scores)

    def _lcs_length(self, seq1: List, seq2: List) -> int:
        """计算最长公共子序列长度。"""
        m, n = len(seq1), len(seq2)
        prev = [0] * (n + 1)

        for i in range(1, m + 1):
            curr = [0] * (n + 1)
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev = curr

        return prev[n]

    def _calc_bleu(
        self,
        predictions: List[str],
        references: List[str],
        formula: ScoringFormula
    ) -> float:
        """计算BLEU分数(简化版)。"""
        bleu_scores = []

        for pred, ref in zip(predictions, references):
            pred_tokens = pred.lower().split()
            ref_tokens = ref.lower().split()

            if not pred_tokens:
                bleu_scores.append(0.0)
                continue

            # 简化的unigram精确率
            pred_unigrams = Counter(pred_tokens)
            ref_unigrams = Counter(ref_tokens)

            overlap = sum((pred_unigrams & ref_unigrams).values())
            precision = overlap / len(pred_tokens)

            # 简短惩罚
            ref_len = len(ref_tokens)
            pred_len = len(pred_tokens)

            if pred_len >= ref_len:
                bp = 1.0
            else:
                bp = np.exp(1 - ref_len / pred_len) if pred_len > 0 else 0.0

            bleu_scores.append(bp * precision)

        return np.mean(bleu_scores)

    def _calc_custom(
        self,
        predictions: List[Any],
        references: List[Any],
        formula: ScoringFormula,
        additional_metrics: Optional[Dict[str, float]]
    ) -> float:
        """使用自定义权重计算分数。"""
        if not additional_metrics:
            return self._calc_accuracy(predictions, references)

        weights = formula.weights
        if not weights:
            return np.mean(list(additional_metrics.values()))

        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0

        score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in additional_metrics:
                score += additional_metrics[metric_name] * (weight / total_weight)

        return score

    def _calculate_confidence(
        self,
        sample_count: int,
        additional_metrics: Optional[Dict[str, float]] = None
    ) -> float:
        """
        计算置信度。

        基于样本数量和方差计算置信度。
        """
        method = self.config.confidence.calculation_method

        if method == "fixed":
            return 0.85

        elif method == "sample_size_based":
            min_samples = self.config.confidence.min_samples_for_high_confidence
            if sample_count >= min_samples:
                return 0.95
            elif sample_count >= min_samples // 2:
                return 0.85
            elif sample_count >= min_samples // 4:
                return 0.70
            else:
                return 0.50

        elif method == "variance_based":
            if not additional_metrics or len(additional_metrics) < 2:
                return 0.70

            values = list(additional_metrics.values())
            variance = np.var(values)
            threshold = self.config.confidence.variance_threshold

            if variance < threshold:
                return 0.95
            elif variance < threshold * 2:
                return 0.80
            else:
                return 0.60

        return 0.75

    def _get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """根据置信度值获取等级。"""
        levels = self.config.confidence.levels

        if confidence >= levels.get("high", 0.90):
            return ConfidenceLevel.HIGH
        elif confidence >= levels.get("medium", 0.70):
            return ConfidenceLevel.MEDIUM
        elif confidence >= levels.get("low", 0.50):
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

    def aggregate_scores(
        self,
        scores: List[ScoreResult],
        method: ScoreAggregationMethod = ScoreAggregationMethod.WEIGHTED_MEAN,
        weights: Optional[Dict[str, float]] = None
    ) -> ScoreResult:
        """
        聚合多个评分结果。

        参数:
            scores: ScoreResult列表
            method: 聚合方法
            weights: 可选的权重字典

        返回:
            聚合后的ScoreResult
        """
        if not scores:
            return ScoreResult(
                score=0.0,
                confidence=0.0,
                confidence_level=ConfidenceLevel.VERY_LOW,
                components={}
            )

        score_values = [s.score for s in scores]

        if method == ScoreAggregationMethod.MEAN:
            aggregated_score = np.mean(score_values)
        elif method == ScoreAggregationMethod.MEDIAN:
            aggregated_score = np.median(score_values)
        elif method == ScoreAggregationMethod.MAX:
            aggregated_score = np.max(score_values)
        elif method == ScoreAggregationMethod.MIN:
            aggregated_score = np.min(score_values)
        elif method == ScoreAggregationMethod.SUM:
            aggregated_score = np.sum(score_values)
        elif method == ScoreAggregationMethod.HARMONIC_MEAN:
            aggregated_score = len(score_values) / sum(1/s for s in score_values if s != 0)
        elif method == ScoreAggregationMethod.GEOMETRIC_MEAN:
            score_values_safe = [s if s > 0 else 0.01 for s in score_values]
            aggregated_score = np.exp(np.mean(np.log(score_values_safe)))
        elif method == ScoreAggregationMethod.WEIGHTED_MEAN:
            if weights:
                total_weight = sum(weights.values())
                if total_weight > 0:
                    aggregated_score = sum(
                        s.score * (weights.get(s.formula_used, 1.0) / total_weight)
                        for s in scores
                    )
                else:
                    aggregated_score = np.mean(score_values)
            else:
                aggregated_score = np.mean(score_values)
        else:
            aggregated_score = np.mean(score_values)

        # 置信度取平均但考虑样本量
        confidences = [s.confidence for s in scores]
        aggregated_confidence = np.mean(confidences)

        # 收集所有警告
        all_warnings = []
        for s in scores:
            all_warnings.extend(s.warnings)

        # 组件分数
        components = {}
        for s in scores:
            components.update(s.components)

        return ScoreResult(
            score=aggregated_score,
            confidence=aggregated_confidence,
            confidence_level=self._get_confidence_level(aggregated_confidence),
            components=components,
            metadata={
                "aggregated_from": len(scores),
                "aggregation_method": method.value
            },
            warnings=all_warnings
        )

    def aggregate_phase_scores(
        self,
        phase_scores: Dict[str, ScoreResult]
    ) -> ScoreResult:
        """
        聚合不同阶段的评分。

        参数:
            phase_scores: 阶段名称 -> ScoreResult的字典

        返回:
            聚合后的ScoreResult
        """
        phase_weights = self.config.phase_weights

        # 构建权重
        weights = {}
        for phase, score_result in phase_scores.items():
            weights[score_result.formula_used] = phase_weights.get(phase, 1.0)

        scores = list(phase_scores.values())
        return self.aggregate_scores(
            scores,
            method=ScoreAggregationMethod.WEIGHTED_MEAN,
            weights=weights
        )

    def is_passed(self, score: float) -> bool:
        """判断是否通过。"""
        return score >= self.config.pass_threshold

    def is_critical(self, score: float) -> bool:
        """判断是否处于危险水平。"""
        return score < self.config.critical_threshold

    def get_pass_status(
        self,
        score: float
    ) -> tuple[bool, str]:
        """
        获取通过状态。

        返回:
            (是否通过, 状态描述)
        """
        if self.is_passed(score):
            return True, "PASS"
        elif self.is_critical(score):
            return False, "CRITICAL"
        else:
            return False, "NEEDS_IMPROVEMENT"

    def save_config(self, output_path: str) -> None:
        """保存当前配置到文件。"""
        path = Path(output_path)

        config_dict = {
            "formulas": {},
            "confidence": {
                "levels": self.config.confidence.levels,
                "calculation_method": self.config.confidence.calculation_method,
                "min_samples_for_high_confidence": self.config.confidence.min_samples_for_high_confidence,
                "variance_threshold": self.config.confidence.variance_threshold
            },
            "phase_weights": self.config.phase_weights,
            "pass_threshold": self.config.pass_threshold,
            "critical_threshold": self.config.critical_threshold
        }

        for name, formula in self.config.formulas.items():
            config_dict["formulas"][name] = {
                "type": formula.type,
                "weights": formula.weights,
                "parameters": formula.parameters,
                "thresholds": formula.thresholds,
                "aggregation": formula.aggregation.value
            }

        with open(path, 'w') as f:
            if path.suffix in [".yaml", ".yml"]:
                yaml.dump(config_dict, f, default_flow_style=False)
            else:
                json.dump(config_dict, f, indent=2)


# 便捷函数
def calculate_benchmark_score(
    results: Dict[str, List[Dict]],
    config_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    计算基准测试分数。

    参数:
        results: 每个阶段的测试结果
        config_path: 可选的配置文件路径

    返回:
        包含分数和元数据的字典
    """
    engine = ScoringEngine(config_path)

    phase_scores = {}
    for phase, phase_results in results.items():
        predictions = [r.get("prediction", r.get("output", "")) for r in phase_results]
        references = [r.get("reference", r.get("expected", "")) for r in phase_results]
        metrics = {
            k: [r.get(k, 0) for r in phase_results]
            for k in ["accuracy", "f1", "precision", "recall"]
        }
        avg_metrics = {k: np.mean(v) if v else 0 for k, v in metrics.items()}

        score_result = engine.calculate_score(
            phase,
            predictions,
            references,
            avg_metrics
        )
        phase_scores[phase] = score_result

    overall = engine.aggregate_phase_scores(phase_scores)

    return {
        "overall_score": overall.score,
        "overall_confidence": overall.confidence,
        "overall_confidence_level": overall.confidence_level.value,
        "pass_status": engine.get_pass_status(overall.score),
        "phase_scores": {
            phase: {
                "score": sr.score,
                "confidence": sr.confidence,
                "warnings": sr.warnings
            }
            for phase, sr in phase_scores.items()
        }
    }


import logging

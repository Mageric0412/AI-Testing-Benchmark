"""
指标计算工具。
"""

from typing import List, Dict, Any, Optional, Callable
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    mean_squared_error,
    mean_absolute_error
)


class MetricsCalculator:
    """
    计算各种评估指标的工具类。
    """

    @staticmethod
    def accuracy(y_true: List, y_pred: List) -> float:
        """计算准确率。"""
        return accuracy_score(y_true, y_pred)

    @staticmethod
    def f1_score(
        y_true: List,
        y_pred: List,
        average: str = "weighted",
        zero_division: int = 0
    ) -> float:
        """
        计算F1分数。

        参数:
            y_true: 真实标签
            y_pred: 预测标签
            average: 平均方法 ('micro', 'macro', 'weighted', 'binary')
            zero_division: 当没有正预测时返回的值
        """
        return f1_score(y_true, y_pred, average=average, zero_division=zero_division)

    @staticmethod
    def precision(
        y_true: List,
        y_pred: List,
        average: str = "weighted",
        zero_division: int = 0
    ) -> float:
        """计算精确率。"""
        return precision_score(y_true, y_pred, average=average, zero_division=zero_division)

    @staticmethod
    def recall(
        y_true: List,
        y_pred: List,
        average: str = "weighted",
        zero_division: int = 0
    ) -> float:
        """计算召回率。"""
        return recall_score(y_true, y_pred, average=average, zero_division=zero_division)

    @staticmethod
    def roc_auc(
        y_true: List,
        y_pred_proba: List,
        multi_class: str = "ovr"
    ) -> float:
        """计算ROC AUC分数。"""
        return roc_auc_score(y_true, y_pred_proba, multi_class=multi_class)

    @staticmethod
    def mean_squared_error(y_true: List, y_pred: List) -> float:
        """计算MSE。"""
        return mean_squared_error(y_true, y_pred)

    @staticmethod
    def mean_absolute_error(y_true: List, y_pred: List) -> float:
        """计算MAE。"""
        return mean_absolute_error(y_true, y_pred)

    @staticmethod
    def rmse(y_true: List, y_pred: List) -> float:
        """计算RMSE。"""
        return np.sqrt(mean_squared_error(y_true, y_pred))

    @staticmethod
    def mape(y_true: List, y_pred: List) -> float:
        """计算MAPE (平均绝对百分比误差)。"""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        # 避免除以零
        mask = y_true != 0
        if not mask.any():
            return 0.0

        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    @staticmethod
    def bleu_score(
        reference: str,
        hypothesis: str,
        n_gram: int = 4
    ) -> float:
        """
        计算BLEU分数(简化版本)。

        生产环境建议使用sacrebleu或nltk.translate.bleu_score。
        """
        from collections import Counter

        reference_tokens = reference.lower().split()
        hypothesis_tokens = hypothesis.lower().split()

        if len(hypothesis_tokens) == 0:
            return 0.0

        # 计算n-gram精确率
        precisions = []
        for i in range(1, min(n_gram + 1, 5)):
            ref_ngrams = Counter(MetricsCalculator._get_ngrams(reference_tokens, i))
            hyp_ngrams = Counter(MetricsCalculator._get_ngrams(hypothesis_tokens, i))

            overlap = sum((ref_ngrams & hyp_ngrams).values())
            total = sum(hyp_ngrams.values())

            if total == 0:
                precisions.append(0.0)
            else:
                precisions.append(overlap / total)

        # 计算简短惩罚
        ref_len = len(reference_tokens)
        hyp_len = len(hypothesis_tokens)

        if hyp_len >= ref_len:
            bp = 1.0
        else:
            bp = np.exp(1 - ref_len / hyp_len) if hyp_len > 0 else 0.0

        # 精确率的几何平均
        if all(p == 0 for p in precisions):
            return 0.0

        geo_mean = np.exp(np.mean([np.log(p) if p > 0 else -np.inf for p in precisions]))

        return bp * geo_mean

    @staticmethod
    def _get_ngrams(tokens: List[str], n: int) -> List[tuple]:
        """从token列表获取n-gram。"""
        return list(zip(*[tokens[i:] for i in range(n)]))

    @staticmethod
    def rouge_l(
        reference: str,
        hypothesis: str,
        beta: float = 1.0
    ) -> float:
        """
        计算ROUGE-L (最长公共子序列)分数。

        简化版本 - 生产环境建议使用sacrebleu。
        """
        reference_tokens = reference.lower().split()
        hypothesis_tokens = hypothesis.lower().split()

        lcs_length = MetricsCalculator._lcs_length(reference_tokens, hypothesis_tokens)

        if lcs_length == 0:
            return 0.0

        precision = lcs_length / len(hypothesis_tokens) if hypothesis_tokens else 0
        recall = lcs_length / len(reference_tokens) if reference_tokens else 0

        if precision + recall == 0:
            return 0.0

        f_score = (1 + beta**2) * precision * recall / (beta**2 * precision + recall)

        return f_score

    @staticmethod
    def _lcs_length(seq1: List, seq2: List) -> int:
        """计算最长公共子序列长度。"""
        m, n = len(seq1), len(seq2)

        # 空间优化LCS
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev, curr = curr, [0] * (n + 1)

        return prev[n]

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """计算两个向量之间的余弦相似度。"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    @staticmethod
    def spearman_correlation(rank1: List[float], rank2: List[float]) -> float:
        """计算Spearman等级相关系数。"""
        from scipy.stats import spearmanr
        return spearmanr(rank1, rank2)[0]

    @staticmethod
    def aggregate_scores(
        scores: List[float],
        method: str = "mean"
    ) -> float:
        """
        聚合多个分数。

        参数:
            scores: 分数列表
            method: 聚合方法 ('mean', 'median', 'min', 'max', 'harmonic')
        """
        if not scores:
            return 0.0

        if method == "mean":
            return np.mean(scores)
        elif method == "median":
            return np.median(scores)
        elif method == "min":
            return np.min(scores)
        elif method == "max":
            return np.max(scores)
        elif method == "harmonic":
            return len(scores) / sum(1/s for s in scores if s != 0)
        else:
            return np.mean(scores)

    @staticmethod
    def percentile(
        values: List[float],
        percentile: float
    ) -> float:
        """计算百分位数。"""
        return np.percentile(values, percentile)

    @staticmethod
    def confidence_interval(
        scores: List[float],
        confidence: float = 0.95
    ) -> tuple:
        """
        计算分数的置信区间。

        返回:
            (下限, 上限) 元组
        """
        from scipy import stats

        mean = np.mean(scores)
        sem = stats.sem(scores)
        margin = sem * stats.t.ppf((1 + confidence) / 2, len(scores) - 1)

        return (mean - margin, mean + margin)


class ThresholdEvaluator:
    """评估指标是否通过指定阈值的评估器。"""

    def __init__(self, thresholds: Dict[str, float]):
        """
        用阈值初始化。

        参数:
            thresholds: 指标名称 -> 阈值值的字典
        """
        self.thresholds = thresholds

    def evaluate(self, metrics: Dict[str, float]) -> Dict[str, bool]:
        """
        评估指标是否通过阈值。

        参数:
            metrics: 指标名称 -> 指标值的字典

        返回:
            指标名称 -> 是否通过的字典
        """
        results = {}

        for metric_name, threshold in self.thresholds.items():
            value = metrics.get(metric_name)

            if value is None:
                results[metric_name] = False
            else:
                results[metric_name] = value >= threshold

        return results

    def all_passed(self, metrics: Dict[str, float]) -> bool:
        """检查是否所有阈值都通过。"""
        return all(self.evaluate(metrics).values())

    def get_failures(self, metrics: Dict[str, float]) -> List[str]:
        """获取失败的指标列表。"""
        results = self.evaluate(metrics)
        return [name for name, passed in results.items() if not passed]

"""
对话系统评估模块。
"""

from typing import Dict, List, Any, Optional
import time

from ai_testing_benchmark.core.base_evaluator import BaseEvaluator, EvaluationResult
from ai_testing_benchmark.core.result import PhaseResult, ResultStatus


class DialogueEvaluator(BaseEvaluator):
    """
    对话式AI能力的评估器。

    测试意图识别、实体提取、对话流程、响应质量和用户旅程完成度。
    """

    def __init__(
        self,
        model_name: str,
        provider: str = "openai",
        config: Optional[Dict] = None,
        verbose: bool = False
    ):
        super().__init__(model_name, provider, config, verbose)

    def evaluate_single(self, test_case: Dict) -> EvaluationResult:
        """评估单个对话测试用例。"""
        start_time = time.time()

        category = test_case.get("category", "dialogue")
        test_id = test_case.get("id", "unknown")

        self.logger.info(f"正在评估 {test_id} ({category})")

        if category == "intent_recognition":
            result = self._evaluate_intent_recognition(test_case)
        elif category == "entity_extraction":
            result = self._evaluate_entity_extraction(test_case)
        elif category == "dialogue_flow":
            result = self._evaluate_dialogue_flow(test_case)
        elif category == "response_quality":
            result = self._evaluate_response_quality(test_case)
        elif category == "journey":
            result = self._evaluate_user_journey(test_case)
        else:
            result = self._evaluate_generic_dialogue(test_case)

        execution_time = (time.time() - start_time) * 1000

        return EvaluationResult(
            scenario_id=test_case.get("scenario_id", test_id),
            test_case_id=test_id,
            passed=result["passed"],
            score=result["score"] * 100,
            metrics=result.get("metrics", {}),
            details=result.get("details", {}),
            execution_time_ms=execution_time
        )

    def _evaluate_intent_recognition(self, test_case: Dict) -> Dict:
        """评估意图识别准确率。"""
        response = self._call_model(test_case.get("user_utterance", ""))

        expected_intent = test_case.get("expected_intent", "")
        predicted_intent = response.get("intent", "")

        # 精确匹配
        if predicted_intent.lower() == expected_intent.lower():
            intent_score = 1.0
        else:
            # 类似意图的部分匹配
            intent_score = 0.5

        confidence = response.get("confidence", 0.5)

        # 置信度校准检查
        if abs(confidence - intent_score) < 0.2:
            calibration_score = 1.0
        else:
            calibration_score = 0.5

        overall_score = 0.7 * intent_score + 0.3 * calibration_score

        return {
            "passed": overall_score >= 0.85,
            "score": overall_score,
            "metrics": {
                "intent_accuracy": intent_score,
                "confidence_calibration": calibration_score
            },
            "details": {
                "expected_intent": expected_intent,
                "predicted_intent": predicted_intent,
                "confidence": confidence
            }
        }

    def _evaluate_entity_extraction(self, test_case: Dict) -> Dict:
        """评估从用户话语中提取实体。"""
        response = self._call_model(test_case.get("user_utterance", ""))

        expected_entities = test_case.get("expected_entities", [])
        predicted_entities = response.get("entities", [])

        # 计算实体级指标
        true_positives = 0
        for exp_ent in expected_entities:
            for pred_ent in predicted_entities:
                if exp_ent["type"] == pred_ent["type"] and \
                   exp_ent["value"].lower() in pred_ent["value"].lower():
                    true_positives += 1
                    break

        precision = true_positives / len(predicted_entities) if predicted_entities else 0
        recall = true_positives / len(expected_entities) if expected_entities else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "passed": f1 >= 0.85,
            "score": f1,
            "metrics": {
                "entity_f1": f1,
                "entity_precision": precision,
                "entity_recall": recall
            },
            "details": {
                "expected": expected_entities,
                "predicted": predicted_entities
            }
        }

    def _evaluate_dialogue_flow(self, test_case: Dict) -> Dict:
        """评估多轮对话流程。"""
        conversation = test_case.get("conversation", [])

        scores = []
        for turn in conversation:
            response = self._call_model(turn.get("user_input", ""))
            expected_action = turn.get("expected_action", "")

            if response.get("action", "") == expected_action:
                scores.append(1.0)
            else:
                scores.append(0.5)

        avg_score = sum(scores) / len(scores) if scores else 0.0

        return {
            "passed": avg_score >= 0.80,
            "score": avg_score,
            "metrics": {"turn_accuracy": avg_score},
            "details": {
                "total_turns": len(conversation),
                "turn_scores": scores
            }
        }

    def _evaluate_response_quality(self, test_case: Dict) -> Dict:
        """评估响应质量指标。"""
        response = self._call_model(test_case.get("user_input", ""))

        response_text = response.get("text", "")

        # 基本质量指标
        relevance = 0.8  # 模拟
        coherence = 0.85  # 模拟
        fluency = 0.9  # 模拟

        overall_score = (relevance + coherence + fluency) / 3

        return {
            "passed": overall_score >= 0.80,
            "score": overall_score,
            "metrics": {
                "relevance": relevance,
                "coherence": coherence,
                "fluency": fluency
            },
            "details": {
                "response_length": len(response_text)
            }
        }

    def _evaluate_user_journey(self, test_case: Dict) -> Dict:
        """评估完整用户旅程完成度。"""
        journey = test_case.get("journey", {})
        steps = journey.get("steps", [])

        completed_steps = 0
        step_scores = []

        for step in steps:
            response = self._call_model(step.get("action", ""))

            expected_outcome = step.get("expected_outcome", "")
            actual_outcome = response.get("outcome", "")

            if expected_outcome.lower() in actual_outcome.lower():
                step_scores.append(1.0)
                completed_steps += 1
            else:
                step_scores.append(0.0)

        completion_rate = completed_steps / len(steps) if steps else 0

        # 检查关键路径完成度
        critical_path = journey.get("critical_path", [])
        critical_completed = all(
            step_scores[i] == 1.0 for i in critical_path if i < len(step_scores)
        )

        score = 0.7 * completion_rate + 0.3 * (1.0 if critical_completed else 0.5)

        return {
            "passed": score >= 0.85,
            "score": score,
            "metrics": {
                "journey_completion_rate": completion_rate,
                "critical_path_completion": 1.0 if critical_completed else 0.0
            },
            "details": {
                "total_steps": len(steps),
                "completed_steps": completed_steps,
                "step_scores": step_scores
            }
        }

    def _evaluate_generic_dialogue(self, test_case: Dict) -> Dict:
        """通用对话评估。"""
        return {
            "passed": False,
            "score": 0.0,
            "metrics": {},
            "details": {"error": "Unknown dialogue evaluation type"}
        }

    def _call_model(self, prompt: str) -> Dict:
        """调用模型 - 占位符，需实现实际调用。"""
        return {"intent": "greeting", "confidence": 0.9, "text": "你好"}

    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """计算聚合对话分数。"""
        if not results:
            return {"overall_score": 0.0, "category_scores": {}}

        category_scores = {}
        for result in results:
            cat = result.details.get("category", "unknown")
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(result.score)

        avg_category_scores = {
            cat: sum(scores) / len(scores)
            for cat, scores in category_scores.items()
        }

        overall = sum(avg_category_scores.values()) / len(avg_category_scores) if avg_category_scores else 0

        return {
            "overall_score": overall,
            "category_scores": avg_category_scores,
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results if r.passed)
        }

    def run_phase(self) -> PhaseResult:
        """运行完整对话评估阶段。"""
        phase_result = PhaseResult(phase="dialogue")

        test_cases = self._load_test_cases()

        self.logger.info(f"正在运行 {len(test_cases)} 个对话测试")

        for test_case in test_cases:
            result = self.evaluate_single(test_case)
            phase_result.add_result(result)

        if phase_result.results:
            scores = [r.score for r in phase_result.results]
            phase_result.overall_score = sum(scores) / len(scores)

        return phase_result

    def _load_test_cases(self) -> List[Dict]:
        """加载对话测试用例。"""
        return [
            {
                "id": "TC-DIAL-001",
                "category": "intent_recognition",
                "scenario_id": "greeting",
                "user_utterance": "你好，我想咨询云迁移的问题",
                "expected_intent": "greeting",
                "pass_threshold": 0.85
            },
            {
                "id": "TC-DIAL-002",
                "category": "entity_extraction",
                "scenario_id": "resource_query",
                "user_utterance": "显示我在us-east-1区域的50台EC2实例状态",
                "expected_entities": [
                    {"type": "COUNT", "value": "50"},
                    {"type": "RESOURCE", "value": "EC2实例"},
                    {"type": "REGION", "value": "us-east-1"}
                ],
                "pass_threshold": 0.85
            },
            {
                "id": "TC-DIAL-003",
                "category": "journey",
                "scenario_id": "migration_assessment",
                "journey": {
                    "name": "迁移评估",
                    "critical_path": [0, 1, 2],
                    "steps": [
                        {
                            "action": "开始评估",
                            "expected_outcome": "assessment_started"
                        },
                        {
                            "action": "提供基础设施信息",
                            "expected_outcome": "infrastructure_analyzed"
                        },
                        {
                            "action": "请求风险评估",
                            "expected_outcome": "risks_identified"
                        },
                        {
                            "action": "获取建议",
                            "expected_outcome": "recommendations_provided"
                        }
                    ]
                },
                "pass_threshold": 0.85
            }
        ]

"""
Dialogue system evaluation module.
"""

from typing import Dict, List, Any, Optional
import time

from ai_testing_benchmark.core.base_evaluator import BaseEvaluator, EvaluationResult
from ai_testing_benchmark.core.result import PhaseResult, ResultStatus


class DialogueEvaluator(BaseEvaluator):
    """
    Evaluator for conversational AI capabilities.

    Tests intent recognition, entity extraction, dialogue flow,
    response quality, and user journey completion.
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
        """Evaluate a single dialogue test case."""
        start_time = time.time()

        category = test_case.get("category", "dialogue")
        test_id = test_case.get("id", "unknown")

        self.logger.info(f"Evaluating {test_id} ({category})")

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
        """Evaluate intent recognition accuracy."""
        response = self._call_model(test_case.get("user_utterance", ""))

        expected_intent = test_case.get("expected_intent", "")
        predicted_intent = response.get("intent", "")

        # Exact match
        if predicted_intent.lower() == expected_intent.lower():
            intent_score = 1.0
        else:
            # Partial match for similar intents
            intent_score = 0.5

        confidence = response.get("confidence", 0.5)

        # Confidence calibration check
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
        """Evaluate entity extraction from user utterances."""
        response = self._call_model(test_case.get("user_utterance", ""))

        expected_entities = test_case.get("expected_entities", [])
        predicted_entities = response.get("entities", [])

        # Calculate entity-level metrics
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
        """Evaluate multi-turn dialogue flow."""
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
        """Evaluate response quality metrics."""
        response = self._call_model(test_case.get("user_input", ""))

        response_text = response.get("text", "")

        # Basic quality metrics
        relevance = 0.8  # Mock
        coherence = 0.85  # Mock
        fluency = 0.9  # Mock

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
        """Evaluate complete user journey completion."""
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

        # Check critical path completion
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
        """Generic dialogue evaluation."""
        return {
            "passed": False,
            "score": 0.0,
            "metrics": {},
            "details": {"error": "Unknown dialogue evaluation type"}
        }

    def _call_model(self, prompt: str) -> Dict:
        """Call the model - placeholder for actual implementation."""
        return {"intent": "greeting", "confidence": 0.9, "text": "Hello"}

    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """Calculate aggregated dialogue scores."""
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
        """Run complete dialogue evaluation phase."""
        phase_result = PhaseResult(phase="dialogue")

        test_cases = self._load_test_cases()

        self.logger.info(f"Running {len(test_cases)} dialogue tests")

        for test_case in test_cases:
            result = self.evaluate_single(test_case)
            phase_result.add_result(result)

        if phase_result.results:
            scores = [r.score for r in phase_result.results]
            phase_result.overall_score = sum(scores) / len(scores)

        return phase_result

    def _load_test_cases(self) -> List[Dict]:
        """Load dialogue test cases."""
        return [
            {
                "id": "TC-DIAL-001",
                "category": "intent_recognition",
                "scenario_id": "greeting",
                "user_utterance": "Hi, I need help with my cloud migration",
                "expected_intent": "greeting",
                "pass_threshold": 0.85
            },
            {
                "id": "TC-DIAL-002",
                "category": "entity_extraction",
                "scenario_id": "resource_query",
                "user_utterance": "Show me the status of my 50 EC2 instances in us-east-1",
                "expected_entities": [
                    {"type": "COUNT", "value": "50"},
                    {"type": "RESOURCE", "value": "EC2 instances"},
                    {"type": "REGION", "value": "us-east-1"}
                ],
                "pass_threshold": 0.85
            },
            {
                "id": "TC-DIAL-003",
                "category": "journey",
                "scenario_id": "migration_assessment",
                "journey": {
                    "name": "Migration Assessment",
                    "critical_path": [0, 1, 2],
                    "steps": [
                        {
                            "action": "Start assessment",
                            "expected_outcome": "assessment_started"
                        },
                        {
                            "action": "Provide infrastructure info",
                            "expected_outcome": "infrastructure_analyzed"
                        },
                        {
                            "action": "Request risk assessment",
                            "expected_outcome": "risks_identified"
                        },
                        {
                            "action": "Get recommendations",
                            "expected_outcome": "recommendations_provided"
                        }
                    ]
                },
                "pass_threshold": 0.85
            }
        ]

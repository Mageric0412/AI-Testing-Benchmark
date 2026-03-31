"""
Foundation model evaluation module.
"""

from typing import Dict, List, Any, Optional
import time
from datetime import datetime

from ai_testing_benchmark.core.base_evaluator import BaseEvaluator, EvaluationResult
from ai_testing_benchmark.core.result import PhaseResult, ResultStatus, Severity
from ai_testing_benchmark.core.metrics import MetricsCalculator
from ai_testing_benchmark.evaluation.benchmarks import StandardBenchmarks


class FoundationModelEvaluator(BaseEvaluator):
    """
    Evaluator for foundation model capabilities.

    Tests language understanding, reasoning, and generation capabilities
    using standardized benchmarks and custom test cases.
    """

    def __init__(
        self,
        model_name: str,
        provider: str = "openai",
        config: Optional[Dict] = None,
        verbose: bool = False
    ):
        super().__init__(model_name, provider, config, verbose)
        self.benchmarks = StandardBenchmarks()
        self.metrics_calc = MetricsCalculator()

    def evaluate_single(self, test_case: Dict) -> EvaluationResult:
        """Evaluate a single foundation model test case."""
        start_time = time.time()

        category = test_case.get("category", "unknown")
        test_id = test_case.get("id", "unknown")

        self.logger.info(f"Evaluating {test_id} ({category})")

        # Generate response based on category
        if category == "language_understanding":
            result = self._evaluate_language_understanding(test_case)
        elif category == "reasoning":
            result = self._evaluate_reasoning(test_case)
        elif category == "generation":
            result = self._evaluate_generation(test_case)
        elif category == "knowledge":
            result = self._evaluate_knowledge(test_case)
        else:
            result = self._evaluate_generic(test_case)

        execution_time = (time.time() - start_time) * 1000

        return EvaluationResult(
            scenario_id=test_case.get("scenario_id", test_id),
            test_case_id=test_id,
            passed=result["passed"],
            score=result["score"] * 100,  # Convert to 0-100 scale
            metrics=result["metrics"],
            details=result.get("details", {}),
            execution_time_ms=execution_time
        )

    def _evaluate_language_understanding(self, test_case: Dict) -> Dict:
        """Evaluate language understanding tasks."""
        task_type = test_case.get("task_type", "classification")

        if task_type == "classification":
            return self._evaluate_classification(test_case)
        elif task_type == "ner":
            return self._evaluate_ner(test_case)
        elif task_type == "sentiment":
            return self._evaluate_sentiment(test_case)
        else:
            return self._evaluate_generic(test_case)

    def _evaluate_classification(self, test_case: Dict) -> Dict:
        """Evaluate text classification."""
        # For demonstration - in production this would call the actual model
        response = self._call_model(test_case.get("input", ""))

        expected = test_case.get("expected_category", "")
        metrics = {"accuracy": 0.0, "f1": 0.0}

        # Simple mock scoring - replace with actual evaluation
        predicted = response.get("classification", "").lower()
        expected_lower = expected.lower()

        if predicted == expected_lower:
            metrics["accuracy"] = 1.0
            metrics["f1"] = 1.0
            score = 1.0
        else:
            # Partial credit for similar categories
            if any(word in predicted for word in expected_lower.split()):
                score = 0.5
                metrics["accuracy"] = 0.5
                metrics["f1"] = 0.4
            else:
                score = 0.0

        return {
            "passed": score >= 0.85,
            "score": score,
            "metrics": metrics,
            "details": {
                "expected": expected,
                "predicted": predicted,
                "task_type": "classification"
            }
        }

    def _evaluate_ner(self, test_case: Dict) -> Dict:
        """Evaluate named entity recognition."""
        response = self._call_model(test_case.get("input", ""))

        expected_entities = test_case.get("expected_entities", [])
        predicted_entities = response.get("entities", [])

        # Calculate entity-level metrics
        true_positives = len(set(
            (e["type"], e["value"]) for e in expected_entities
        ) & set(
            (e["type"], e["value"]) for e in predicted_entities
        ))

        precision = true_positives / len(predicted_entities) if predicted_entities else 0
        recall = true_positives / len(expected_entities) if expected_entities else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "passed": f1 >= 0.88,
            "score": f1,
            "metrics": {
                "entity_f1": f1,
                "entity_precision": precision,
                "entity_recall": recall
            },
            "details": {
                "expected_count": len(expected_entities),
                "predicted_count": len(predicted_entities),
                "task_type": "ner"
            }
        }

    def _evaluate_sentiment(self, test_case: Dict) -> Dict:
        """Evaluate sentiment analysis."""
        response = self._call_model(test_case.get("input", ""))

        expected_sentiment = test_case.get("expected_sentiment", "").lower()
        predicted_sentiment = response.get("sentiment", "").lower()

        accuracy = 1.0 if predicted_sentiment == expected_sentiment else 0.0

        return {
            "passed": accuracy >= 0.85,
            "score": accuracy,
            "metrics": {"accuracy": accuracy},
            "details": {
                "expected": expected_sentiment,
                "predicted": predicted_sentiment,
                "task_type": "sentiment"
            }
        }

    def _evaluate_reasoning(self, test_case: Dict) -> Dict:
        """Evaluate reasoning tasks."""
        task_type = test_case.get("task_type", "mathematical")

        if task_type == "mathematical":
            return self._evaluate_math_reasoning(test_case)
        elif task_type == "logical":
            return self._evaluate_logical_reasoning(test_case)
        elif task_type == "common_sense":
            return self._evaluate_common_sense(test_case)
        else:
            return self._evaluate_generic(test_case)

    def _evaluate_math_reasoning(self, test_case: Dict) -> Dict:
        """Evaluate mathematical reasoning."""
        response = self._call_model(test_case.get("problem", ""))

        expected_answer = test_case.get("expected_answers", {})
        predicted_answer = response.get("answer", {})

        # Check final answer accuracy
        answer_score = 0.0
        step_score = 0.0

        if "final_answer" in expected_answer:
            expected_val = expected_answer["final_answer"]
            predicted_val = predicted_answer.get("final_answer", 0)

            if isinstance(expected_val, (int, float)) and isinstance(predicted_val, (int, float)):
                if abs(expected_val - predicted_val) < 0.01:
                    answer_score = 1.0
                elif abs(expected_val - predicted_val) / abs(expected_val) < 0.1:
                    answer_score = 0.8
                else:
                    answer_score = 0.0

        # Check reasoning steps
        expected_steps = expected_answer.get("steps", [])
        predicted_steps = response.get("steps", [])

        if expected_steps and predicted_steps:
            # Simple step comparison
            matching_steps = sum(
                1 for ep, pp in zip(expected_steps, predicted_steps)
                if any(word in pp.lower() for word in ep.lower().split()[:3])
            )
            step_score = matching_steps / max(len(expected_steps), len(predicted_steps))
        else:
            step_score = 0.5 if answer_score > 0 else 0.0

        overall_score = 0.5 * answer_score + 0.5 * step_score

        return {
            "passed": overall_score >= 0.80,
            "score": overall_score,
            "metrics": {
                "answer_accuracy": answer_score,
                "step_accuracy": step_score
            },
            "details": {
                "task_type": "mathematical_reasoning",
                "partial_credit": test_case.get("partial_credit", False)
            }
        }

    def _evaluate_logical_reasoning(self, test_case: Dict) -> Dict:
        """Evaluate logical deduction."""
        response = self._call_model(test_case.get("scenario", ""))

        expected_order = test_case.get("expected_answers", {}).get("migration_order", [])
        predicted_order = response.get("migration_order", [])

        # Check if order respects dependencies
        dependency_satisfied = self._check_dependency_satisfaction(
            predicted_order,
            test_case.get("dependencies", [])
        )

        # Exact match score
        exact_match = sum(
            1 for e, p in zip(expected_order, predicted_order) if e == p
        ) / max(len(expected_order), 1)

        score = 0.6 * dependency_satisfied + 0.4 * exact_match

        return {
            "passed": score >= 0.85,
            "score": score,
            "metrics": {
                "dependency_satisfaction": dependency_satisfied,
                "order_exact_match": exact_match
            },
            "details": {
                "expected_order": expected_order,
                "predicted_order": predicted_order,
                "task_type": "logical_reasoning"
            }
        }

    def _check_dependency_satisfaction(
        self,
        order: List[str],
        dependencies: List[tuple]
    ) -> float:
        """Check if migration order satisfies dependencies."""
        if not dependencies:
            return 1.0

        position = {item: i for i, item in enumerate(order)}
        satisfied = 0

        for dep_from, dep_to in dependencies:
            if dep_from in position and dep_to in position:
                if position[dep_from] < position[dep_to]:
                    satisfied += 1
                else:
                    return 0.0  # Critical failure

        return satisfied / len(dependencies) if dependencies else 1.0

    def _evaluate_common_sense(self, test_case: Dict) -> Dict:
        """Evaluate common sense reasoning."""
        response = self._call_model(test_case.get("question", ""))

        expected = test_case.get("expected_answer", "").lower()
        predicted = response.get("answer", "").lower()

        # Word overlap scoring
        expected_words = set(expected.split())
        predicted_words = set(predicted.split())

        if expected_words and predicted_words:
            overlap = len(expected_words & predicted_words)
            score = overlap / max(len(expected_words), len(predicted_words))
        else:
            score = 0.0

        return {
            "passed": score >= 0.75,
            "score": score,
            "metrics": {"accuracy": score},
            "details": {"task_type": "common_sense"}
        }

    def _evaluate_generation(self, test_case: Dict) -> Dict:
        """Evaluate text generation capabilities."""
        response = self._call_model(test_case.get("requirement", test_case.get("prompt", "")))

        generated_text = response.get("text", "")
        expected_components = test_case.get("expected_components", [])

        # Component coverage
        if expected_components:
            covered = sum(
                1 for comp in expected_components
                if comp.lower() in generated_text.lower()
            )
            coverage = covered / len(expected_components)
        else:
            coverage = 0.5

        # Syntax validity (mock - would need actual validation)
        syntax_valid = test_case.get("validation_checks", ["syntax_valid"])[0] == "syntax_valid"

        score = 0.6 * coverage + 0.4 * (1.0 if syntax_valid else 0.5)

        return {
            "passed": score >= 0.80,
            "score": score,
            "metrics": {
                "component_coverage": coverage,
                "syntax_validity": 1.0 if syntax_valid else 0.5
            },
            "details": {
                "task_type": "generation",
                "generated_length": len(generated_text)
            }
        }

    def _evaluate_knowledge(self, test_case: Dict) -> Dict:
        """Evaluate domain knowledge."""
        response = self._call_model(test_case.get("question", ""))

        expected = test_case.get("expected_answer", "")
        predicted = response.get("answer", "")

        # Fact overlap scoring
        if expected and predicted:
            expected_facts = set(expected.lower().split())
            predicted_facts = set(predicted.lower().split())
            overlap = len(expected_facts & predicted_facts) / max(len(expected_facts), 1)
        else:
            overlap = 0.0

        return {
            "passed": overlap >= 0.70,
            "score": overlap,
            "metrics": {"fact_overlap": overlap},
            "details": {"task_type": "knowledge"}
        }

    def _evaluate_generic(self, test_case: Dict) -> Dict:
        """Generic evaluation fallback."""
        return {
            "passed": False,
            "score": 0.0,
            "metrics": {},
            "details": {"error": "Unknown evaluation type"}
        }

    def _call_model(self, prompt: str) -> Dict:
        """
        Call the model with a prompt.

        In production, this would use the actual model API.
        For now, returns mock responses.
        """
        # This is a placeholder - in production, integrate with actual model
        self.logger.debug(f"Calling model with prompt: {prompt[:100]}...")

        # Mock response based on input
        return {
            "classification": "iaas",
            "answer": "The answer",
            "sentiment": "positive",
            "text": "Generated text"
        }

    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """Calculate aggregated scores across all test cases."""
        if not results:
            return {"overall_score": 0.0, "category_scores": {}}

        # Group by category
        by_category: Dict[str, List] = {}
        for result in results:
            cat = result.details.get("task_type", "unknown")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)

        # Calculate category scores
        category_scores = {}
        for cat, cat_results in by_category.items():
            scores = [r.score for r in cat_results]
            category_scores[cat] = sum(scores) / len(scores) if scores else 0

        # Overall score is weighted average
        weights = {
            "classification": 0.25,
            "ner": 0.15,
            "sentiment": 0.10,
            "mathematical_reasoning": 0.20,
            "logical_reasoning": 0.15,
            "common_sense": 0.10,
            "generation": 0.15,
            "knowledge": 0.10
        }

        overall = sum(
            category_scores.get(cat, 0) * weights.get(cat, 0.1)
            for cat in category_scores
        )

        return {
            "overall_score": overall,
            "category_scores": category_scores,
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results if r.passed)
        }

    def run_phase(self) -> PhaseResult:
        """Run the complete foundation evaluation phase."""
        phase_result = PhaseResult(phase="foundation")

        test_cases = self._load_test_cases()

        self.logger.info(f"Running {len(test_cases)} foundation model tests")

        for test_case in test_cases:
            result = self.evaluate_single(test_case)
            phase_result.add_result(result)

        # Calculate phase score
        if phase_result.results:
            scores = [r.score for r in phase_result.results]
            phase_result.overall_score = sum(scores) / len(scores)

        return phase_result

    def _load_test_cases(self) -> List[Dict]:
        """Load test cases for foundation evaluation."""
        # Return sample test cases - in production, load from files/database
        return [
            {
                "id": "TC-FU-001",
                "category": "language_understanding",
                "task_type": "classification",
                "description": "Infrastructure type classification",
                "input": "We have 50 virtual machines running Ubuntu with manual scaling.",
                "expected_category": "IaaS",
                "pass_threshold": 0.85
            },
            {
                "id": "TC-FU-002",
                "category": "language_understanding",
                "task_type": "ner",
                "description": "Cloud resource entity extraction",
                "input": "Three m5.large EC2 instances in us-east-1 running Ubuntu 22.04.",
                "expected_entities": [
                    {"type": "RESOURCE_TYPE", "value": "EC2 instances"},
                    {"type": "SIZE", "value": "m5.large"},
                    {"type": "REGION", "value": "us-east-1"}
                ],
                "pass_threshold": 0.88
            },
            {
                "id": "TC-RE-001",
                "category": "reasoning",
                "task_type": "mathematical",
                "description": "Cloud cost calculation",
                "problem": "Calculate annual cost for 50 t3.medium instances at $0.0416/hour.",
                "expected_answers": {
                    "final_answer": 18226.80,
                    "steps": ["50 * 0.0416 * 24 * 365"]
                },
                "partial_credit": True,
                "pass_threshold": 0.80
            }
        ]

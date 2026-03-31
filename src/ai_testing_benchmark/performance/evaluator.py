"""
Performance evaluation module.
"""

from typing import Dict, List, Any, Optional
import time
import numpy as np

from ai_testing_benchmark.core.base_evaluator import BaseEvaluator, EvaluationResult
from ai_testing_benchmark.core.result import PhaseResult, ResultStatus


class PerformanceEvaluator(BaseEvaluator):
    """
    Evaluator for AI system performance metrics.

    Tests:
    - Latency (P50, P95, P99)
    - Throughput (tokens/second)
    - Cost efficiency
    - Scalability
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
        """Evaluate a single performance test case."""
        start_time = time.time()

        category = test_case.get("category", "performance")
        test_id = test_case.get("id", "unknown")

        self.logger.info(f"Evaluating {test_id} ({category})")

        if category == "latency":
            result = self._evaluate_latency(test_case)
        elif category == "throughput":
            result = self._evaluate_throughput(test_case)
        elif category == "cost":
            result = self._evaluate_cost_efficiency(test_case)
        elif category == "scalability":
            result = self._evaluate_scalability(test_case)
        else:
            result = self._evaluate_generic_performance(test_case)

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

    def _evaluate_latency(self, test_case: Dict) -> Dict:
        """Evaluate response latency."""
        latencies = []
        num_requests = test_case.get("num_requests", 100)

        for _ in range(num_requests):
            request_start = time.time()
            self._call_model(test_case.get("prompt", "test"))
            request_end = time.time()
            latencies.append((request_end - request_start) * 1000)  # Convert to ms

        latencies = np.array(latencies)

        p50 = np.percentile(latencies, 50)
        p95 = np.percentile(latencies, 95)
        p99 = np.percentile(latencies, 99)

        thresholds = test_case.get("thresholds", {})
        p95_threshold = thresholds.get("p95_ms", 500)
        p99_threshold = thresholds.get("p99_ms", 1000)

        # Score based on threshold compliance
        p95_pass = p95 <= p95_threshold
        p99_pass = p99 <= p99_threshold

        score = 1.0 if (p95_pass and p99_pass) else 0.5

        return {
            "passed": score >= 0.85,
            "score": score,
            "metrics": {
                "latency_p50_ms": p50,
                "latency_p95_ms": p95,
                "latency_p99_ms": p99
            },
            "details": {
                "num_requests": num_requests,
                "mean_latency": np.mean(latencies),
                "std_latency": np.std(latencies)
            }
        }

    def _evaluate_throughput(self, test_case: Dict) -> Dict:
        """Evaluate throughput (tokens/second)."""
        total_tokens = 0
        total_time = 0
        num_requests = test_case.get("num_requests", 10)

        for _ in range(num_requests):
            request_start = time.time()
            response = self._call_model(test_case.get("prompt", "test"))
            request_end = time.time()

            total_time += (request_end - request_start)
            total_tokens += response.get("tokens", 100)

        tokens_per_second = total_tokens / total_time if total_time > 0 else 0

        threshold = test_case.get("min_throughput", 10)  # tokens/second

        score = min(1.0, tokens_per_second / threshold) if threshold > 0 else 0

        return {
            "passed": score >= 0.80,
            "score": score,
            "metrics": {
                "tokens_per_second": tokens_per_second,
                "total_tokens": total_tokens,
                "total_time_seconds": total_time
            },
            "details": {
                "num_requests": num_requests,
                "avg_tokens_per_request": total_tokens / num_requests if num_requests > 0 else 0
            }
        }

    def _evaluate_cost_efficiency(self, test_case: Dict) -> Dict:
        """Evaluate cost efficiency."""
        response = self._call_model(test_case.get("prompt", "test"))

        tokens_used = response.get("tokens", 100)
        cost_per_1k = test_case.get("cost_per_1k_tokens", 0.002)
        total_cost = (tokens_used / 1000) * cost_per_1k

        expected_cost = test_case.get("expected_cost", 0.01)

        cost_ratio = expected_cost / total_cost if total_cost > 0 else 0
        score = min(1.0, cost_ratio)

        return {
            "passed": score >= 0.80,
            "score": score,
            "metrics": {
                "cost_per_request": total_cost,
                "cost_efficiency_ratio": cost_ratio
            },
            "details": {
                "tokens_used": tokens_used,
                "cost_per_1k_tokens": cost_per_1k
            }
        }

    def _evaluate_scalability(self, test_case: Dict) -> Dict:
        """Evaluate scalability under load."""
        concurrency_levels = test_case.get("concurrency_levels", [1, 5, 10, 50])
        results = []

        for concurrency in concurrency_levels:
            start = time.time()
            # Simulate concurrent requests
            for _ in range(concurrency):
                self._call_model(test_case.get("prompt", "test"))
            elapsed = time.time() - start
            throughput = concurrency / elapsed if elapsed > 0 else 0
            results.append({"concurrency": concurrency, "throughput": throughput})

        # Check if throughput scales linearly
        base_throughput = results[0]["throughput"] if results else 1
        scalability_scores = []

        for r in results:
            expected_throughput = base_throughput * r["concurrency"]
            actual_throughput = r["throughput"]
            score = min(1.0, actual_throughput / expected_throughput) if expected_throughput > 0 else 0
            scalability_scores.append(score)

        avg_scalability = sum(scalability_scores) / len(scalability_scores) if scalability_scores else 0

        return {
            "passed": avg_scalability >= 0.70,
            "score": avg_scalability,
            "metrics": {
                "scalability_score": avg_scalability,
                "throughput_by_concurrency": {r["concurrency"]: r["throughput"] for r in results}
            },
            "details": {"scalability_results": results}
        }

    def _evaluate_generic_performance(self, test_case: Dict) -> Dict:
        """Generic performance evaluation."""
        return {
            "passed": False,
            "score": 0.0,
            "metrics": {},
            "details": {"error": "Unknown performance test type"}
        }

    def _call_model(self, prompt: str) -> Dict:
        """Call the model - placeholder."""
        return {"tokens": 100, "latency_ms": 50}

    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """Calculate aggregated performance scores."""
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

        # Weight latency more heavily
        weights = {"latency": 0.40, "throughput": 0.30, "cost": 0.15, "scalability": 0.15}

        overall = sum(
            avg_category_scores.get(cat, 0) * weights.get(cat, 0.2)
            for cat in set(list(avg_category_scores.keys()) + list(weights.keys()))
        )

        return {
            "overall_score": overall,
            "category_scores": avg_category_scores,
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results if r.passed)
        }

    def run_phase(self) -> PhaseResult:
        """Run complete performance evaluation phase."""
        phase_result = PhaseResult(phase="performance")

        test_cases = self._load_test_cases()

        self.logger.info(f"Running {len(test_cases)} performance tests")

        for test_case in test_cases:
            result = self.evaluate_single(test_case)
            phase_result.add_result(result)

        if phase_result.results:
            scores = [r.score for r in phase_result.results]
            phase_result.overall_score = sum(scores) / len(scores)

        return phase_result

    def _load_test_cases(self) -> List[Dict]:
        """Load performance test cases."""
        return [
            {
                "id": "TC-PERF-001",
                "category": "latency",
                "scenario_id": "LAT-001",
                "prompt": "What is cloud migration?",
                "num_requests": 50,
                "thresholds": {
                    "p95_ms": 500,
                    "p99_ms": 1000
                },
                "pass_threshold": 0.85
            },
            {
                "id": "TC-PERF-002",
                "category": "throughput",
                "scenario_id": "THR-001",
                "prompt": "Explain cloud migration strategies",
                "num_requests": 20,
                "min_throughput": 50,
                "pass_threshold": 0.80
            }
        ]

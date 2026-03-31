"""
Base evaluator class for all evaluation types.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import loguru


class EvaluationResult(BaseModel):
    """Container for evaluation results."""

    scenario_id: str
    test_case_id: str
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    metrics: Dict[str, float] = Field(default_factory=dict)
    details: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators in the benchmark framework.

    Subclasses must implement:
    - evaluate_single(): Evaluate a single test case
    - calculate_overall_score(): Aggregate results into overall score
    """

    def __init__(
        self,
        model_name: str,
        provider: str = "openai",
        config: Optional[Dict] = None,
        verbose: bool = False
    ):
        """
        Initialize base evaluator.

        Args:
            model_name: Name of the model to evaluate
            provider: Model provider (openai, anthropic, etc.)
            config: Optional configuration dictionary
            verbose: Enable verbose logging
        """
        self.model_name = model_name
        self.provider = provider
        self.config = config or {}
        self.verbose = verbose
        self.logger = loguru.logger

        if verbose:
            self.logger.enable("ai_testing_benchmark")
        else:
            self.logger.disable("ai_testing_benchmark")

    @abstractmethod
    def evaluate_single(self, test_case: Dict) -> EvaluationResult:
        """
        Evaluate a single test case.

        Args:
            test_case: Dictionary containing test case data

        Returns:
            EvaluationResult with scores and metadata
        """
        pass

    @abstractmethod
    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """
        Calculate overall score from individual results.

        Args:
            results: List of EvaluationResult objects

        Returns:
            Dictionary with aggregated scores
        """
        pass

    def run_evaluation(
        self,
        test_cases: List[Dict],
        stop_on_first_failure: bool = False,
        early_stopping_threshold: float = 0.5
    ) -> Dict:
        """
        Run evaluation on a list of test cases.

        Args:
            test_cases: List of test case dictionaries
            stop_on_first_failure: Stop if any test fails
            early_stopping_threshold: Threshold for early stopping

        Returns:
            Dictionary containing all results and summary
        """
        results = []
        failed_count = 0

        for i, test_case in enumerate(test_cases):
            self.logger.info(f"Evaluating test case {i+1}/{len(test_cases)}: {test_case.get('id', 'unknown')}")

            try:
                result = self.evaluate_single(test_case)
                results.append(result)

                if not result.passed:
                    failed_count += 1
                    self.logger.warning(f"Test case {test_case.get('id')} failed with score {result.score}")

                    if stop_on_first_failure:
                        self.logger.warning("Stopping due to first failure")
                        break

                    if failed_count / len(test_cases) > (1 - early_stopping_threshold):
                        self.logger.warning("Early stopping threshold reached")
                        break

            except Exception as e:
                self.logger.error(f"Error evaluating test case {test_case.get('id')}: {str(e)}")
                results.append(EvaluationResult(
                    scenario_id=test_case.get("scenario_id", "unknown"),
                    test_case_id=test_case.get("id", "unknown"),
                    passed=False,
                    score=0.0,
                    errors=[str(e)]
                ))

        summary = self.calculate_overall_score(results)

        return {
            "results": results,
            "summary": summary,
            "total_tests": len(test_cases),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed)
        }

    def _build_evaluation_prompt(self, test_case: Dict, system_prompt: Optional[str] = None) -> str:
        """
        Build prompt for evaluation.

        Args:
            test_case: Test case data
            system_prompt: Optional system prompt override

        Returns:
            Formatted prompt string
        """
        base_prompt = system_prompt or self.config.get("system_prompt", "")

        prompt_parts = [base_prompt]

        if "description" in test_case:
            prompt_parts.append(f"\n\nTask Description:\n{test_case['description']}")

        if "input" in test_case:
            if isinstance(test_case["input"], dict):
                prompt_parts.append(f"\n\nInput Data:\n{self._format_dict(test_case['input'])}")
            else:
                prompt_parts.append(f"\n\nInput:\n{test_case['input']}")

        if "question" in test_case:
            prompt_parts.append(f"\n\nQuestion:\n{test_case['question']}")

        return "\n\n".join(prompt_parts)

    def _format_dict(self, d: Dict, indent: int = 0) -> str:
        """Format dictionary for display in prompt."""
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{'  ' * indent}{key}:")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{'  ' * indent}{key}:")
                for item in value:
                    lines.append(f"{'  ' * (indent + 1)}- {item}")
            else:
                lines.append(f"{'  ' * indent}{key}: {value}")
        return "\n".join(lines)

    def _extract_model_response(self, raw_response: Any) -> str:
        """
        Extract text response from model output.

        Args:
            raw_response: Raw model response

        Returns:
            Extracted text string
        """
        if isinstance(raw_response, str):
            return raw_response
        elif isinstance(raw_response, dict):
            return raw_response.get("content", raw_response.get("text", str(raw_response)))
        elif hasattr(raw_response, "content"):
            return raw_response.content
        else:
            return str(raw_response)

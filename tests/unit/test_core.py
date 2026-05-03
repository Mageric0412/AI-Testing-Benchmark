"""
Unit tests for core module.
"""

import pytest
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig
from ai_testing_benchmark.core.result import EvaluationResult, PhaseResult, ResultStatus
from ai_testing_benchmark.core.metrics import MetricsCalculator


class TestConfig:
    """Tests for configuration management."""

    def test_default_config(self):
        """Test default configuration creation."""
        config = BenchmarkConfig(
            model=ModelConfig(name="gpt-4", provider="openai")
        )
        assert config.model.name == "gpt-4"
        assert config.model.provider == "openai"

    def test_phase_enabled(self):
        """Test phase enable/disable checking."""
        config = BenchmarkConfig(
            model=ModelConfig(name="gpt-4")
        )
        assert config.is_phase_enabled("foundation") is True
        assert config.is_phase_enabled("nonexistent") is False


class TestMetricsCalculator:
    """Tests for metrics calculations."""

    def test_accuracy(self):
        """Test accuracy calculation."""
        y_true = [1, 0, 1, 1, 0]
        y_pred = [1, 0, 1, 0, 0]
        accuracy = MetricsCalculator.accuracy(y_true, y_pred)
        assert accuracy == 0.8

    def test_f1_score(self):
        """Test F1 score calculation."""
        y_true = [1, 0, 1, 1, 0]
        y_pred = [1, 0, 1, 0, 0]
        f1 = MetricsCalculator.f1_score(y_true, y_pred)
        assert f1 > 0.7

    def test_rmse(self):
        """Test RMSE calculation."""
        y_true = [1.0, 2.0, 3.0, 4.0]
        y_pred = [1.1, 2.1, 2.9, 4.2]
        rmse = MetricsCalculator.rmse(y_true, y_pred)
        assert rmse < 0.3

    def test_aggregate_scores(self):
        """Test score aggregation."""
        scores = [0.8, 0.9, 0.7, 0.85]
        assert MetricsCalculator.aggregate_scores(scores, "mean") == pytest.approx(0.8125)
        assert MetricsCalculator.aggregate_scores(scores, "max") == 0.9
        assert MetricsCalculator.aggregate_scores(scores, "min") == 0.7


class TestEvaluationResult:
    """Tests for evaluation result handling."""

    def test_result_passed(self):
        """Test passed property."""
        result = EvaluationResult(
            test_case_id="test-001",
            test_case_name="Test Case",
            category="foundation",
            phase="foundation",
            status=ResultStatus.PASS,
            score=85.0,
            pass_threshold=80.0
        )
        assert result.passed is True
        assert result.failed is False

    def test_result_failed(self):
        """Test failed property."""
        result = EvaluationResult(
            test_case_id="test-001",
            test_case_name="Test Case",
            category="foundation",
            phase="foundation",
            status=ResultStatus.FAIL,
            score=70.0,
            pass_threshold=80.0
        )
        assert result.passed is False
        assert result.failed is True


class TestPhaseResult:
    """Tests for phase result aggregation."""

    def test_add_result(self):
        """Test adding results to phase."""
        phase = PhaseResult(phase="foundation")

        result1 = EvaluationResult(
            test_case_id="test-001",
            test_case_name="Test 1",
            category="foundation",
            phase="foundation",
            status=ResultStatus.PASS,
            score=85.0
        )

        result2 = EvaluationResult(
            test_case_id="test-002",
            test_case_name="Test 2",
            category="foundation",
            phase="foundation",
            status=ResultStatus.FAIL,
            score=70.0
        )

        phase.add_result(result1)
        phase.add_result(result2)

        assert phase.total_tests == 2
        assert phase.passed_tests == 1
        assert phase.failed_tests == 1
        assert phase.pass_rate == 50.0

    def test_pass_rate(self):
        """Test pass rate calculation."""
        phase = PhaseResult(phase="foundation")
        assert phase.pass_rate == 0.0

        for i in range(4):
            result = EvaluationResult(
                test_case_id=f"test-{i}",
                test_case_name=f"Test {i}",
                category="foundation",
                phase="foundation",
                status=ResultStatus.PASS,
                score=85.0
            )
            phase.add_result(result)

        assert phase.pass_rate == 100.0

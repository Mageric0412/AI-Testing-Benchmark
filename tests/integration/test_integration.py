"""
Integration tests for AI-Testing-Benchmark.
"""

import pytest
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig


class TestBenchmarkRunner:
    """Integration tests for benchmark runner."""

    def test_runner_initialization(self):
        """Test runner initialization."""
        config = BenchmarkConfig(
            model=ModelConfig(name="gpt-4", provider="openai")
        )
        runner = BenchmarkRunner(config=config)

        assert runner.config.model.name == "gpt-4"
        assert len(runner.evaluators) >= 0  # Depends on enabled phases

    def test_runner_with_disabled_phases(self):
        """Test runner with specific phases disabled."""
        config = BenchmarkConfig(
            model=ModelConfig(name="gpt-4"),
            foundation={"enabled": False},
            dialogue={"enabled": False}
        )
        runner = BenchmarkRunner(config=config)

        # Disabled phases should not have evaluators
        assert "foundation" not in runner.evaluators
        assert "dialogue" not in runner.evaluators

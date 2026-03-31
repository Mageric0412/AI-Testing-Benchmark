"""
AI-Testing-Benchmark
A comprehensive evaluation framework for AI-guided cloud migration journey systems.
"""

__version__ = "1.0.0"
__author__ = "AI Testing Team"

from ai_testing_benchmark.core.benchmark_runner import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig
from ai_testing_benchmark.core.result import EvaluationResult

__all__ = [
    "BenchmarkRunner",
    "BenchmarkConfig",
    "EvaluationResult",
]

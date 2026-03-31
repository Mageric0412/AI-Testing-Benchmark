"""
AI-Testing-Benchmark核心模块。
包含基础类、接口和通用工具。
"""

from ai_testing_benchmark.core.base_evaluator import BaseEvaluator
from ai_testing_benchmark.core.benchmark_runner import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig
from ai_testing_benchmark.core.result import EvaluationResult
from ai_testing_benchmark.core.metrics import MetricsCalculator

__all__ = [
    "BaseEvaluator",
    "BenchmarkRunner",
    "BenchmarkConfig",
    "EvaluationResult",
    "MetricsCalculator",
]

"""
AI-Testing-Benchmark
面向AI引导云迁移旅程系统的综合评估框架。
"""

__version__ = "1.0.0"
__author__ = "AI测试团队"

from ai_testing_benchmark.core.benchmark_runner import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig
from ai_testing_benchmark.core.result import EvaluationResult

__all__ = [
    "BenchmarkRunner",
    "BenchmarkConfig",
    "EvaluationResult",
]

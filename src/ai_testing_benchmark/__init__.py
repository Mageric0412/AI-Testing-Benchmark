"""
AI-Testing-Benchmark
面向AI引导云迁移旅程系统的综合评估框架。
"""

__version__ = "2.0.0"
__author__ = "AI测试团队"

from ai_testing_benchmark.core.benchmark_runner import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig
from ai_testing_benchmark.core.result import EvaluationResult
from ai_testing_benchmark.core.test_suite_loader import (
    TestSuiteLoader,
    load_test_suite,
    LoadedTestSuite,
    TestCase,
    Scenario
)
from ai_testing_benchmark.core.scoring_engine import (
    ScoringEngine,
    ScoreResult,
    ConfidenceLevel,
    ScoringConfig
)

__all__ = [
    "BenchmarkRunner",
    "BenchmarkConfig",
    "EvaluationResult",
    # Test Suite Loader
    "TestSuiteLoader",
    "load_test_suite",
    "LoadedTestSuite",
    "TestCase",
    "Scenario",
    # Scoring Engine
    "ScoringEngine",
    "ScoreResult",
    "ConfidenceLevel",
    "ScoringConfig",
]

"""
Standard benchmark definitions and configurations.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class Benchmark:
    """Container for benchmark information."""
    name: str
    description: str
    tasks: List[str]
    metrics: List[str]
    dataset_size: int
    expected_accuracy: float


class StandardBenchmarks:
    """
    Registry of standard benchmarks for foundation model evaluation.

    Based on industry standards including:
    - MMLU (Massive Multitask Language Understanding)
    - GSM8K (Grade School Math 8K)
    - HELM (Holistic Evaluation of Language Models)
    - BIG-Bench
    """

    BENCHMARKS: Dict[str, Benchmark] = {
        "mmlu": Benchmark(
            name="MMLU",
            description="Massive Multitask Language Understanding - 57 subjects",
            tasks=["multiple_choice"],
            metrics=["accuracy", "5-shot accuracy"],
            dataset_size=14079,
            expected_accuracy=0.70
        ),
        "gsm8k": Benchmark(
            name="GSM8K",
            description="Grade School Math 8K - 8.5K math word problems",
            tasks=["math_reasoning"],
            metrics=["accuracy", "pass@1", "pass@8"],
            dataset_size=8500,
            expected_accuracy=0.75
        ),
        "hellaswag": Benchmark(
            name="HellaSwag",
            description="Commonsense inference - 70K samples",
            tasks=["completion", "commonsense"],
            metrics=["accuracy", "10-shot accuracy"],
            dataset_size=70000,
            expected_accuracy=0.80
        ),
        "truthfulqa": Benchmark(
            name="TruthfulQA",
            description="Truthfulness evaluation - 817 questions",
            tasks=["question_answering", "truthfulness"],
            metrics=["mc1", "mc2"],
            dataset_size=817,
            expected_accuracy=0.50
        ),
        "winogrande": Benchmark(
            name="Winogrande",
            description="Commonsense reasoning - 40K samples",
            tasks=["commonsense", "fill-in-blank"],
            metrics=["accuracy", "5-shot accuracy"],
            dataset_size=40000,
            expected_accuracy=0.70
        ),
        "humaneval": Benchmark(
            name="HumanEval",
            description="Code generation - 164 problems",
            tasks=["code_generation"],
            metrics=["pass@1", "pass@10", "pass@100"],
            dataset_size=164,
            expected_accuracy=0.70
        ),
        "bigbench": Benchmark(
            name="BIG-Bench",
            description="Beyond the Imitation Game - 150+ tasks",
            tasks=["reasoning", "language_understanding", "generation"],
            metrics=["normalized_score", "ROUGE-L"],
            dataset_size=1000000,
            expected_accuracy=0.60
        )
    }

    # Custom cloud migration benchmarks
    CLOUD_MIGRATION_BENCHMARKS: Dict[str, Benchmark] = {
        "cloud_classification": Benchmark(
            name="Cloud Infrastructure Classification",
            description="Classify infrastructure descriptions into IaaS/PaaS/SaaS/CaaS/FaaS",
            tasks=["classification"],
            metrics=["accuracy", "f1_weighted"],
            dataset_size=500,
            expected_accuracy=0.88
        ),
        "dependency_resolution": Benchmark(
            name="Infrastructure Dependency Resolution",
            description="Resolve dependencies between cloud resources",
            tasks=["logical_reasoning"],
            metrics=["dependency_accuracy", "topology_correctness"],
            dataset_size=200,
            expected_accuracy=0.85
        ),
        "cost_estimation": Benchmark(
            name="Cloud Cost Estimation",
            description="Estimate cloud migration and operational costs",
            tasks=["calculation", "reasoning"],
            metrics=["prediction_accuracy", "error_rate"],
            dataset_size=300,
            expected_accuracy=0.90
        ),
        "migration_strategy": Benchmark(
            name="Migration Strategy Selection",
            description="Recommend appropriate migration strategies",
            tasks=["recommendation", "classification"],
            metrics=["recommendation_accuracy", "rationale_quality"],
            dataset_size=400,
            expected_accuracy=0.82
        ),
        "risk_assessment": Benchmark(
            name="Migration Risk Assessment",
            description="Identify and assess migration risks",
            tasks=["risk_identification", "severity_classification"],
            metrics=["risk_detection_rate", "false_positive_rate"],
            dataset_size=250,
            expected_accuracy=0.85
        )
    }

    @classmethod
    def get_benchmark(cls, name: str) -> Optional[Benchmark]:
        """Get benchmark by name."""
        return cls.BENCHMARKS.get(name.lower()) or cls.CLOUD_MIGRATION_BENCHMARKS.get(name.lower())

    @classmethod
    def list_benchmarks(cls, include_custom: bool = True) -> List[str]:
        """List all available benchmark names."""
        benchmarks = list(cls.BENCHMARKS.keys())
        if include_custom:
            benchmarks.extend(cls.CLOUD_MIGRATION_BENCHMARKS.keys())
        return benchmarks

    @classmethod
    def get_recommended_benchmark_suite(cls) -> List[str]:
        """
        Get recommended suite of benchmarks for comprehensive evaluation.

        Returns a balanced set of benchmarks covering different capabilities.
        """
        return [
            "mmlu",           # Knowledge
            "gsm8k",          # Mathematical reasoning
            "hellaswag",      # Commonsense reasoning
            "truthfulqa",     # Truthfulness
            "humaneval",      # Code generation
            "cloud_classification",  # Domain-specific
            "migration_strategy"     # Domain-specific
        ]

    @classmethod
    def get_quick_benchmark_suite(cls) -> List[str]:
        """Get quick benchmark suite for rapid iteration."""
        return [
            "mmlu",
            "gsm8k",
            "cloud_classification"
        ]

    @classmethod
    def get_full_benchmark_suite(cls) -> List[str]:
        """Get full benchmark suite for comprehensive evaluation."""
        return cls.list_benchmarks(include_custom=True)

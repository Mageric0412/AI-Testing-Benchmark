"""
Quick start example for AI-Testing-Benchmark.
"""

from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig


def main():
    """Run a quick benchmark."""
    # Create configuration
    config = BenchmarkConfig(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": "your-api-key"}
        )
    )

    # Initialize runner
    runner = BenchmarkRunner(config=config, verbose=True)

    # Run foundation evaluation only
    print("Running foundation model evaluation...")
    foundation_results = runner.run_phase("foundation")

    print(f"\nFoundation Phase Results:")
    print(f"  Score: {foundation_results.overall_score:.2f}")
    print(f"  Tests: {foundation_results.passed_tests}/{foundation_results.total_tests} passed")
    print(f"  Pass Rate: {foundation_results.pass_rate:.1f}%")

    return foundation_results


if __name__ == "__main__":
    main()

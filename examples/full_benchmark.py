"""
Full benchmark example with all phases.
"""

import os
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig


def main():
    """Run complete benchmark across all phases."""
    # Load configuration from environment or use defaults
    model_name = os.environ.get("AI_BENCHMARK_MODEL", "gpt-4")
    provider = os.environ.get("AI_BENCHMARK_PROVIDER", "openai")

    api_key = os.environ.get("OPENAI_API_KEY", "")

    config = BenchmarkConfig(
        model=ModelConfig(
            name=model_name,
            provider=provider,
            credentials={"api_key": api_key} if api_key else {}
        )
    )

    # Initialize runner
    runner = BenchmarkRunner(config=config, verbose=True)

    print(f"Starting benchmark for {model_name} ({provider})")
    print("=" * 60)

    # Run full benchmark
    report = runner.run_full_benchmark()

    # Print summary
    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)
    print(f"\nOverall Score: {report.overall_score:.2f}")
    print(f"Quality Gates: {'PASSED' if report.quality_gate_passed else 'FAILED'}")
    print(f"\nTotal Tests: {report.total_tests}")
    print(f"Passed: {report.total_passed}")
    print(f"Failed: {report.total_failed}")
    print(f"Critical Issues: {report.critical_issues}")
    print(f"High Issues: {report.high_issues}")

    print("\nPhase Scores:")
    for phase_name, phase_result in report.phases.items():
        status = "PASS" if phase_result.passed else "FAIL"
        print(f"  {phase_name}: {phase_result.overall_score:.2f} [{status}]")

    # Generate reports
    json_report = runner.generate_report(output_format="json")
    print(f"\nJSON report generated ({len(json_report)} chars)")

    # Save report
    runner.generate_report(
        output_format="json",
        output_path="./benchmark_results.json",
        include_raw=False
    )
    print("Report saved to ./benchmark_results.json")


if __name__ == "__main__":
    main()

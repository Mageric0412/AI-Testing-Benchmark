"""
Custom evaluation example - Cloud Migration specific.
"""

from ai_testing_benchmark.migration import CloudMigrationEvaluator
from ai_testing_benchmark.core.result import PhaseResult


def main():
    """Run cloud migration specific evaluation."""
    # Initialize evaluator
    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai",
        config={"phase": "assessment"},
        verbose=True
    )

    # Define custom test cases
    test_cases = [
        {
            "id": "MY-ASSESS-001",
            "phase": "assessment",
            "category": "infrastructure_discovery",
            "scenario_id": "CUSTOM-001",
            "input": {
                "description": """
                Enterprise infrastructure:
                - 500 servers across 3 data centers
                - VMware vSphere environment
                - 50TB SAN storage
                - 200 VMs running various workloads
                """
            },
            "expected_outputs": {
                "total_servers": {"value": 500, "tolerance": 0.05},
                "total_vms": {"value": 200, "tolerance": 0.1},
                "storage_identified": {"value": 50, "tolerance": 0.1}
            },
            "pass_threshold": 0.85
        },
        {
            "id": "MY-RISK-001",
            "phase": "assessment",
            "category": "risk_identification",
            "scenario_id": "CUSTOM-RISK-001",
            "input": {
                "description": """
                Financial services company:
                - Customer PII data stored in databases
                - PCI-DSS compliance required
                - 24/7 uptime requirement
                - Legacy COBOL systems integrated
                """
            },
            "expected_outputs": {
                "risks": {
                    "data_sovereignty": {"severity": "HIGH"},
                    "compliance": {"severity": "CRITICAL"},
                    "availability": {"severity": "HIGH"},
                    "legacy_integration": {"severity": "MEDIUM"}
                }
            },
            "pass_threshold": 0.80
        }
    ]

    # Run evaluation
    print("Running custom cloud migration evaluation...")
    results = evaluator.run_evaluation(test_cases)

    # Print results
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)

    for result in results["results"]:
        status = "PASS" if result.passed else "FAIL"
        print(f"\n{result.test_case_id}: {result.score:.2f}% [{status}]")

        if result.metrics:
            print("  Metrics:")
            for metric, value in result.metrics.items():
                print(f"    {metric}: {value:.4f}")

    print(f"\nSummary:")
    print(f"  Total: {results['total_tests']}")
    print(f"  Passed: {results['passed']}")
    print(f"  Failed: {results['failed']}")

    return results


if __name__ == "__main__":
    main()

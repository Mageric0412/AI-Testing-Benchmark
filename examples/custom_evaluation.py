"""
自定义评估示例 - 云迁移特定场景评估。

测试用例从 data/custom_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.migration import CloudMigrationEvaluator
from ai_testing_benchmark.core.result import PhaseResult


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "custom_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_enterprise_assessment():
    """示例1: 企业级基础设施评估"""
    print("=" * 60)
    print("示例1: 企业级基础设施评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "enterprise_assessment")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    passed = 0
    failed = 0
    for test_case in test_cases:
        result = evaluator.evaluate_single(test_case)
        if result.passed:
            passed += 1
        else:
            failed += 1
        status = "通过" if result.passed else "失败"
        print(f"\n{test_case['id']}: {result.score:.2f} [{status}]")

    print(f"\n总计: {len(test_cases)}")
    print(f"通过: {passed}")
    print(f"失败: {failed}")


def example_financial_risk():
    """示例2: 金融行业风险识别"""
    print("\n" + "=" * 60)
    print("示例2: 金融行业风险识别")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "financial_risk")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for test_case in test_cases:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}:")
        print(f"  分数: {result.score:.2f}")
        print(f"  状态: {'通过' if result.passed else '失败'}")
        if result.metrics:
            print("  指标:")
            for metric, value in result.metrics.items():
                print(f"    {metric}: {value:.4f}")


def example_cost_estimation_custom():
    """示例3: 自定义成本估算"""
    print("\n" + "=" * 60)
    print("示例3: 自定义成本估算")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "cost_estimation")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for test_case in test_cases:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}:")
        print(f"  分数: {result.score:.2f}")
        if result.metrics:
            print("  详细指标:")
            for metric, value in result.metrics.items():
                print(f"    {metric}: {value}")


def example_migration_strategy_custom():
    """示例4: 迁移策略自定义推荐"""
    print("\n" + "=" * 60)
    print("示例4: 迁移策略自定义推荐")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "migration_strategy")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for test_case in test_cases:
        result = evaluator.evaluate_single(test_case)
        status = "通过" if result.passed else "失败"
        print(f"\n测试 {test_case['id']}: {result.score:.2f} [{status}]")
        if result.metrics:
            print("  指标:")
            for metric, value in result.metrics.items():
                print(f"    {metric}: {value}")


def example_sequencing_optimization():
    """示例5: 迁移排序优化"""
    print("\n" + "=" * 60)
    print("示例5: 迁移排序优化")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "sequencing_optimization")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for test_case in test_cases:
        result = evaluator.evaluate_single(test_case)
        status = "通过" if result.passed else "失败"
        print(f"\n测试 {test_case['id']}: {result.score:.2f} [{status}]")


def main():
    """运行所有自定义评估示例。"""
    print("\n" + "=" * 60)
    print("自定义评估示例集")
    print("=" * 60)

    example_enterprise_assessment()
    example_financial_risk()
    example_cost_estimation_custom()
    example_migration_strategy_custom()
    example_sequencing_optimization()

    print("\n" + "=" * 60)
    print("所有示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
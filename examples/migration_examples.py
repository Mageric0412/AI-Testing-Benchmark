"""
云迁移评估示例 - 迁移旅程功能测试。

测试用例从 data/migration_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.migration import CloudMigrationEvaluator


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "migration_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_infrastructure_discovery():
    """示例1: 基础设施发现评估"""
    print("=" * 60)
    print("示例1: 基础设施发现评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "infrastructure_discovery")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_dependency_mapping():
    """示例2: 依赖关系映射评估"""
    print("\n" + "=" * 60)
    print("示例2: 依赖关系映射评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "dependency_mapping")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_cost_estimation():
    """示例3: 成本估算评估"""
    print("\n" + "=" * 60)
    print("示例3: 成本估算评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "cost_estimation")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_migration_strategy():
    """示例4: 迁移策略推荐评估"""
    print("\n" + "=" * 60)
    print("示例4: 迁移策略推荐评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "migration_strategy")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_risk_assessment():
    """示例5: 风险评估"""
    print("\n" + "=" * 60)
    print("示例5: 风险评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "risk_assessment")
    test_cases = category_data["test_cases"]

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_infrastructure_discovery()
    example_dependency_mapping()
    example_cost_estimation()
    example_migration_strategy()
    example_risk_assessment()
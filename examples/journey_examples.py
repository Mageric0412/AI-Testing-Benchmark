"""
云迁移旅程评估示例 - 评估云迁移调研智能助手的10个阶段能力。

测试用例从 data/journey_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.migration import CloudMigrationJourneyEvaluator


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "journey_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_resource_import():
    """示例1: 资源导入评估"""
    print("=" * 60)
    print("示例1: 资源导入评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "resource_import")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 资源导入")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_inventory_confirmation():
    """示例2: 资源清单确认评估"""
    print("\n" + "=" * 60)
    print("示例2: 资源清单确认评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "inventory_confirmation")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 资源清单确认")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_resource_summary():
    """示例3: 资源总结评估"""
    print("\n" + "=" * 60)
    print("示例3: 资源总结评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "resource_summary")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 资源总结")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_grouping_confirmation():
    """示例4: 分组确认评估"""
    print("\n" + "=" * 60)
    print("示例4: 分组确认评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "grouping_confirmation")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 分组确认")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_architecture_confirmation():
    """示例5: 架构确认评估"""
    print("\n" + "=" * 60)
    print("示例5: 架构确认评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "architecture_confirmation")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 架构确认")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_cloud_strategy():
    """示例6: 上云策略确认评估"""
    print("\n" + "=" * 60)
    print("示例6: 上云策略确认评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "cloud_strategy")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 上云策略确认")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_preference_confirmation():
    """示例7: 偏好确认评估"""
    print("\n" + "=" * 60)
    print("示例7: 偏好确认评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "preference_confirmation")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 偏好确认")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_specification_recommendation():
    """示例8: 规格推荐评估"""
    print("\n" + "=" * 60)
    print("示例8: 规格推荐评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "specification_recommendation")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 规格推荐")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_compatibility_task():
    """示例9: 主机数据库兼容性任务评估"""
    print("\n" + "=" * 60)
    print("示例9: 主机数据库兼容性任务评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "compatibility_task")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 主机数据库兼容性任务")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_report_generation():
    """示例10: 迁移报告生成评估"""
    print("\n" + "=" * 60)
    print("示例10: 迁移报告生成评估")
    print("=" * 60)

    data = load_test_cases()
    phase_data = next(p for p in data["phases"] if p["name"] == "report_generation")
    test_cases = phase_data["test_cases"]

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试: {tc['id']}")
        print(f"  阶段: 迁移报告生成")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {'是' if result.passed else '否'}")
        if result.metrics:
            print(f"  指标:")
            for metric, value in result.metrics.items():
                print(f"    - {metric}: {value:.2f}")

    return test_cases


def example_full_journey():
    """示例11: 完整旅程评估"""
    print("\n" + "=" * 60)
    print("示例11: 完整旅程评估 (所有10个阶段)")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    results = evaluator.run_phase()

    print(f"\n旅程评估完成:")
    print(f"  总测试数: {results.total_tests}")
    print(f"  通过数: {results.passed_tests}")
    print(f"  失败数: {results.failed_tests}")
    print(f"  总体分数: {results.overall_score:.2f}")

    return results


def main():
    """运行所有云迁移旅程评估示例。"""
    print("\n" + "=" * 60)
    print("云迁移旅程评估示例集")
    print("=" * 60)

    # 运行各阶段示例
    example_resource_import()
    example_inventory_confirmation()
    example_resource_summary()
    example_grouping_confirmation()
    example_architecture_confirmation()
    example_cloud_strategy()
    example_preference_confirmation()
    example_specification_recommendation()
    example_compatibility_task()
    example_report_generation()

    # 运行完整旅程评估
    example_full_journey()

    print("\n" + "=" * 60)
    print("所有旅程评估示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

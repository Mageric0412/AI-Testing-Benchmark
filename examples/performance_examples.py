"""
性能评估示例 - AI性能测试。

测试用例从 data/performance_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.performance import PerformanceEvaluator


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "performance_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_latency():
    """示例1: 延迟测试"""
    print("=" * 60)
    print("示例1: 延迟测试")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "latency")
    test_cases = category_data["test_cases"]

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_throughput():
    """示例2: 吞吐量测试"""
    print("\n" + "=" * 60)
    print("示例2: 吞吐量测试")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "throughput")
    test_cases = category_data["test_cases"]

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_cost_efficiency():
    """示例3: 成本效率测试"""
    print("\n" + "=" * 60)
    print("示例3: 成本效率测试")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "cost_efficiency")
    test_cases = category_data["test_cases"]

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_scalability():
    """示例4: 可扩展性测试"""
    print("\n" + "=" * 60)
    print("示例4: 可扩展性测试")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "scalability")
    test_cases = category_data["test_cases"]

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_consistency():
    """示例5: 一致性测试"""
    print("\n" + "=" * 60)
    print("示例5: 一致性测试")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "consistency")
    test_cases = category_data["test_cases"]

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_availability():
    """示例6: 可用性测试"""
    print("\n" + "=" * 60)
    print("示例6: 可用性测试")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "availability")
    test_cases = category_data["test_cases"]

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_latency()
    example_throughput()
    example_cost_efficiency()
    example_scalability()
    example_consistency()
    example_availability()
"""
安全评估示例 - AI安全性测试。

测试用例从 data/safety_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.safety import SafetyEvaluator


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "safety_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_prompt_injection():
    """示例1: 提示注入检测"""
    print("=" * 60)
    print("示例1: 提示注入检测")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "prompt_injection")
    test_cases = category_data["test_cases"]

    evaluator = SafetyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        blocked = not result.passed  # If it passed the safety check, it was blocked
        status = "✓ 拦截" if blocked else "✗ 未拦截"
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  结果: {status}")
        print(f"  分数: {result.score:.2f}")


def example_jailbreak():
    """示例2: 越狱攻击检测"""
    print("\n" + "=" * 60)
    print("示例2: 越狱攻击检测")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "jailbreak")
    test_cases = category_data["test_cases"]

    evaluator = SafetyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        blocked = not result.passed
        status = "✓ 拦截" if blocked else "✗ 未拦截"
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  结果: {status}")
        print(f"  分数: {result.score:.2f}")


def example_bias_detection():
    """示例3: 偏见检测"""
    print("\n" + "=" * 60)
    print("示例3: 偏见检测")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "bias")
    test_cases = category_data["test_cases"]

    evaluator = SafetyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_toxicity_detection():
    """示例4: 毒性检测"""
    print("\n" + "=" * 60)
    print("示例4: 毒性检测")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "toxicity")
    test_cases = category_data["test_cases"]

    evaluator = SafetyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_hallucination():
    """示例5: 幻觉检测"""
    print("\n" + "=" * 60)
    print("示例5: 幻觉检测")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "hallucination")
    test_cases = category_data["test_cases"]

    evaluator = SafetyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_data_privacy():
    """示例6: 数据隐私保护"""
    print("\n" + "=" * 60)
    print("示例6: 数据隐私保护")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "data_privacy")
    test_cases = category_data["test_cases"]

    evaluator = SafetyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}: {tc['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_prompt_injection()
    example_jailbreak()
    example_bias_detection()
    example_toxicity_detection()
    example_hallucination()
    example_data_privacy()
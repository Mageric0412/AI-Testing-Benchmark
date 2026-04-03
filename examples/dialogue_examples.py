"""
对话评估示例 - 对话AI能力测试。

测试用例从 data/dialogue_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.dialogue import DialogueEvaluator


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "dialogue_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_intent_recognition():
    """示例1: 意图识别评估"""
    print("=" * 60)
    print("示例1: 意图识别评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "intent_recognition")
    test_cases = category_data["test_cases"]

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n输入: {tc['user_utterance'][:40]}...")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_entity_extraction():
    """示例2: 实体提取评估"""
    print("\n" + "=" * 60)
    print("示例2: 实体提取评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "entity_extraction")
    test_cases = category_data["test_cases"]

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n输入: {tc['input'][:40]}...")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_dialogue_flow():
    """示例3: 对话流程评估"""
    print("\n" + "=" * 60)
    print("示例3: 对话流程评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "dialogue_flow")
    test_cases = category_data["test_cases"]

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n场景: {tc['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_response_quality():
    """示例4: 响应质量评估"""
    print("\n" + "=" * 60)
    print("示例4: 响应质量评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "response_quality")
    test_cases = category_data["test_cases"]

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n查询: {tc['query'][:40]}...")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_intent_recognition()
    example_entity_extraction()
    example_dialogue_flow()
    example_response_quality()

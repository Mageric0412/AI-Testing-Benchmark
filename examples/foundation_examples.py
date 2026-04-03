"""
基础模型评估示例 - 语言理解能力测试。

测试用例从 data/foundation_test_cases.json 动态加载。
"""

import json
from pathlib import Path
from ai_testing_benchmark.evaluation import FoundationModelEvaluator


def load_test_cases():
    """从配置加载测试用例"""
    data_path = Path(__file__).parent.parent / "data" / "foundation_test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def example_knowledge_qa():
    """示例1: 知识问答评估"""
    print("=" * 60)
    print("示例1: 知识问答评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "knowledge")
    test_cases = category_data["test_cases"]

    evaluator = FoundationModelEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n问题: {tc['question']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")

    return test_cases


def example_reasoning():
    """示例2: 推理能力评估"""
    print("\n" + "=" * 60)
    print("示例2: 推理能力评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "reasoning")
    test_cases = category_data["test_cases"]

    evaluator = FoundationModelEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n测试 {tc['id']}:")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")

    return test_cases


def example_classification():
    """示例3: 分类能力评估"""
    print("\n" + "=" * 60)
    print("示例3: 分类能力评估")
    print("=" * 60)

    data = load_test_cases()
    category_data = next(c for c in data["categories"] if c["name"] == "classification")
    test_cases = category_data["test_cases"]

    evaluator = FoundationModelEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    for tc in test_cases:
        result = evaluator.evaluate_single(tc)
        print(f"\n分类任务 {tc['id']}:")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")

    return test_cases


def main():
    """运行所有基础模型评估示例"""
    print("\n" + "=" * 60)
    print("基础模型评估示例集")
    print("=" * 60)

    example_knowledge_qa()
    example_reasoning()
    example_classification()

    print("\n" + "=" * 60)
    print("所有基础评估示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
基础模型评估示例 - 语言理解能力测试。
"""

import os
from ai_testing_benchmark.evaluation import FoundationModelEvaluator


def example_knowledge_qa():
    """示例1: 知识问答评估"""
    print("=" * 60)
    print("示例1: 知识问答评估")
    print("=" * 60)

    evaluator = FoundationModelEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    # 知识问答测试
    test_cases = [
        {
            "id": "KNOW-001",
            "category": "knowledge",
            "question": "AWS定义的6种云迁移策略是什么？",
            "expected_topics": ["重新托管", "重新平台化", "重构", "重新购买", "淘汰", "保留"]
        },
        {
            "id": "KNOW-002",
            "category": "knowledge",
            "question": "什么是RTO和RPO？它们有什么区别？",
            "expected_topics": ["RTO", "RPO", "恢复时间目标", "恢复点目标", "业务连续性"]
        },
        {
            "id": "KNOW-003",
            "category": "knowledge",
            "question": "解释一下Kubernetes的核心组件及其作用。",
            "expected_topics": ["kube-apiserver", "etcd", "kubelet", "container-runtime", "controller"]
        }
    ]

    for test_case in test_cases:
        result = evaluator.evaluate_single(test_case)
        print(f"\n问题: {test_case['question']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_reasoning():
    """示例2: 推理能力评估"""
    print("\n" + "=" * 60)
    print("示例2: 推理能力评估")
    print("=" * 60)

    evaluator = FoundationModelEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    # 推理测试用例
    reasoning_tests = [
        {
            "id": "REASON-001",
            "category": "reasoning",
            "task": "如果一个EC2实例成本为$0.10/小时，运行10个实例24/7一个月（30天）需要多少钱？",
            "expected_steps": ["计算每天成本", "计算每月成本", "考虑可能的节省"]
        },
        {
            "id": "REASON-002",
            "category": "reasoning",
            "task": "一家公司有100台虚拟机，平均利用率45%。迁移到云端后，预计可以节省多少成本？",
            "expected_analysis": ["当前成本分析", "云端成本估算", "优化建议"]
        },
        {
            "id": "REASON-003",
            "category": "reasoning",
            "task": "分析以下迁移场景的风险：3层架构应用，数据库在本地，需要零停机迁移。",
            "expected_risks": ["数据同步风险", "连接切换风险", "回滚风险"]
        }
    ]

    for test_case in reasoning_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}:")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_classification():
    """示例3: 分类能力评估"""
    print("\n" + "=" * 60)
    print("示例3: 分类能力评估")
    print("=" * 60)

    evaluator = FoundationModelEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    # 分类测试
    classification_tasks = [
        {
            "id": "CLASS-001",
            "category": "language_understanding",
            "task_type": "classification",
            "task": "将以下工作负载分类为高/中/低优先级迁移：\n1. 客户-facing电商网站\n2. 内部文档管理系统\n3. 核心支付处理系统",
            "categories": ["高优先级", "中优先级", "低优先级"],
            "expected": {
                "电商网站": "高优先级",
                "文档管理": "中优先级",
                "支付处理": "高优先级"
            }
        },
        {
            "id": "CLASS-002",
            "category": "language_understanding",
            "task_type": "classification",
            "task": "将以下问题分类为：迁移策略、成本问题、安全问题、性能问题\n1. '我们的RDS实例成本太高'\n2. '迁移后应用响应变慢'\n3. '如何确保PCI-DSS合规'",
            "categories": ["迁移策略", "成本问题", "安全问题", "性能问题"],
            "expected": {
                "RDS成本": "成本问题",
                "响应变慢": "性能问题",
                "PCI-DSS": "安全问题"
            }
        }
    ]

    for test_case in classification_tasks:
        result = evaluator.evaluate_single(test_case)
        print(f"\n分类任务 {test_case['id']}:")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_knowledge_qa()
    example_reasoning()
    example_classification()
"""
性能评估示例 - AI性能测试。
"""

import os
import time
from ai_testing_benchmark.performance import PerformanceEvaluator


def example_latency():
    """示例1: 延迟测试"""
    print("=" * 60)
    print("示例1: 延迟测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    latency_tests = [
        {
            "id": "LAT-001",
            "category": "latency",
            "name": "简单问答延迟",
            "query": "什么是云迁移？",
            "expected_max_latency_ms": 5000
        },
        {
            "id": "LAT-002",
            "category": "latency",
            "name": "复杂分析延迟",
            "query": """
            分析以下迁移场景：
            - 100台虚拟机
            - 50TB数据
            - 零停机要求
            - 2周内完成

            请提供详细的迁移计划，包括风险评估和资源需求。
            """,
            "expected_max_latency_ms": 30000
        },
        {
            "id": "LAT-003",
            "category": "latency",
            "name": "批量评估延迟",
            "query": "什么是IaaS?",
            "expected_max_latency_ms": 5000
        }
    ]

    for test_case in latency_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_throughput():
    """示例2: 吞吐量测试"""
    print("\n" + "=" * 60)
    print("示例2: 吞吐量测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    throughput_tests = [
        {
            "id": "THRU-001",
            "category": "throughput",
            "name": "并发请求测试",
            "concurrent_requests": 10,
            "duration_seconds": 60,
            "test_query": "解释容器化技术"
        },
        {
            "id": "THRU-002",
            "category": "throughput",
            "name": "持续负载测试",
            "concurrent_requests": 5,
            "duration_seconds": 120,
            "test_query": "什么是云原生?"
        }
    ]

    for test_case in throughput_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_cost_efficiency():
    """示例3: 成本效率测试"""
    print("\n" + "=" * 60)
    print("示例3: 成本效率测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    cost_tests = [
        {
            "id": "COST-001",
            "category": "cost_efficiency",
            "name": "基础模型成本比较",
            "models": [
                {"name": "gpt-4", "provider": "openai"},
                {"name": "gpt-3.5-turbo", "provider": "openai"}
            ],
            "test_queries": [
                "什么是云迁移?",
                "AWS的EC2有哪些实例类型?"
            ],
            "evaluation_metric": "cost_per_accuracy"
        },
        {
            "id": "COST-002",
            "category": "cost_efficiency",
            "name": "大批量处理成本",
            "model": {"name": "gpt-3.5-turbo", "provider": "openai"},
            "batch_size": 100,
            "test_scenario": "产品描述分类",
            "expected_cost_per_1k": 1.00
        }
    ]

    for test_case in cost_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_scalability():
    """示例4: 可扩展性测试"""
    print("\n" + "=" * 60)
    print("示例4: 可扩展性测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    scalability_tests = [
        {
            "id": "SCALE-001",
            "category": "scalability",
            "name": "并发扩展测试",
            "load_levels": [1, 5, 10, 20, 50],
            "duration_per_level": 30,
            "test_query": "解释云架构设计模式"
        },
        {
            "id": "SCALE-002",
            "category": "scalability",
            "name": "上下文长度扩展",
            "context_sizes": [1_000, 5_000, 10_000, 20_000],
            "test_scenario": "长文档分析",
            "expected_linear_scaling": True
        }
    ]

    for test_case in scalability_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_consistency():
    """示例5: 一致性测试"""
    print("\n" + "=" * 60)
    print("示例5: 一致性测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    consistency_tests = [
        {
            "id": "CONS-001",
            "category": "consistency",
            "name": "相同输入一致性",
            "query": "AWS的S3是什么服务？请简要说明。",
            "repeat_count": 5,
            "temperature": 0.0
        },
        {
            "id": "CONS-002",
            "category": "consistency",
            "name": "确定性测试",
            "query": "1+1等于多少？",
            "repeat_count": 10,
            "temperature": 0.0
        },
        {
            "id": "CONS-003",
            "category": "consistency",
            "name": "创造性测试（应该有变化）",
            "query": "写一个关于云迁移的简短故事",
            "repeat_count": 5,
            "temperature": 0.9,
            "expected_variation": True
        }
    ]

    for test_case in consistency_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_availability():
    """示例6: 可用性测试"""
    print("\n" + "=" * 60)
    print("示例6: 可用性测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    availability_tests = [
        {
            "id": "AVAIL-001",
            "category": "availability",
            "name": "持续可用性监控",
            "duration_minutes": 10,
            "test_interval_seconds": 30,
            "test_query": "当前时间是什么？",
            "expected_availability": 0.99
        },
        {
            "id": "AVAIL-002",
            "category": "availability",
            "name": "错误恢复测试",
            "test_scenario": "模拟API限流场景",
            "retry_behavior": "exponential_backoff",
            "expected_recovery": True
        }
    ]

    for test_case in availability_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_latency()
    example_throughput()
    example_cost_efficiency()
    example_scalability()
    example_consistency()
    example_availability()
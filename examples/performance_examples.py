"""
性能评估示例 - AI性能测试。
"""

import os
import time
from ai_testing_benchmark.performance import PerformanceEvaluator
from ai_testing_benchmark.core.config import ModelConfig


def example_latency():
    """示例1: 延迟测试"""
    print("=" * 60)
    print("示例1: 延迟测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    latency_tests = [
        {
            "test_id": "LAT-001",
            "name": "简单问答延迟",
            "query": "什么是云迁移？",
            "expected_max_latency_ms": 5000
        },
        {
            "test_id": "LAT-002",
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
            "test_id": "LAT-003",
            "name": "批量评估延迟",
            "queries": [
                "什么是IaaS?",
                "什么是PaaS?",
                "什么是SaaS?",
                "AWS的S3是什么服务?",
                "Azure的Blob存储特点是什么?"
            ],
            "expected_max_latency_ms": 5000
        }
    ]

    results = evaluator.evaluate_latency(latency_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['name']}")
        print(f"  平均延迟: {result['avg_latency_ms']:.2f} ms")
        print(f"  P50延迟: {result['p50_latency_ms']:.2f} ms")
        print(f"  P95延迟: {result['p95_latency_ms']:.2f} ms")
        print(f"  P99延迟: {result['p99_latency_ms']:.2f} ms")
        print(f"  最大延迟: {result['max_latency_ms']:.2f} ms")
        status = "✓ 通过" if result['passed'] else "✗ 失败"
        print(f"  状态: {status}")


def example_throughput():
    """示例2: 吞吐量测试"""
    print("\n" + "=" * 60)
    print("示例2: 吞吐量测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    throughput_tests = [
        {
            "test_id": "THRU-001",
            "name": "并发请求测试",
            "concurrent_requests": 10,
            "duration_seconds": 60,
            "test_queries": [
                "解释容器化技术",
                "什么是Kubernetes?",
                "Docker和虚拟机有什么区别?",
                "描述微服务架构的优点",
                "什么是CI/CD?"
            ]
        },
        {
            "test_id": "THRU-002",
            "name": "持续负载测试",
            "concurrent_requests": 5,
            "duration_seconds": 120,
            "test_queries": [
                "什么是云原生?",
                "12-factor app是什么?",
                "解释DevOps理念"
            ]
        }
    ]

    results = evaluator.evaluate_throughput(throughput_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['name']}")
        print(f"  总请求数: {result['total_requests']}")
        print(f"  成功请求: {result['successful_requests']}")
        print(f"  失败请求: {result['failed_requests']}")
        print(f"  吞吐量: {result['throughput_rps']:.2f} 请求/秒")
        print(f"  错误率: {result['error_rate']:.2%}")
        print(f"  平均响应时间: {result['avg_response_time_ms']:.2f} ms")


def example_cost_efficiency():
    """示例3: 成本效率测试"""
    print("\n" + "=" * 60)
    print("示例3: 成本效率测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    cost_tests = [
        {
            "test_id": "COST-001",
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
            "test_id": "COST-002",
            "name": "大批量处理成本",
            "model": {"name": "gpt-3.5-turbo", "provider": "openai"},
            "batch_size": 100,
            "test_scenario": "产品描述分类",
            "expected_cost_per_1k: 1.00"
        }
    ]

    results = evaluator.evaluate_cost_efficiency(cost_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['name']}")
        if result.get('models_comparison'):
            print("  模型比较:")
            for model_name, metrics in result['models_comparison'].items():
                print(f"    {model_name}:")
                print(f"      成本: ${metrics['cost']:.4f}")
                print(f"      准确率: {metrics['accuracy']:.2%}")
                print(f"      成本效率: ${metrics['cost_per_accuracy']:.4f}/准确率")
        else:
            print(f"  总成本: ${result['total_cost']:.4f}")
            print(f"  每千次成本: ${result['cost_per_1k']:.4f}")
            print(f"  准确率: {result['accuracy']:.2%}")


def example_scalability():
    """示例4: 可扩展性测试"""
    print("\n" + "=" * 60)
    print("示例4: 可扩展性测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    scalability_tests = [
        {
            "test_id": "SCALE-001",
            "name": "并发扩展测试",
            "load_levels": [1, 5, 10, 20, 50],
            "duration_per_level": 30,
            "test_query": "解释云架构设计模式"
        },
        {
            "test_id": "SCALE-002",
            "name": "上下文长度扩展",
            "context_sizes": [1_000, 5_000, 10_000, 20_000],
            "test_scenario": "长文档分析",
            "expected_linear_scaling": True
        }
    ]

    results = evaluator.evaluate_scalability(scalability_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['name']}")
        print(f"  扩展系数: {result.get('scaling_factor', 'N/A')}")
        print(f"  线性度: {result.get('linearity', 0):.2f}")
        print(f"  性能退化: {result.get('performance_degradation', 0):.2%}")
        print("  负载级别数据:")
        for level, metrics in result.get('level_metrics', {}).items():
            print(f"    {level}: {metrics['throughput_rps']:.2f} RPS, {metrics['avg_latency_ms']:.2f} ms")


def example_consistency():
    """示例5: 一致性测试"""
    print("\n" + "=" * 60)
    print("示例5: 一致性测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    consistency_tests = [
        {
            "test_id": "CONS-001",
            "name": "相同输入一致性",
            "query": "AWS的S3是什么服务？请简要说明。",
            "repeat_count": 5,
            "temperature": 0.0
        },
        {
            "test_id": "CONS-002",
            "name": "确定性测试",
            "query": "1+1等于多少？",
            "repeat_count": 10,
            "temperature": 0.0
        },
        {
            "test_id": "CONS-003",
            "name": "创造性测试（应该有变化）",
            "query": "写一个关于云迁移的简短故事",
            "repeat_count": 5,
            "temperature": 0.9,
            "expected_variation": True
        }
    ]

    results = evaluator.evaluate_consistency(consistency_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['name']}")
        print(f"  一致性分数: {result['consistency_score']:.2f}")
        print(f"  响应变化度: {result.get('variation_score', 0):.2f}")
        print(f"  重复率: {result.get('repetition_rate', 0):.2%}")
        if result.get('identical_responses'):
            print(f"  完全相同响应数: {result['identical_responses']}/{result['total_responses']}")


def example_availability():
    """示例6: 可用性测试"""
    print("\n" + "=" * 60)
    print("示例6: 可用性测试")
    print("=" * 60)

    evaluator = PerformanceEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    availability_tests = [
        {
            "test_id": "AVAIL-001",
            "name": "持续可用性监控",
            "duration_minutes": 10,
            "test_interval_seconds": 30,
            "test_query": "当前时间是什么？",
            "expected_availability": 0.99
        },
        {
            "test_id": "AVAIL-002",
            "name": "错误恢复测试",
            "test_scenario": "模拟API限流场景",
            "retry_behavior": "exponential_backoff",
            "expected_recovery": True
        }
    ]

    results = evaluator.evaluate_availability(availability_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['name']}")
        print(f"  可用性: {result['availability']:.2%}")
        print(f"  成功请求: {result['successful_requests']}/{result['total_requests']}")
        print(f"  平均恢复时间: {result.get('mean_recovery_time_ms', 0):.2f} ms")
        print(f"  SLA达标: {'是' if result.get('sla_met') else '否'}")


if __name__ == "__main__":
    example_latency()
    example_throughput()
    example_cost_efficiency()
    example_scalability()
    example_consistency()
    example_availability()

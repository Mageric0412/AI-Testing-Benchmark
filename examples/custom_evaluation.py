"""
自定义评估示例 - 云迁移特定场景评估。
"""

import os
from ai_testing_benchmark.migration import CloudMigrationEvaluator
from ai_testing_benchmark.core.config import ModelConfig
from ai_testing_benchmark.core.result import PhaseResult


def example_enterprise_assessment():
    """示例1: 企业级基础设施评估"""
    print("=" * 60)
    print("示例1: 企业级基础设施评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    # 自定义测试用例
    test_cases = [
        {
            "id": "MY-ASSESS-001",
            "phase": "assessment",
            "category": "infrastructure_discovery",
            "scenario_id": "ENTERPRISE-001",
            "input": {
                "description": """
                企业级基础设施配置：
                - 3个数据中心，共500台服务器
                - VMware vSphere虚拟化环境
                - 50TB SAN存储
                - 200台运行各种工作负载的虚拟机
                - 15台数据库服务器
                - 10台负载均衡器
                """
            },
            "expected_outputs": {
                "total_servers": {"value": 500, "tolerance": 0.05},
                "total_vms": {"value": 200, "tolerance": 0.1},
                "storage_identified": {"value": 50, "tolerance": 0.1},
                "db_servers": {"value": 15, "tolerance": 0.2}
            },
            "pass_threshold": 0.85
        },
        {
            "id": "MY-ASSESS-002",
            "phase": "assessment",
            "category": "infrastructure_discovery",
            "scenario_id": "KUBERNETES-001",
            "input": {
                "description": """
                Kubernetes集群配置：
                - 生产集群：100节点，混合使用c5和m5实例
                - 预发布集群：20节点
                - 开发集群：10节点
                - 500个微服务
                - 每个微服务3-8个Pod
                - 使用Istio服务网格
                - Prometheus + Grafana监控
                """
            },
            "expected_outputs": {
                "total_nodes": {"value": 130, "tolerance": 0.1},
                "clusters": {"value": 3, "tolerance": 0},
                "services": {"value": 500, "tolerance": 0.15}
            },
            "pass_threshold": 0.80
        }
    ]

    results = evaluator.run_evaluation(test_cases)

    print(f"\n总计: {results['total_tests']}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")

    for result in results["results"]:
        status = "通过" if result.passed else "失败"
        print(f"\n{result.test_case_id}: {result.score:.2f}% [{status}]")


def example_financial_risk():
    """示例2: 金融行业风险识别"""
    print("\n" + "=" * 60)
    print("示例2: 金融行业风险识别")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    test_cases = [
        {
            "id": "MY-RISK-001",
            "phase": "assessment",
            "category": "risk_identification",
            "scenario_id": "FINANCE-RISK-001",
            "input": {
                "description": """
                金融服务公司云迁移项目：

                数据资产：
                - 客户PII数据（姓名、身份证、银行账户）
                - 交易记录（每日500万笔）
                - 监管报告数据

                合规要求：
                - PCI-DSS 1级认证
                - SOX合规
                - GDPR（针对欧盟客户）
                - 数据必须保留在中国境内

                业务需求：
                - 7x24小时可用性
                - 零数据丢失要求
                - 与现有核心系统集成
                """
            },
            "expected_outputs": {
                "risks": {
                    "data_sovereignty": {"severity": "高"},
                    "compliance": {"severity": "严重"},
                    "availability": {"severity": "高"},
                    "integration": {"severity": "中"}
                }
            },
            "pass_threshold": 0.80
        }
    ]

    results = evaluator.run_evaluation(test_cases)

    for result in results["results"]:
        print(f"\n测试 {result.test_case_id}:")
        print(f"  分数: {result.score:.2%}")
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

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    test_cases = [
        {
            "id": "MY-COST-001",
            "phase": "assessment",
            "category": "cost_estimation",
            "scenario_id": "COST-CUSTOM-001",
            "input": {
                "workload": {
                    "web_servers": 30,
                    "web_spec": "c5.large",
                    "app_servers": 40,
                    "app_spec": "c5.xlarge",
                    "db_servers": 10,
                    "db_spec": "r5.2xlarge",
                    "storage_gb": 10000,
                    "monthly_data_transfer_gb": 5000
                },
                "current_monthly_cost": "$80,000（本地数据中心）",
                "target_provider": "AWS",
                "migration_type": "lift_and_shift"
            },
            "expected_outputs": {
                "estimated_monthly_cost": {
                    "min": 45000,
                    "max": 65000
                },
                "year_one_cost": {
                    "min": 600000,
                    "max": 850000
                },
                "breakdown_required": ["计算", "存储", "数据传输"]
            },
            "pass_threshold": 0.75
        }
    ]

    results = evaluator.run_evaluation(test_cases)

    for result in results["results"]:
        print(f"\n测试 {result.test_case_id}:")
        print(f"  分数: {result.score:.2%}")
        if result.metrics:
            print("  详细指标:")
            for metric, value in result.metrics.items():
                print(f"    {metric}: {value}")


def example_migration_strategy_custom():
    """示例4: 迁移策略自定义推荐"""
    print("\n" + "=" * 60)
    print("示例4: 迁移策略自定义推荐")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    test_cases = [
        {
            "id": "MY-STRAT-001",
            "phase": "planning",
            "category": "strategy_recommendation",
            "scenario_id": "STRAT-CUSTOM-001",
            "input": {
                "application": {
                    "name": "订单处理系统",
                    "age_years": 8,
                    "tech_stack": "Java 8, Spring MVC, Oracle 11g",
                    "architecture": "单体",
                    "change_frequency": "每周",
                    "technical_debt": "中",
                    "team_familiarity": "高",
                    "business_criticality": "关键",
                    "scaling_needs": "高",
                    "customizations": "大量",
                    "dependencies": ["支付网关", "库存系统", "物流API"]
                }
            },
            "expected_outputs": {
                "recommended_strategy": "重构",
                "rationale_required": True,
                "timeline_months": {"min": 6, "max": 12}
            },
            "pass_threshold": 0.80
        },
        {
            "id": "MY-STRAT-002",
            "phase": "planning",
            "category": "strategy_recommendation",
            "scenario_id": "STRAT-CUSTOM-002",
            "input": {
                "application": {
                    "name": "内部文档管理系统",
                    "age_years": 3,
                    "tech_stack": "Node.js, React, MongoDB",
                    "architecture": "微服务",
                    "change_frequency": "每天",
                    "technical_debt": "低",
                    "team_familiarity": "高",
                    "business_criticality": "低",
                    "scaling_needs": "中",
                    "customizations": "最少"
                }
            },
            "expected_outputs": {
                "recommended_strategy": "重新托管",
                "rationale_required": True
            },
            "pass_threshold": 0.75
        }
    ]

    results = evaluator.run_evaluation(test_cases)

    for result in results["results"]:
        status = "通过" if result.passed else "失败"
        print(f"\n测试 {result.test_case_id}: {result.score:.2%} [{status}]")
        if result.metrics:
            print("  指标:")
            for metric, value in result.metrics.items():
                print(f"    {metric}: {value}")


def example_sequencing_optimization():
    """示例5: 迁移排序优化"""
    print("\n" + "=" * 60)
    print("示例5: 迁移排序优化")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    test_cases = [
        {
            "id": "MY-SEQ-001",
            "phase": "planning",
            "category": "sequencing_optimization",
            "scenario_id": "SEQ-CUSTOM-001",
            "input": {
                "applications": [
                    {"id": "APP-001", "name": "用户认证", "dependencies": [], "risk": "低", "business_priority": 1},
                    {"id": "APP-002", "name": "产品目录", "dependencies": [], "risk": "低", "business_priority": 2},
                    {"id": "APP-003", "name": "搜索服务", "dependencies": ["APP-002"], "risk": "中", "business_priority": 3},
                    {"id": "APP-004", "name": "购物车", "dependencies": ["APP-001", "APP-003"], "risk": "中", "business_priority": 4},
                    {"id": "APP-005", "name": "订单处理", "dependencies": ["APP-001", "APP-004"], "risk": "高", "business_priority": 5},
                    {"id": "APP-006", "name": "支付服务", "dependencies": ["APP-001"], "risk": "严重", "business_priority": 6}
                ],
                "constraints": {
                    "max_concurrent_migrations": 2,
                    "team_capacity": 5,
                    "must_complete_by": "6个月"
                }
            },
            "expected_outputs": {
                "valid_sequence": True,
                "dependency_respected": True,
                "constraint_satisfied": True,
                "estimated_duration_months": {"min": 4, "max": 7}
            },
            "pass_threshold": 0.85
        }
    ]

    results = evaluator.run_evaluation(test_cases)

    for result in results["results"]:
        status = "通过" if result.passed else "失败"
        print(f"\n测试 {result.test_case_id}: {result.score:.2%} [{status}]")
        if result.get('sequence'):
            print(f"  建议序列: {result['sequence']}")


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

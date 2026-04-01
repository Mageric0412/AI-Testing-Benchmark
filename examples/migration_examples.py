"""
云迁移评估示例 - 迁移旅程功能测试。
"""

import os
from ai_testing_benchmark.migration import CloudMigrationEvaluator


def example_infrastructure_discovery():
    """示例1: 基础设施发现评估"""
    print("=" * 60)
    print("示例1: 基础设施发现评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    discovery_tests = [
        {
            "id": "DISC-001",
            "category": "assessment",
            "scenario_name": "中型企业基础设施",
            "description": """
            我们的IT基础设施包括：
            - 2个数据中心（上海主站，北京灾备）
            - 80台物理服务器（50台Linux，30台Windows）
            - 120台VMware虚拟机
            - 6台数据库服务器（3台MySQL，2台SQL Server，1台PostgreSQL）
            - 10台应用服务器（Java Spring Boot）
            - 5台负载均衡器（F5）
            - 25台网络设备（交换机和路由器）
            """,
            "expected_outputs": {
                "total_servers": 80,
                "vm_count": 120,
                "db_count": 6,
                "load_balancers": 5
            }
        },
        {
            "id": "DISC-002",
            "category": "assessment",
            "scenario_name": "微服务架构",
            "description": """
            我们的系统运行在Kubernetes上：
            - 3个集群（生产环境50节点，预发布10节点，开发5节点）
            - 约150个微服务
            - 每个服务2-8个Pod
            - 使用Istio服务网格
            - Harbor作为容器仓库
            - Kafka消息队列
            """,
            "expected_outputs": {
                "clusters": 3,
                "total_nodes": 65,
                "services_identified": 150
            }
        }
    ]

    for test_case in discovery_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_dependency_mapping():
    """示例2: 依赖关系映射评估"""
    print("\n" + "=" * 60)
    print("示例2: 依赖关系映射评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    dependency_tests = [
        {
            "id": "DEPM-001",
            "category": "assessment",
            "scenario_name": "三层Web应用依赖",
            "architecture": """
            Web层: React SPA -> Nginx -> S3/CloudFront
            应用层: API Gateway -> [用户服务, 产品服务, 订单服务, 支付服务]
            数据层: PostgreSQL -> Redis缓存 -> S3存储
            消息队列: RabbitMQ -> 异步处理
            """,
            "known_dependencies": [
                "Web -> API Gateway",
                "API Gateway -> 用户服务",
                "API Gateway -> 产品服务",
                "API Gateway -> 订单服务",
                "API Gateway -> 支付服务",
                "订单服务 -> RabbitMQ",
                "支付服务 -> RabbitMQ",
                "产品服务 -> PostgreSQL",
                "用户服务 -> PostgreSQL",
                "订单服务 -> Redis"
            ]
        },
        {
            "id": "DEPM-002",
            "category": "assessment",
            "scenario_name": "遗留系统依赖",
            "architecture": """
            遗留ERP系统 (AS/400, COBOL) -> MQSeries -> 中间件
            现代CRM (Salesforce) -> API
            MES系统 -> REST API
            批处理作业 -> 文件共享 -> DB2
            """,
            "known_dependencies": [
                "ERP -> MQSeries",
                "MES -> API",
                "批处理 -> DB2"
            ]
        }
    ]

    for test_case in dependency_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_cost_estimation():
    """示例3: 成本估算评估"""
    print("\n" + "=" * 60)
    print("示例3: 成本估算评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    cost_tests = [
        {
            "id": "COST-001",
            "category": "assessment",
            "scenario_name": "中型企业AWS迁移",
            "workload": {
                "servers": 50,
                "types": {
                    "web_server": {"count": 20, "spec": "4 vCPU, 16GB"},
                    "app_server": {"count": 20, "spec": "8 vCPU, 32GB"},
                    "db_server": {"count": 5, "spec": "16 vCPU, 64GB"},
                    "cache_server": {"count": 5, "spec": "4 vCPU, 16GB"}
                },
                "storage_tb": 20,
                "monthly_data_transfer_tb": 5
            },
            "target_provider": "AWS",
            "expected_range": {
                "min_monthly": 25000,
                "max_monthly": 40000
            }
        },
        {
            "id": "COST-002",
            "category": "assessment",
            "scenario_name": "多提供商比较",
            "workload": {
                "ec2_instances": 30,
                "instance_type": "m5.large",
                "storage_gb": 5000,
                "monthly_hours": 730
            },
            "providers": ["AWS", "Azure", "GCP"],
            "expected": {
                "provider_identified": True,
                "cost_range_accurate": True
            }
        }
    ]

    for test_case in cost_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_migration_strategy():
    """示例4: 迁移策略推荐评估"""
    print("\n" + "=" * 60)
    print("示例4: 迁移策略推荐评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    strategy_tests = [
        {
            "id": "STRAT-001",
            "category": "planning",
            "scenario_name": "遗留ERP系统",
            "application": {
                "name": "企业ERP系统",
                "age_years": 12,
                "tech_stack": "Java 6, WebLogic, Oracle",
                "architecture": "单体",
                "change_frequency": "季度",
                "technical_debt": "高",
                "team_familiarity": "低",
                "business_criticality": "关键"
            },
            "expected_strategy": "重构"
        },
        {
            "id": "STRAT-002",
            "category": "planning",
            "scenario_name": "现代化微服务",
            "application": {
                "name": "客户门户",
                "age_years": 2,
                "tech_stack": "Node.js, React, PostgreSQL",
                "architecture": "微服务",
                "change_frequency": "每周",
                "technical_debt": "低",
                "team_familiarity": "高",
                "business_criticality": "高"
            },
            "expected_strategy": "重新托管"
        },
        {
            "id": "STRAT-003",
            "category": "planning",
            "scenario_name": "传统批处理",
            "application": {
                "name": "工资处理系统",
                "age_years": 20,
                "tech_stack": "COBOL, JCL, VSAM",
                "architecture": "大型机",
                "change_frequency": "极少",
                "technical_debt": "中",
                "team_familiarity": "非常低",
                "business_criticality": "中"
            },
            "expected_strategy": "重新购买或淘汰"
        }
    ]

    for test_case in strategy_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_risk_assessment():
    """示例5: 风险评估"""
    print("\n" + "=" * 60)
    print("示例5: 风险评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    risk_tests = [
        {
            "id": "RISK-001",
            "category": "assessment",
            "scenario_name": "金融数据迁移",
            "context": """
            公司：金融服务业
            数据类型：客户PII、交易数据
            合规要求：PCI-DSS、SOX、GDPR
            数据量：10PB
            零停机要求：是
            """,
            "expected_risk_categories": [
                "data_sovereignty",
                "compliance",
                "security",
                "downtime"
            ]
        },
        {
            "id": "RISK-002",
            "category": "assessment",
            "scenario_name": "遗留系统迁移",
            "context": """
            遗留系统：AS/400 + COBOL
            团队技能：5名COBOL开发人员，平均年龄55岁
            文档覆盖率：40%
            依赖关系：MQSeries, DB2, 平面文件
            """,
            "expected_risk_categories": [
                "skill_gaps",
                "technical_debt",
                "integration_complexity"
            ]
        }
    ]

    for test_case in risk_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n测试 {test_case['id']}: {test_case['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_infrastructure_discovery()
    example_dependency_mapping()
    example_cost_estimation()
    example_migration_strategy()
    example_risk_assessment()
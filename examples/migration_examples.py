"""
云迁移评估示例 - 迁移旅程功能测试。
"""

import os
from ai_testing_benchmark.migration import CloudMigrationEvaluator
from ai_testing_benchmark.core.config import ModelConfig


def example_infrastructure_discovery():
    """示例1: 基础设施发现评估"""
    print("=" * 60)
    print("示例1: 基础设施发现评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    discovery_tests = [
        {
            "test_id": "DISC-001",
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
            "test_id": "DISC-002",
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

    results = evaluator.evaluate_infrastructure_discovery(discovery_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['scenario_name']}")
        print(f"  发现率: {result['discovery_rate']:.2%}")
        print(f"  准确率: {result['accuracy']:.2%}")
        print(f"  误报率: {result['false_positive_rate']:.2%}")
        if result.get('missing_items'):
            print(f"  遗漏项: {result['missing_items']}")


def example_dependency_mapping():
    """示例2: 依赖关系映射评估"""
    print("\n" + "=" * 60)
    print("示例2: 依赖关系映射评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    dependency_tests = [
        {
            "test_id": "DEPM-001",
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
            "test_id": "DEPM-002",
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

    results = evaluator.evaluate_dependency_mapping(dependency_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['scenario_name']}")
        print(f"  依赖召回率: {result['recall']:.2%}")
        print(f"  依赖精确率: {result['precision']:.2%}")
        print(f"  循环检测: {'是' if result.get('cycle_detected') else '否'}")
        print(f"  关键路径识别: {'是' if result.get('critical_path_identified') else '否'}")


def example_cost_estimation():
    """示例3: 成本估算评估"""
    print("\n" + "=" * 60)
    print("示例3: 成本估算评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    cost_tests = [
        {
            "test_id": "COST-001",
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
            "test_id": "COST-002",
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

    results = evaluator.evaluate_cost_estimation(cost_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['scenario_name']}")
        print(f"  估算准确率: {result['accuracy']:.2%}")
        print(f"  分解准确率: {result.get('breakdown_accuracy', 0):.2%}")
        if result.get('estimated_monthly_cost'):
            print(f"  估算月成本: ${result['estimated_monthly_cost']:,.2f}")
        print(f"  优化建议数量: {result.get('optimization_count', 0)}")


def example_migration_strategy():
    """示例4: 迁移策略推荐评估"""
    print("\n" + "=" * 60)
    print("示例4: 迁移策略推荐评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    strategy_tests = [
        {
            "test_id": "STRAT-001",
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
            "test_id": "STRAT-002",
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
            "test_id": "STRAT-003",
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

    results = evaluator.evaluate_migration_strategy(strategy_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['scenario_name']}")
        print(f"  策略准确率: {result['strategy_accuracy']:.2%}")
        print(f"  推荐策略: {result['recommended_strategy']}")
        print(f"  预期策略: {result['expected_strategy']}")
        print(f"  理由质量: {result.get('rationale_quality', 0):.2f}")
        print(f"  理由: {result.get('rationale', 'N/A')}")


def example_risk_assessment():
    """示例5: 风险评估"""
    print("\n" + "=" * 60)
    print("示例5: 风险评估")
    print("=" * 60)

    evaluator = CloudMigrationEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    risk_tests = [
        {
            "test_id": "RISK-001",
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
            "test_id": "RISK-002",
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

    results = evaluator.evaluate_risk_assessment(risk_tests)

    for result in results:
        print(f"\n测试 {result['test_id']}: {result['scenario_name']}")
        print(f"  风险检测率: {result['detection_rate']:.2%}")
        print(f"  严重程度准确率: {result.get('severity_accuracy', 0):.2%}")
        print(f"  检测到的风险:")
        for risk in result.get('identified_risks', []):
            print(f"    - {risk['category']}: {risk['severity']}")


if __name__ == "__main__":
    example_infrastructure_discovery()
    example_dependency_mapping()
    example_cost_estimation()
    example_migration_strategy()
    example_risk_assessment()

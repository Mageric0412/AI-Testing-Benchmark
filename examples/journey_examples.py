"""
云迁移旅程评估示例 - 评估云迁移调研智能助手的10个阶段能力。
"""

from ai_testing_benchmark.migration import CloudMigrationJourneyEvaluator


def example_resource_import():
    """示例1: 资源导入评估"""
    print("=" * 60)
    print("示例1: 资源导入评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-001",
        "phase": evaluator.PHASE_RESOURCE_IMPORT,
        "scenario_id": "JOURNEY-001",
        "input": {
            "raw_description": """
            我公司有如下IT基础设施：
            - 50台Windows Server 2019虚拟机
            - 30台Ubuntu 22.04虚拟机
            - 20台CentOS 7服务器
            - 5台MySQL 5.7数据库服务器
            - 3台PostgreSQL 13数据库
            - 2台Oracle 19c数据库
            - 10台Nginx负载均衡器
            - 5TB NFS存储
            """
        },
        "expected_outputs": {
            "vm_count": 100,
            "os_types": ["Windows Server 2019", "Ubuntu 22.04", "CentOS 7"],
            "entities": ["MySQL", "PostgreSQL", "Oracle", "Nginx", "NFS"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 资源导入")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_inventory_confirmation():
    """示例2: 资源清单确认评估"""
    print("\n" + "=" * 60)
    print("示例2: 资源清单确认评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-002",
        "phase": evaluator.PHASE_INVENTORY_CONFIRM,
        "scenario_id": "JOURNEY-002",
        "input": {
            "inventory_data": {
                "vms": [
                    {"name": "WEB-01", "os": "Windows", "cpu": 4, "memory": 16},
                    {"name": "WEB-02", "os": "Windows", "cpu": 4, "memory": 16},
                    {"name": "DB-01", "os": "Linux", "cpu": 8, "memory": 32}
                ],
                "databases": [
                    {"name": "Oracle-ERP", "version": "19c", "size_tb": 2}
                ]
            }
        },
        "expected_outputs": {
            "confirmed_items": ["WEB-01", "WEB-02", "DB-01", "Oracle-ERP"],
            "completeness_rate": 1.0
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 资源清单确认")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_resource_summary():
    """示例3: 资源总结评估"""
    print("\n" + "=" * 60)
    print("示例3: 资源总结评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-003",
        "phase": evaluator.PHASE_RESOURCE_SUMMARY,
        "scenario_id": "JOURNEY-003",
        "input": {
            "resource_list": """
            共100台虚拟机：
            - 60台Web服务器 (Windows/Ubuntu)
            - 25台应用服务器 (CentOS)
            - 10台数据库服务器 (Oracle/MySQL/PostgreSQL)
            - 5台负载均衡器

            存储: 10TB SAN + 5TB NAS
            """
        },
        "expected_outputs": {
            "key_info": ["100台VM", "Web服务器", "应用服务器", "数据库", "负载均衡", "存储"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 资源总结")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_grouping_confirmation():
    """示例4: 分组确认评估"""
    print("\n" + "=" * 60)
    print("示例4: 分组确认评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-004",
        "phase": evaluator.PHASE_GROUPING_CONFIRM,
        "scenario_id": "JOURNEY-004",
        "input": {
            "resources": [
                {"id": "VM1", "type": "web", "dependencies": []},
                {"id": "VM2", "type": "web", "dependencies": []},
                {"id": "VM3", "type": "app", "dependencies": ["VM1", "VM2"]},
                {"id": "VM4", "type": "db", "dependencies": ["VM3"]}
            ]
        },
        "expected_outputs": {
            "groups": [
                {"name": "Web层", "resources": ["VM1", "VM2"]},
                {"name": "应用层", "resources": ["VM3"]},
                {"name": "数据层", "resources": ["VM4"]}
            ],
            "dependencies": ["VM3->VM1", "VM3->VM2", "VM4->VM3"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 分组确认")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_architecture_confirmation():
    """示例5: 架构确认评估"""
    print("\n" + "=" * 60)
    print("示例5: 架构确认评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-005",
        "phase": evaluator.PHASE_ARCHITECTURE_CONFIRM,
        "scenario_id": "JOURNEY-005",
        "input": {
            "workload_info": {
                "application_type": "三层Web应用",
                "traffic": "日均100万PV",
                "availability": "99.9%",
                "data_size_tb": 5
            }
        },
        "expected_outputs": {
            "recommended_architecture": "高可用架构",
            "components": ["ELB", "ASG", "RDS", "ElastiCache", "CloudWatch"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 架构确认")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_cloud_strategy():
    """示例6: 上云策略确认评估"""
    print("\n" + "=" * 60)
    print("示例6: 上云策略确认评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-006",
        "phase": evaluator.PHASE_CLOUD_STRATEGY,
        "scenario_id": "JOURNEY-006",
        "input": {
            "application_info": {
                "name": "企业ERP系统",
                "age_years": 8,
                "tech_stack": "Java 6, WebLogic, Oracle 11g",
                "architecture": "单体",
                "change_frequency": "季度",
                "business_criticality": "高"
            }
        },
        "expected_outputs": {
            "recommended_strategies": ["重构", "Replatform"],
            "rationale": "系统老旧但稳定，建议逐步重构"
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 上云策略确认")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_preference_confirmation():
    """示例7: 偏好确认评估"""
    print("\n" + "=" * 60)
    print("示例7: 偏好确认评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-007",
        "phase": evaluator.PHASE_PREFERENCE_CONFIRM,
        "scenario_id": "JOURNEY-007",
        "input": {
            "user_input": "我们希望迁移到AWS，首选成本优化方案，希望保留一定的控制权"
        },
        "expected_outputs": {
            "preferences": ["AWS", "成本优化", "保留控制权"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 偏好确认")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_specification_recommendation():
    """示例8: 规格推荐评估"""
    print("\n" + "=" * 60)
    print("示例8: 规格推荐评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-008",
        "phase": evaluator.PHASE_SPECIFICATION,
        "scenario_id": "JOURNEY-008",
        "input": {
            "workload_specs": {
                "app_type": "Web应用",
                "concurrent_users": 1000,
                "peak_cpu": "70%",
                "data_size_gb": 500
            }
        },
        "expected_outputs": {
            "recommended_specs": ["t3.large", "m5.large", "r5.xlarge"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 规格推荐")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_compatibility_task():
    """示例9: 主机数据库兼容性任务评估"""
    print("\n" + "=" * 60)
    print("示例9: 主机数据库兼容性任务评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-009",
        "phase": evaluator.PHASE_COMPATIBILITY,
        "scenario_id": "JOURNEY-009",
        "input": {
            "environment_info": {
                "source": "Oracle 19c on-premises",
                "target": "AWS RDS Oracle",
                "data_size_tb": 10
            }
        },
        "expected_outputs": {
            "compatibility_issues": ["字符集不兼容", "SQL语法差异"],
            "migration_paths": ["DMS", "S3+Glue"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 主机数据库兼容性任务")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_report_generation():
    """示例10: 迁移报告生成评估"""
    print("\n" + "=" * 60)
    print("示例10: 迁移报告生成评估")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    test_case = {
        "id": "TC-JOURNEY-010",
        "phase": evaluator.PHASE_REPORT,
        "scenario_id": "JOURNEY-010",
        "input": {
            "migration_data": {
                "resources": 100,
                "recommended_strategy": "分段迁移",
                "estimated_duration_months": 6,
                "estimated_cost_monthly": 50000
            }
        },
        "expected_outputs": {
            "required_sections": ["概述", "当前环境", "目标架构", "迁移策略", "时间线", "成本估算", "风险评估"],
            "recommendations": ["建议先迁移非关键系统", "建立回滚方案"]
        },
        "pass_threshold": 0.8
    }

    result = evaluator.evaluate_single(test_case)

    print(f"\n测试: {test_case['id']}")
    print(f"  阶段: 迁移报告生成")
    print(f"  分数: {result.score:.2f}")
    print(f"  通过: {'是' if result.passed else '否'}")
    print(f"  指标:")
    for metric, value in result.metrics.items():
        print(f"    - {metric}: {value:.2f}")

    return result


def example_full_journey():
    """示例11: 完整旅程评估"""
    print("\n" + "=" * 60)
    print("示例11: 完整旅程评估 (所有10个阶段)")
    print("=" * 60)

    evaluator = CloudMigrationJourneyEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    results = evaluator.run_phase()

    print(f"\n旅程评估完成:")
    print(f"  总测试数: {results.total_tests}")
    print(f"  通过数: {results.passed_tests}")
    print(f"  失败数: {results.failed_tests}")
    print(f"  总体分数: {results.overall_score:.2f}")

    return results


def main():
    """运行所有云迁移旅程评估示例。"""
    print("\n" + "=" * 60)
    print("云迁移旅程评估示例集")
    print("=" * 60)

    # 运行各阶段示例
    example_resource_import()
    example_inventory_confirmation()
    example_resource_summary()
    example_grouping_confirmation()
    example_architecture_confirmation()
    example_cloud_strategy()
    example_preference_confirmation()
    example_specification_recommendation()
    example_compatibility_task()
    example_report_generation()

    # 运行完整旅程评估
    example_full_journey()

    print("\n" + "=" * 60)
    print("所有旅程评估示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
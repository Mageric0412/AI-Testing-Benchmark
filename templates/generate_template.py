"""
生成测试套件XLSX模板。
"""

import sys
sys.path.insert(0, str(__file__.parent.parent / "src"))

from ai_testing_benchmark.core.test_suite_loader import TestSuiteLoader, TestCase, Scenario


def create_sample_test_suite() -> None:
    """创建示例测试套件并保存为XLSX。"""

    # 创建测试用例
    test_cases = [
        # 资源导入阶段测试用例
        TestCase(
            id="RI-001",
            scenario_id="SC-001",
            phase="resource_import",
            description="标准Excel资源清单导入，包含20+服务器信息",
            input={
                "file_format": "xlsx",
                "expected_fields": ["资源ID", "资源名称", "CPU", "内存", "操作系统"],
                "row_count": 25
            },
            expected_output={"status": "success", "parsed_count": 25},
            priority="P0",
            tags=["resource_import", "excel", "positive"]
        ),
        TestCase(
            id="RI-002",
            scenario_id="SC-001",
            phase="resource_import",
            description="CSV格式资源清单导入",
            input={"file_format": "csv", "row_count": 10},
            expected_output={"status": "success", "parsed_count": 10},
            priority="P0",
            tags=["resource_import", "csv", "positive"]
        ),
        TestCase(
            id="RI-003",
            scenario_id="SC-001",
            phase="resource_import",
            description="部分缺失字段的资源清单导入",
            input={"file_format": "xlsx", "missing_fields": ["操作系统版本"]},
            expected_output={"status": "partial", "warnings": ["缺少必填字段"]},
            priority="P1",
            tags=["resource_import", "validation", "negative"]
        ),

        # 资源清单确认阶段测试用例
        TestCase(
            id="IC-001",
            scenario_id="SC-002",
            phase="inventory_confirmation",
            description="混合类型资源（VM、物理机、容器）的分类确认",
            input={"resource_types": ["vm", "physical", "container"], "total_count": 50},
            expected_output={"correctly_classified": 50},
            priority="P0",
            tags=["classification", "mixed_workload"]
        ),
        TestCase(
            id="IC-002",
            scenario_id="SC-002",
            phase="inventory_confirmation",
            description="规格信息（CPU、内存、存储）的确认和修正",
            input={"spec_mismatch_rate": 0.1},
            expected_output={"corrections_applied": 5},
            priority="P1",
            tags=["specification", "correction"]
        ),

        # 资源总结阶段测试用例
        TestCase(
            id="RS-001",
            scenario_id="SC-003",
            phase="resource_summary",
            description="资源类型分布统计",
            input={"resource_distribution": {"vm": 60, "physical": 20, "container": 20}},
            expected_output={"charts_generated": ["pie", "bar"]},
            priority="P0",
            tags=["statistics", "visualization"]
        ),
        TestCase(
            id="RS-002",
            scenario_id="SC-003",
            phase="resource_summary",
            description="成本估算基础数据生成",
            input={"resources": []},
            expected_output={"cost_estimate": True},
            priority="P1",
            tags=["cost", "estimation"]
        ),

        # 分组与架构确认阶段测试用例
        TestCase(
            id="GA-001",
            scenario_id="SC-004",
            phase="grouping_architecture",
            description="按业务/Tier/依赖关系自动分组",
            input={"grouping_strategy": "auto", "resources": []},
            expected_output={"group_count": 5},
            priority="P0",
            tags=["grouping", "auto"]
        ),
        TestCase(
            id="GA-002",
            scenario_id="SC-004",
            phase="grouping_architecture",
            description="分组粒度调整（从粗粒度到细粒度）",
            input={"adjust_granularity": "increase", "current_groups": 3},
            expected_output={"adjusted_groups": 8},
            priority="P1",
            tags=["grouping", "adjustment"]
        ),
        TestCase(
            id="GA-006",
            scenario_id="SC-004",
            phase="grouping_architecture",
            description="目标架构推荐（IaaS/PaaS/SaaS）",
            input={"workload_types": ["web", "database", "cache"]},
            expected_output={"architecture": "cloud-native"},
            priority="P0",
            tags=["architecture", "recommendation"]
        ),

        # 上云策略确认阶段测试用例
        TestCase(
            id="CS-001",
            scenario_id="SC-005",
            phase="cloud_strategy",
            description="Rehost策略推荐（lift-and-shift）",
            input={"workload_type": "legacy_web", "constraints": []},
            expected_output={"recommended_strategy": "rehost"},
            priority="P0",
            tags=["strategy", "rehost", "legacy"]
        ),
        TestCase(
            id="CS-002",
            scenario_id="SC-005",
            phase="cloud_strategy",
            description="Replatform策略推荐",
            input={"workload_type": "database", "constraints": ["low_risk"]},
            expected_output={"recommended_strategy": "replatform"},
            priority="P0",
            tags=["strategy", "replatform"]
        ),
        TestCase(
            id="CS-003",
            scenario_id="SC-005",
            phase="cloud_strategy",
            description="成本效益分析",
            input={"strategy": "rehost", "resource_count": 100},
            expected_output={"roi_estimate": ">20%"},
            priority="P1",
            tags=["strategy", "cost", "roi"]
        ),

        # 规格推荐阶段测试用例
        TestCase(
            id="SP-001",
            scenario_id="SC-006",
            phase="spec_recommendation",
            description="Web服务器CPU规格推荐",
            input={"workload": "web_server", "traffic_level": "medium"},
            expected_output={"instance_type": "t3.large"},
            priority="P0",
            tags=["spec", "compute", "web"]
        ),
        TestCase(
            id="SP-002",
            scenario_id="SC-006",
            phase="spec_recommendation",
            description="数据库内存规格推荐",
            input={"workload": "database", "data_size": "1TB"},
            expected_output={"instance_type": "r5.xlarge"},
            priority="P0",
            tags=["spec", "memory", "database"]
        ),
        TestCase(
            id="SP-007",
            scenario_id="SC-006",
            phase="spec_recommendation",
            description="高可用配置推荐（多AZ部署）",
            input={"sla_requirement": "99.99%", "workload": "critical"},
            expected_output={"multi_az": True},
            priority="P1",
            tags=["spec", "ha", "multi_az"]
        ),

        # 兼容性评估阶段测试用例
        TestCase(
            id="CA-001",
            scenario_id="SC-007",
            phase="compatibility",
            description="大型机系统识别",
            input={"system_type": "ibm_mainframe"},
            expected_output={"detected": True, "model": "z15"},
            priority="P0",
            tags=["compatibility", "mainframe", "detection"]
        ),
        TestCase(
            id="CA-002",
            scenario_id="SC-007",
            phase="compatibility",
            description="Oracle数据库兼容性评分",
            input={"database_type": "oracle_19c", "workload": "oltp"},
            expected_output={"score": 3.5, "max_score": 5},
            priority="P0",
            tags=["compatibility", "oracle", "scoring"]
        ),
        TestCase(
            id="CA-003",
            scenario_id="SC-007",
            phase="compatibility",
            description="兼容性障碍识别",
            input={"database_type": "sql_server"},
            expected_output={"barriers": ["licensing", "version"]},
            priority="P1",
            tags=["compatibility", "barriers"]
        ),

        # 迁移报告生成阶段测试用例
        TestCase(
            id="MR-001",
            scenario_id="SC-008",
            phase="report_generation",
            description="执行摘要生成",
            input={"assessment_complete": True},
            expected_output={"executive_summary": True},
            priority="P0",
            tags=["report", "summary"]
        ),
        TestCase(
            id="MR-003",
            scenario_id="SC-008",
            phase="report_generation",
            description="目标架构章节生成",
            input={"architecture_recommendation": {}},
            expected_output={"architecture_chapter": True},
            priority="P0",
            tags=["report", "architecture"]
        ),
        TestCase(
            id="MR-012",
            scenario_id="SC-008",
            phase="report_generation",
            description="报告完整性检查",
            input={"report_draft": {}},
            expected_output={"completeness_score": ">95%"},
            priority="P0",
            tags=["report", "validation"]
        ),

        # 端到端集成测试用例
        TestCase(
            id="E2E-001",
            scenario_id="SC-009",
            phase="e2e",
            description="完整小规模迁移评估流程",
            input={"resource_count": 10, "complexity": "low"},
            expected_output={"report_complete": True, "stages_completed": 9},
            priority="P0",
            tags=["e2e", "full_flow", "smoke"]
        ),
        TestCase(
            id="E2E-004",
            scenario_id="SC-009",
            phase="e2e",
            description="传统主机迁移评估完整流程",
            input={"has_mainframe": True, "has_oracle": True},
            expected_output={"compatibility_assessment": True},
            priority="P0",
            tags=["e2e", "legacy", "mainframe"]
        ),
    ]

    # 创建场景
    scenarios = [
        Scenario(
            id="SC-001",
            name="资源导入测试",
            description="测试资源清单的导入和解析功能",
            test_case_ids=["RI-001", "RI-002", "RI-003"]
        ),
        Scenario(
            id="SC-002",
            name="资源清单确认测试",
            description="测试资源分类和确认功能",
            test_case_ids=["IC-001", "IC-002"]
        ),
        Scenario(
            id="SC-003",
            name="资源总结测试",
            description="测试统计分析和可视化功能",
            test_case_ids=["RS-001", "RS-002"]
        ),
        Scenario(
            id="SC-004",
            name="分组与架构确认测试",
            description="测试自动分组和架构推荐功能",
            test_case_ids=["GA-001", "GA-002", "GA-006"]
        ),
        Scenario(
            id="SC-005",
            name="上云策略确认测试",
            description="测试迁移策略推荐和评估功能",
            test_case_ids=["CS-001", "CS-002", "CS-003"]
        ),
        Scenario(
            id="SC-006",
            name="规格推荐测试",
            description="测试云资源规格推荐功能",
            test_case_ids=["SP-001", "SP-002", "SP-007"]
        ),
        Scenario(
            id="SC-007",
            name="兼容性评估测试",
            description="测试传统系统和数据库兼容性评估",
            test_case_ids=["CA-001", "CA-002", "CA-003"]
        ),
        Scenario(
            id="SC-008",
            name="报告生成测试",
            description="测试迁移报告生成功能",
            test_case_ids=["MR-001", "MR-003", "MR-012"]
        ),
        Scenario(
            id="SC-009",
            name="端到端集成测试",
            description="测试完整评估流程",
            test_case_ids=["E2E-001", "E2E-004"]
        ),
    ]

    # 创建测试套件
    from dataclasses import dataclass

    @dataclass
    class MockTestSuite:
        name: str
        version: str
        test_cases: list
        scenarios: list
        config: dict

    suite = MockTestSuite(
        name="Cloud Migration Assessment Test Suite v1.0",
        version="1.0.0",
        test_cases=test_cases,
        scenarios=scenarios,
        config={
            "pass_threshold": 0.80,
            "critical_threshold": 0.60,
            "phase_weights": {
                "resource_import": 0.10,
                "inventory_confirmation": 0.10,
                "resource_summary": 0.10,
                "grouping_architecture": 0.15,
                "cloud_strategy": 0.15,
                "spec_recommendation": 0.15,
                "compatibility": 0.15,
                "report_generation": 0.10
            }
        }
    )

    # 保存为XLSX
    loader = TestSuiteLoader()
    output_path = __file__.parent / "CloudMigration_TestSuite_Template.xlsx"
    loader.save_to_xlsx(suite, str(output_path))

    print(f"✓ 模板已生成: {output_path}")
    print(f"  - 测试用例: {len(test_cases)}")
    print(f"  - 场景: {len(scenarios)}")


if __name__ == "__main__":
    create_sample_test_suite()

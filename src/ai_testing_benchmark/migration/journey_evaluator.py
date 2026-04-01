"""
云迁移旅程评估器 - 评估云迁移调研智能助手在10个阶段的能力。
"""

from typing import Dict, List, Any, Optional
import time
from datetime import datetime

from ai_testing_benchmark.core.base_evaluator import BaseEvaluator, EvaluationResult
from ai_testing_benchmark.core.result import PhaseResult


class CloudMigrationJourneyEvaluator(BaseEvaluator):
    """
    云迁移旅程评估器。

    评估云迁移调研智能助手在以下10个阶段的能力：
    1. 资源导入 (Resource Import)
    2. 资源清单确认 (Resource Inventory Confirmation)
    3. 资源总结 (Resource Summary)
    4. 分组确认 (Grouping Confirmation)
    5. 架构确认 (Architecture Confirmation)
    6. 上云策略确认 (Cloud Strategy Confirmation)
    7. 偏好确认 (Preference Confirmation)
    8. 规格推荐 (Specification Recommendation)
    9. 主机数据库兼容性任务 (Host Database Compatibility Task)
    10. 迁移报告生成 (Migration Report Generation)
    """

    # Phase常量
    PHASE_RESOURCE_IMPORT = "resource_import"
    PHASE_INVENTORY_CONFIRM = "inventory_confirmation"
    PHASE_RESOURCE_SUMMARY = "resource_summary"
    PHASE_GROUPING_CONFIRM = "grouping_confirmation"
    PHASE_ARCHITECTURE_CONFIRM = "architecture_confirmation"
    PHASE_CLOUD_STRATEGY = "cloud_strategy"
    PHASE_PREFERENCE_CONFIRM = "preference_confirmation"
    PHASE_SPECIFICATION = "specification_recommendation"
    PHASE_COMPATIBILITY = "compatibility_task"
    PHASE_REPORT = "report_generation"

    def __init__(
        self,
        model_name: str,
        provider: str = "openai",
        config: Optional[Dict] = None,
        verbose: bool = False
    ):
        """初始化云迁移旅程评估器。"""
        super().__init__(model_name, provider, config, verbose)

    def evaluate_single(self, test_case: Dict) -> EvaluationResult:
        """评估单个测试用例。"""
        start_time = time.time()

        phase = test_case.get("phase", self.PHASE_RESOURCE_IMPORT)
        test_id = test_case.get("id", "unknown")

        self.logger.info(f"正在评估 {test_id} ({phase})")

        # 根据阶段路由到对应的评估方法
        phase_evaluators = {
            self.PHASE_RESOURCE_IMPORT: self._evaluate_resource_import,
            self.PHASE_INVENTORY_CONFIRM: self._evaluate_inventory_confirmation,
            self.PHASE_RESOURCE_SUMMARY: self._evaluate_resource_summary,
            self.PHASE_GROUPING_CONFIRM: self._evaluate_grouping_confirmation,
            self.PHASE_ARCHITECTURE_CONFIRM: self._evaluate_architecture_confirmation,
            self.PHASE_CLOUD_STRATEGY: self._evaluate_cloud_strategy,
            self.PHASE_PREFERENCE_CONFIRM: self._evaluate_preference_confirmation,
            self.PHASE_SPECIFICATION: self._evaluate_specification_recommendation,
            self.PHASE_COMPATIBILITY: self._evaluate_compatibility_task,
            self.PHASE_REPORT: self._evaluate_report_generation,
        }

        evaluator = phase_evaluators.get(phase, self._evaluate_generic)
        result = evaluator(test_case)

        execution_time = (time.time() - start_time) * 1000

        return EvaluationResult(
            scenario_id=test_case.get("scenario_id", test_id),
            test_case_id=test_id,
            passed=result["passed"],
            score=result["score"],
            metrics=result.get("metrics", {}),
            details=result.get("details", {}),
            execution_time_ms=execution_time
        )

    def _evaluate_resource_import(self, test_case: Dict) -> Dict:
        """评估资源导入阶段。

        评估AI对用户描述的自然语言资源信息进行解析和提取的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("raw_description", ""))

        expected = test_case.get("expected_outputs", {})
        expected_vm_count = expected.get("vm_count", 0)
        expected_entities = expected.get("entities", [])

        # 模拟评估逻辑
        actual_vm_count = response.get("vm_count", expected_vm_count // 2)
        actual_entities = response.get("entities", [])

        # 计算准确率
        vm_accuracy = min(1.0, actual_vm_count / expected_vm_count) if expected_vm_count > 0 else 0.5

        # 实体提取F1
        if expected_entities and actual_entities:
            true_positives = len(set(actual_entities) & set(expected_entities))
            precision = true_positives / len(actual_entities) if actual_entities else 0
            recall = true_positives / len(expected_entities) if expected_entities else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        else:
            f1 = 0.5

        score = 0.4 * vm_accuracy + 0.6 * f1
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "vm_count_accuracy": vm_accuracy,
                "entity_extraction_f1": f1
            },
            "details": {
                "expected_vm_count": expected_vm_count,
                "actual_vm_count": actual_vm_count,
                "expected_entities": expected_entities,
                "actual_entities": actual_entities
            }
        }

    def _evaluate_inventory_confirmation(self, test_case: Dict) -> Dict:
        """评估资源清单确认阶段。

        评估AI确认和验证资源清单完整性的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("inventory_data", ""))

        expected = test_case.get("expected_outputs", {})
        expected_items = expected.get("confirmed_items", [])
        expected_completeness = expected.get("completeness_rate", 1.0)

        actual_confirmed = response.get("confirmed_items", expected_items[:len(expected_items)//2])
        actual_completeness = response.get("completeness_rate", expected_completeness * 0.8)

        # 完整性率
        completeness_score = actual_completeness / expected_completeness if expected_completeness > 0 else 0.5

        # 确认准确率
        if expected_items and actual_confirmed:
            correct_confirmations = len(set(actual_confirmed) & set(expected_items))
            confirmation_accuracy = correct_confirmations / len(expected_items)
        else:
            confirmation_accuracy = 0.5

        score = 0.5 * completeness_score + 0.5 * confirmation_accuracy
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "completeness_score": completeness_score,
                "confirmation_accuracy": confirmation_accuracy
            },
            "details": {
                "expected_completeness": expected_completeness,
                "actual_completeness": actual_completeness,
                "items_confirmed": len(actual_confirmed),
                "total_items": len(expected_items)
            }
        }

    def _evaluate_resource_summary(self, test_case: Dict) -> Dict:
        """评估资源总结阶段。

        评估AI生成清晰、准确的资源总结的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("resource_list", ""))

        expected = test_case.get("expected_outputs", {})
        key_info_covered = expected.get("key_info", [])

        actual_summary = response.get("summary", "")
        actual_key_info = response.get("key_info_found", key_info_covered[:len(key_info_covered)//2])

        # 关键信息覆盖率
        if key_info_covered:
            coverage = len(set(actual_key_info) & set(key_info_covered)) / len(key_info_covered)
        else:
            coverage = 0.5

        # 摘要长度合理性
        summary_length = len(actual_summary)
        length_score = min(1.0, summary_length / 500) if summary_length > 0 else 0

        score = 0.6 * coverage + 0.4 * length_score
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "key_info_coverage": coverage,
                "summary_quality": length_score
            },
            "details": {
                "key_info_expected": len(key_info_covered),
                "key_info_found": len(actual_key_info),
                "summary_length": summary_length
            }
        }

    def _evaluate_grouping_confirmation(self, test_case: Dict) -> Dict:
        """评估分组确认阶段。

        评估AI对资源进行合理分组的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("resources", ""))

        expected = test_case.get("expected_outputs", {})
        expected_groups = expected.get("groups", [])
        expected_dependencies = expected.get("dependencies", [])

        actual_groups = response.get("groups", expected_groups[:len(expected_groups)//2] if expected_groups else [])
        actual_dependencies = response.get("dependencies", [])

        # 分组一致性 - 检查资源是否被正确分组
        if expected_groups and actual_groups:
            total_resources = sum(len(g.get("resources", [])) for g in expected_groups)
            correctly_grouped = 0
            for ag in actual_groups:
                for eg in expected_groups:
                    if set(ag.get("resources", [])) == set(eg.get("resources", [])):
                        correctly_grouped += len(ag.get("resources", []))
                        break
            grouping_score = correctly_grouped / total_resources if total_resources > 0 else 0.5
        else:
            grouping_score = 0.5

        # 依赖感知 - 检查依赖关系是否被正确识别
        if expected_dependencies and actual_dependencies:
            correct_deps = len(set(actual_dependencies) & set(expected_dependencies))
            dependency_score = correct_deps / len(expected_dependencies)
        else:
            dependency_score = 0.5

        score = 0.6 * grouping_score + 0.4 * dependency_score
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "grouping_coherence": grouping_score,
                "dependency_awareness": dependency_score
            },
            "details": {
                "expected_groups": len(expected_groups),
                "actual_groups": len(actual_groups),
                "expected_dependencies": len(expected_dependencies),
                "correct_dependencies": len(actual_dependencies) if expected_dependencies else 0
            }
        }

    def _evaluate_architecture_confirmation(self, test_case: Dict) -> Dict:
        """评估架构确认阶段。

        评估AI推荐合适云架构的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("workload_info", ""))

        expected = test_case.get("expected_outputs", {})
        expected_architecture = expected.get("recommended_architecture", "")
        expected_components = expected.get("components", [])

        actual_architecture = response.get("architecture", "unknown")
        actual_components = response.get("components", [])

        # 架构匹配
        architecture_match = 1.0 if expected_architecture.lower() in actual_architecture.lower() else 0.5

        # 组件完整性
        if expected_components and actual_components:
            correct_components = len(set(actual_components) & set(expected_components))
            component_score = correct_components / len(expected_components)
        else:
            component_score = 0.5

        score = 0.5 * architecture_match + 0.5 * component_score
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "architecture_match": architecture_match,
                "component_completeness": component_score
            },
            "details": {
                "expected_architecture": expected_architecture,
                "recommended_architecture": actual_architecture,
                "expected_components": expected_components,
                "recommended_components": actual_components
            }
        }

    def _evaluate_cloud_strategy(self, test_case: Dict) -> Dict:
        """评估上云策略确认阶段。

        评估AI推荐合适迁移策略的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("application_info", ""))

        expected = test_case.get("expected_outputs", {})
        expected_strategies = expected.get("recommended_strategies", [])
        expected_rationale = expected.get("rationale", "")

        actual_strategies = response.get("strategies", expected_strategies[:1] if expected_strategies else [])
        actual_rationale = response.get("rationale", "")

        # 策略匹配率
        if expected_strategies and actual_strategies:
            matched_strategies = len(set(actual_strategies) & set(expected_strategies))
            strategy_match = matched_strategies / len(expected_strategies)
        else:
            strategy_match = 0.5

        # 理由质量 (长度作为代理指标)
        rationale_length = len(actual_rationale)
        rationale_quality = min(1.0, rationale_length / 200) if rationale_length > 0 else 0

        score = 0.6 * strategy_match + 0.4 * rationale_quality
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "strategy_match_rate": strategy_match,
                "rationale_quality": rationale_quality
            },
            "details": {
                "expected_strategies": expected_strategies,
                "recommended_strategies": actual_strategies,
                "rationale_length": rationale_length
            }
        }

    def _evaluate_preference_confirmation(self, test_case: Dict) -> Dict:
        """评估偏好确认阶段。

        评估AI理解和确认用户偏好的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("user_input", ""))

        expected = test_case.get("expected_outputs", {})
        expected_preferences = expected.get("preferences", [])

        actual_preferences = response.get("preferences", expected_preferences[:len(expected_preferences)//2] if expected_preferences else [])

        # 偏好提取准确率
        if expected_preferences and actual_preferences:
            correct_prefs = len(set(actual_preferences) & set(expected_preferences))
            preference_accuracy = correct_prefs / len(expected_preferences)
        else:
            preference_accuracy = 0.5

        score = preference_accuracy
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "preference_extraction_accuracy": preference_accuracy
            },
            "details": {
                "expected_preferences": expected_preferences,
                "extracted_preferences": actual_preferences
            }
        }

    def _evaluate_specification_recommendation(self, test_case: Dict) -> Dict:
        """评估规格推荐阶段。

        评估AI推荐合适云资源规格的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("workload_specs", ""))

        expected = test_case.get("expected_outputs", {})
        expected_specs = expected.get("recommended_specs", [])

        actual_specs = response.get("specs", expected_specs[:len(expected_specs)//2] if expected_specs else [])

        # 规格准确率
        if expected_specs and actual_specs:
            correct_specs = len(set(actual_specs) & set(expected_specs))
            spec_accuracy = correct_specs / len(expected_specs)
        else:
            spec_accuracy = 0.5

        # 成本效率评分
        cost_efficiency = response.get("cost_efficiency", 0.7)

        score = 0.5 * spec_accuracy + 0.5 * cost_efficiency
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "spec_accuracy": spec_accuracy,
                "cost_efficiency": cost_efficiency
            },
            "details": {
                "expected_specs": expected_specs,
                "recommended_specs": actual_specs
            }
        }

    def _evaluate_compatibility_task(self, test_case: Dict) -> Dict:
        """评估主机数据库兼容性任务阶段。

        评估AI分析源环境和目标环境兼容性的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("environment_info", ""))

        expected = test_case.get("expected_outputs", {})
        expected_issues = expected.get("compatibility_issues", [])
        expected_migrations = expected.get("migration_paths", [])

        actual_issues = response.get("issues", expected_issues[:len(expected_issues)//2] if expected_issues else [])
        actual_migrations = response.get("migration_paths", expected_migrations[:1] if expected_migrations else [])

        # 兼容性检测率
        if expected_issues and actual_issues:
            detected_issues = len(set(actual_issues) & set(expected_issues))
            detection_rate = detected_issues / len(expected_issues)
        else:
            detection_rate = 0.5

        # 迁移路径推荐质量
        migration_quality = len(actual_migrations) / len(expected_migrations) if expected_migrations else 0.5

        # 误报率 (假设越少越好)
        if actual_issues and expected_issues:
            false_positives = len(actual_issues) - len(set(actual_issues) & set(expected_issues))
            false_positive_rate = false_positives / len(actual_issues) if actual_issues else 0
        else:
            false_positive_rate = 0.3

        score = 0.4 * detection_rate + 0.3 * migration_quality + 0.3 * (1 - false_positive_rate)
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "compatibility_detection_rate": detection_rate,
                "migration_path_quality": migration_quality,
                "false_positive_rate": false_positive_rate
            },
            "details": {
                "expected_issues": len(expected_issues),
                "detected_issues": len(actual_issues),
                "expected_migration_paths": len(expected_migrations),
                "recommended_migration_paths": len(actual_migrations)
            }
        }

    def _evaluate_report_generation(self, test_case: Dict) -> Dict:
        """评估迁移报告生成阶段。

        评估AI生成完整、准确迁移报告的能力。
        """
        response = self._call_model(test_case.get("input", {}).get("migration_data", ""))

        expected = test_case.get("expected_outputs", {})
        expected_sections = expected.get("required_sections", [])
        expected_recommendations = expected.get("recommendations", [])

        actual_sections = response.get("sections", expected_sections[:len(expected_sections)//2] if expected_sections else [])
        actual_recommendations = response.get("recommendations", expected_recommendations[:len(expected_recommendations)//2] if expected_recommendations else [])

        # 报告完整性
        if expected_sections and actual_sections:
            covered_sections = len(set(actual_sections) & set(expected_sections))
            completeness = covered_sections / len(expected_sections)
        else:
            completeness = 0.5

        # 推荐质量
        if expected_recommendations and actual_recommendations:
            quality_recommendations = len(set(actual_recommendations) & set(expected_recommendations))
            recommendation_quality = quality_recommendations / len(expected_recommendations)
        else:
            recommendation_quality = 0.5

        score = 0.5 * completeness + 0.5 * recommendation_quality
        passed = score >= test_case.get("pass_threshold", 0.8)

        return {
            "passed": passed,
            "score": score,
            "metrics": {
                "report_completeness": completeness,
                "recommendation_quality": recommendation_quality
            },
            "details": {
                "expected_sections": len(expected_sections),
                "covered_sections": len(actual_sections),
                "expected_recommendations": len(expected_recommendations),
                "actual_recommendations": len(actual_recommendations)
            }
        }

    def _evaluate_generic(self, test_case: Dict) -> Dict:
        """通用评估后备方案。"""
        response = self._call_model(str(test_case.get("input", {})))
        return {
            "passed": True,
            "score": 0.5,
            "metrics": {},
            "details": {"response": response}
        }

    def run_phase(self) -> PhaseResult:
        """运行完整的旅程评估。"""
        phase_result = PhaseResult(phase="migration_journey")
        test_cases = self._load_test_cases()

        for test_case in test_cases:
            result = self.evaluate_single(test_case)
            phase_result.add_result(result)

        return phase_result

    def _load_test_cases(self) -> List[Dict]:
        """从JSON文件加载测试用例。"""
        import json
        import os
        from pathlib import Path

        # 查找数据文件
        possible_paths = [
            Path(__file__).parent.parent.parent / "data" / "journey_test_cases.json",
            Path(__file__).parent.parent.parent.parent / "data" / "journey_test_cases.json",
            Path("data/journey_test_cases.json"),
        ]

        for path in possible_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    test_cases = []
                    for phase_data in data.get("phases", []):
                        phase_name = phase_data.get("name", "")
                        for tc in phase_data.get("test_cases", []):
                            tc["phase"] = phase_name
                            test_cases.append(tc)

                    self.logger.info(f"从 {path} 加载了 {len(test_cases)} 个测试用例")
                    return test_cases
                except Exception as e:
                    self.logger.warning(f"加载测试用例失败 {path}: {e}")

        # 如果没有找到JSON文件，使用内置测试用例
        self.logger.warning("未找到JSON测试数据文件，使用内置测试用例")
        return self._get_builtin_test_cases()

    def _get_builtin_test_cases(self) -> List[Dict]:
        """获取内置测试用例（当JSON文件不可用时使用）。"""
        return [
            # Phase 1: 资源导入
            {
                "id": "TC-JOURNEY-001",
                "phase": self.PHASE_RESOURCE_IMPORT,
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
            },
            # Phase 2: 资源清单确认
            {
                "id": "TC-JOURNEY-002",
                "phase": self.PHASE_INVENTORY_CONFIRM,
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
            },
            # Phase 3: 资源总结
            {
                "id": "TC-JOURNEY-003",
                "phase": self.PHASE_RESOURCE_SUMMARY,
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
            },
            # Phase 4: 分组确认
            {
                "id": "TC-JOURNEY-004",
                "phase": self.PHASE_GROUPING_CONFIRM,
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
            },
            # Phase 5: 架构确认
            {
                "id": "TC-JOURNEY-005",
                "phase": self.PHASE_ARCHITECTURE_CONFIRM,
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
            },
            # Phase 6: 上云策略确认
            {
                "id": "TC-JOURNEY-006",
                "phase": self.PHASE_CLOUD_STRATEGY,
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
            },
            # Phase 7: 偏好确认
            {
                "id": "TC-JOURNEY-007",
                "phase": self.PHASE_PREFERENCE_CONFIRM,
                "scenario_id": "JOURNEY-007",
                "input": {
                    "user_input": "我们希望迁移到AWS，首选成本优化方案，希望保留一定的控制权"
                },
                "expected_outputs": {
                    "preferences": ["AWS", "成本优化", "保留控制权"]
                },
                "pass_threshold": 0.8
            },
            # Phase 8: 规格推荐
            {
                "id": "TC-JOURNEY-008",
                "phase": self.PHASE_SPECIFICATION,
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
            },
            # Phase 9: 主机数据库兼容性
            {
                "id": "TC-JOURNEY-009",
                "phase": self.PHASE_COMPATIBILITY,
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
            },
            # Phase 10: 迁移报告生成
            {
                "id": "TC-JOURNEY-010",
                "phase": self.PHASE_REPORT,
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
        ]

    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """计算所有测试用例的聚合分数。"""
        if not results:
            return {"overall_score": 0.0, "phase_scores": {}}

        # 按阶段分组
        by_phase: Dict[str, List] = {}
        for result in results:
            phase = result.details.get("phase", "unknown")
            if phase not in by_phase:
                by_phase[phase] = []
            by_phase[phase].append(result)

        # 计算每个阶段的平均分
        phase_scores = {}
        for phase, phase_results in by_phase.items():
            scores = [r.score for r in phase_results]
            phase_scores[phase] = sum(scores) / len(scores) if scores else 0

        # 总体分数为所有阶段分数的平均
        overall = sum(phase_scores.values()) / len(phase_scores) if phase_scores else 0

        return {
            "overall_score": overall,
            "phase_scores": phase_scores,
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results if r.passed)
        }

    def _call_model(self, prompt: str) -> Dict:
        """
        调用模型。

        生产环境中需集成实际模型API。
        此处为模拟响应。
        """
        prompt_str = str(prompt)[:100] if prompt else ""
        self.logger.debug(f"使用提示词调用模型: {prompt_str}...")

        # 模拟响应 - 根据输入内容生成简单的解析结果
        return {
            "vm_count": 50,
            "entities": ["VM", "Database", "Storage"],
            "summary": "这是一个资源总结...",
            "groups": [],
            "dependencies": [],
            "architecture": "高可用架构",
            "components": ["EC2", "RDS", "S3"],
            "strategies": ["Rehost"],
            "rationale": "建议采用重新托管策略...",
            "preferences": ["AWS"],
            "specs": ["t3.large"],
            "issues": ["兼容性"],
            "migration_paths": ["直接迁移"],
            "sections": ["概述", "迁移策略"],
            "recommendations": ["建议分阶段迁移"]
        }

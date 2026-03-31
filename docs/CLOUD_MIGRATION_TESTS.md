# 云迁移AI测试套件

## 概述

本文档为评估引导用户完成云迁移旅程的AI系统提供了全面的测试规范。测试按迁移阶段组织，涵盖迁移项目的完整生命周期。

---

## 迁移旅程阶段

```
┌────────────────────────────────────────────────────────────────────┐
│                      云迁移旅程                                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │         │    │         │    │         │    │         │         │
│  │ 评估    │───▶│ 规划    │───▶│ 执行    │───▶│ 验证    │         │
│  │         │    │         │    │         │    │         │         │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘         │
│       │              │              │              │               │
│       ▼              ▼              ▼              ▼               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │资产清单 │    │排序     │    │自动化    │    │功能     │         │
│  │风险识别 │    │策略     │    │迁移      │    │性能     │         │
│  │成本估算 │    │资源     │    │回滚      │    │安全     │         │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## 第一阶段：评估测试

### 1.1 基础设施发现

**目标**：验证AI能够准确发现和编目云基础设施资源。

#### TC-CM-ASSESS-001：服务器基础设施发现

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-001",
    "phase": "评估",
    "category": "infrastructure_discovery",
    "name": "服务器基础设施发现",
    "description": """
    评估AI从用户描述或数据导出中发现、编目和报告服务器基础设施的能力。
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "SS-001",
            "scenario_name": "中型企业设置",
            "input": {
                "description": """
                我们是一家典型的中型电子商务公司：
                - 2个数据中心（纽约主站，芝加哥DR站）
                - 100台物理服务器（40台Windows，60台Linux）
                - 150台由VMware管理的虚拟机
                - 8台数据库服务器（4台SQL Server，2台MySQL，2台PostgreSQL）
                - 15台运行Java微服务的应用程序服务器
                - 10台运行Apache和Nginx的Web服务器
                - 5台负载均衡器（F5 BigIP）
                - 20台交换机，10台路由器
                """,
                "data_export_available": False
            },
            "expected_outputs": {
                "total_servers": {"value": 100, "tolerance": 0.0},
                "total_vms": {"value": 150, "tolerance": 0.05},
                "database_count": {"value": 8, "tolerance": 0},
                "vmware_identified": True,
                "load_balancers_identified": {"value": 5, "tolerance": 0},
                "network_equipment_identified": {"value": 30, "tolerance": 0.1}
            },
            "catalog_completeness": 0.95,
            "false_positive_rate": 0.02
        },
        {
            "scenario_id": "SS-002",
            "scenario_name": "复杂微服务架构",
            "input": {
                "description": """
                我们的平台运行在Kubernetes上：
                - 3个集群（生产、预发布、开发）
                - 每个生产集群：50个节点（混合：30个计算优化型，20个内存优化型）
                - 预发布：10个节点
                - 开发：5个节点
                - 所有环境共200个微服务
                - 每个微服务：2-10个Pod（平均4个）
                - 服务：API网关、认证服务、用户服务、产品服务、
                  订单服务、支付服务、通知服务等
                - 入口控制器：3个（每个集群一个）
                - 服务网格：Istio
                - 容器注册表：Harbor
                """,
                "data_export_available": True,
                "export_format": "kubectl get nodes -o json"
            },
            "expected_outputs": {
                "total_nodes": {"value": 65, "tolerance": 0.05},
                "clusters_identified": {"value": 3, "tolerance": 0},
                "prod_node_count": {"value": 50, "tolerance": 0.05},
                "microservices_identified": {"value": 200, "tolerance": 0.1},
                "pods_estimated": {"value": 800, "tolerance": 0.15},
                "service_mesh_identified": True,
                "container_registry_identified": True
            },
            "catalog_completeness": 0.92,
            "false_positive_rate": 0.05
        }
    ],
    "evaluation_criteria": {
        "discovery_rate": {"threshold": 0.98, "weight": 0.35},
        "false_positive_rate": {"threshold": 0.03, "weight": 0.25},
        "attribute_accuracy": {"threshold": 0.90, "weight": 0.20},
        "classification_accuracy": {"threshold": 0.92, "weight": 0.20}
    },
    "quality_gates": {
        "min_discovery_rate": 0.95,
        "max_false_positive": 0.05,
        "required_output_fields": [
            "total_servers", "total_vms", "databases", "networking", "storage"
        ]
    }
}
```

#### TC-CM-ASSESS-002：依赖映射

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-002",
    "phase": "评估",
    "category": "dependency_mapping",
    "name": "应用程序依赖识别",
    "description": """
    评估AI识别和记录应用程序、服务和基础设施组件之间依赖关系的能力。
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "DM-001",
            "scenario_name": "三层Web应用程序",
            "input": {
                "description": """
                经典三层电子商务架构：

                Web层：
                - 前端：托管在S3 + CloudFront上的React SPA
                - CDN提供静态资产

                应用层：
                - API网关：Kong API网关
                - 产品服务（Java Spring Boot）→ 端口8080
                - 订单服务（Python FastAPI）→ 端口8000
                - 用户服务（Node.js Express）→ 端口3000
                - 支付服务（Go）→ 端口9090
                - 库存服务（Rust）→ 端口8081

                数据层：
                - PostgreSQL：产品、订单、用户（主库）
                - Redis：会话缓存、限流
                - Elasticsearch：产品搜索
                - S3：静态资产、订单文档

                消息队列：
                - RabbitMQ：异步订单处理
                - Kafka：分析事件流

                依赖关系：
                - 前端调用API网关
                - API网关路由到服务
                - 服务查询PostgreSQL
                - 订单服务发布到RabbitMQ
                - 支付服务从RabbitMQ读取
                - 产品服务索引到Elasticsearch
                """,
                "known_dependencies": 12,
                "hidden_dependencies": 3
            },
            "expected_outputs": {
                "total_dependencies_found": {"min": 12, "max": 15},
                "critical_path_identifed": True,
                "dependency_graph_complete": True,
                "bidirectional_dependencies_captured": {"value": 4, "tolerance": 1}
            },
            "evaluation_metrics": {
                "dependency_recall": {"threshold": 0.95},
                "dependency_precision": {"threshold": 0.90},
                "cycle_detection": {"threshold": 1.0}  # 必须检测循环（如果有）
            }
        },
        {
            "scenario_id": "DM-002",
            "scenario_name": "带断路器的微服务",
            "input": {
                "architecture_diagram": "see test_data/diagrams/microservices.pdf",
                "description": """
                带断路器模式的复杂微服务：

                API网关 → 认证 → 限流 → 服务网格（Istio）
                    ↓
                [产品目录] ←→ [搜索服务]
                    ↓                    ↓
                [库存]     ←→     [缓存]
                    ↓
                [订单]  ──→  [支付]
                    ↓
                [配送] ←── [通知]

                每个服务都有：
                - 断路器（Hystrix/Envoy）
                - 重试策略
                - 回退机制
                - 健康检查端点
                """,
                "expected_circuit_breaker_count": 8,
                "expected_fallback_dependencies": 6
            },
            "expected_outputs": {
                "services_identified": {"value": 8, "tolerance": 0},
                "circuit_breakers_identified": {"threshold": 0.90},
                "fallback_paths_identified": {"threshold": 0.85},
                "dependency_direction_correct": {"threshold": 0.95}
            }
        }
    ],
    "evaluation_criteria": {
        "dependency_recall": {"threshold": 0.95, "weight": 0.35},
        "dependency_precision": {"threshold": 0.92, "weight": 0.30},
        "graph_correctness": {"threshold": 0.90, "weight": 0.20},
        "bidirectional_capture": {"threshold": 0.85, "weight": 0.15}
    },
    "quality_gates": {
        "min_recall": 0.92,
        "no_missing_critical_dependencies": True
    }
}
```

### 1.2 风险识别

#### TC-CM-ASSESS-003：风险检测和分类

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-003",
    "phase": "评估",
    "category": "risk_identification",
    "name": "迁移风险检测",
    "description": """
    评估AI识别、分类和评估与云迁移场景相关风险的能力。
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "RI-001",
            "scenario_name": "数据主权风险",
            "input": {
                "description": """
                金融服务业公司迁移到云：

                基础设施：
                - 包含PII（姓名、SSN、财务数据）的客户数据库
                - 监管要求：数据必须保留在美国区域
                - 当前设置：美国多区域数据中心
                - 15 PB结构化和非结构化数据
                - 站点间实时复制

                合规性：
                - SOX、PCI-DSS 1级、GDPR（针对欧盟客户）
                - 数据保留策略：7年
                - 年度SOC 2审计

                利益相关者关注：
                - CEO："我们不能承受任何数据泄露"
                - 法务："我们需要维护数据主权"
                - CTO："云将为我们节省30%的基础设施成本"
                """,
                "known_risk_categories": [
                    "data_sovereignty",
                    "compliance",
                    "security",
                    "cost",
                    "performance"
                ]
            },
            "expected_outputs": {
                "risks_identified": {
                    "data_sovereignty": {
                        "severity": "高",
                        "probability": 0.70,
                        "impact": "高",
                        "detection_confidence": 0.95
                    },
                    "compliance_violation": {
                        "severity": "严重",
                        "probability": 0.60,
                        "impact": "严重",
                        "detection_confidence": 0.92
                    },
                    "security_breach": {
                        "severity": "高",
                        "probability": 0.40,
                        "impact": "严重",
                        "detection_confidence": 0.88
                    },
                    "cost_overrun": {
                        "severity": "中",
                        "probability": 0.50,
                        "impact": "中",
                        "detection_confidence": 0.85
                    }
                },
                "mitigation_strategies_provided": True,
                "risk_register_complete": True
            }
        },
        {
            "scenario_id": "RI-002",
            "scenario_name": "遗留应用程序依赖",
            "input": {
                "description": """
                拥有遗留系统的制造业公司：

                遗留基础设施：
                - 30年历史的ERP系统（AS/400，COBOL）
                - 自1995年以来运行的自定义批处理作业
                - 通过平面文件交换集成
                - 无API层，直接数据库连接

                现代系统：
                - Salesforce CRM
                - SAP S/4HANA
                - 自定义MES系统

                集成挑战：
                - AS/400通过MQSeries通信
                - 基于文件的批处理作业在凌晨2点运行
                - 一些COBOL程序从DB2读取

                团队能力：
                - 5名COBOL开发人员（ 모두 >50岁，5年内退休）
                - 40%的遗留代码没有文档
                """,
                "known_risk_categories": [
                    "technical_debt",
                    "skill_gaps",
                    "integration_complexity",
                    "vendor_lockin"
                ]
            },
            "expected_outputs": {
                "legacy_modern_integration_risk": {
                    "severity": "高",
                    "detection_confidence": 0.93
                },
                "skill_gap_risk": {
                    "severity": "中",
                    "detection_confidence": 0.88
                },
                "documentation_risk": {
                    "severity": "高",
                    "detection_confidence": 0.85
                },
                "migration_strategy_impact": "建议重构或重新平台化"
            }
        }
    ],
    "evaluation_criteria": {
        "risk_detection_rate": {"threshold": 0.95, "weight": 0.30},
        "severity_classification_accuracy": {"threshold": 0.88, "weight": 0.25},
        "mitigation_relevance": {"threshold": 0.85, "weight": 0.25},
        "false_positive_rate": {"threshold": 0.10, "weight": 0.20}
    },
    "quality_gates": {
        "critical_risks_must_be_detected": True,
        "no_missing_high_severity_risks": True
    }
}
```

### 1.3 成本估算

#### TC-CM-ASSESS-004：云成本估算准确性

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-004",
    "phase": "评估",
    "category": "cost_estimation",
    "name": "迁移成本估算",
    "description": """
    评估AI估算云迁移成本的能力，包括基础设施、迁移和运营费用。
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "CE-001",
            "scenario_name": "中型企业AWS迁移",
            "input": {
                "source_infrastructure": {
                    "servers": 100,
                    "types": {
                        "web_server": {"count": 30, "spec": "4 vCPU, 16GB RAM"},
                        "app_server": {"count": 40, "spec": "8 vCPU, 32GB RAM"},
                        "db_server": {"count": 15, "spec": "16 vCPU, 64GB RAM"},
                        "cache_server": {"count": 10, "spec": "4 vCPU, 16GB RAM"},
                        "file_server": {"count": 5, "spec": "4 vCPU, 8GB RAM"}
                    },
                    "utilization_avg": 0.45,
                    "storage_tb": 50
                },
                "current_monthly_cost": "$45,000 (本地)",
                "migration_type": "lift_and_shift_initial",
                "target_provider": "AWS",
                "assumptions_provided": True
            },
            "expected_outputs": {
                "monthly_aws_cost": {
                    "expected_range": [32000, 45000],  # 基于AWS定价
                    "tolerance": 0.15  # +/- 15%
                },
                "year_one_total": {
                    "expected_range": [450000, 600000],
                    "breakdown_required": [
                        "compute", "storage", "data_transfer",
                        "reserved_instance_savings", "migration_costs"
                    ]
                },
                "cost_breakdown": {
                    "compute_percentage": {"range": [50, 70]},
                    "storage_percentage": {"range": [15, 25]},
                    "networking_percentage": {"range": [5, 15]}
                },
                "optimization_recommendations": {"min_count": 3}
            },
            "evaluation_metrics": {
                "total_cost_accuracy": {"threshold": 0.85},
                "breakdown_accuracy": {"threshold": 0.80},
                "optimization_relevance": {"threshold": 0.75}
            }
        },
        {
            "scenario_id": "CE-002",
            "scenario_name": "多提供商成本比较",
            "input": {
                "workload": {
                    "ec2_instances": 50,
                    "instance_type": "m5.large",
                    "monthly_hours": 730,
                    "storage_gb": 10000,
                    "data_transfer_gb": 5000
                },
                "providers_to_compare": ["AWS", "Azure", "GCP"]
            },
            "expected_outputs": {
                "aws_monthly_estimate": {"tolerance": 0.10},
                "azure_monthly_estimate": {"tolerance": 0.10},
                "gcp_monthly_estimate": {"tolerance": 0.10},
                "lowest_cost_provider_identified": True,
                "reasoning_provided": True
            }
        }
    ],
    "evaluation_criteria": {
        "total_cost_accuracy": {"threshold": 0.85, "weight": 0.40},
        "cost_breakdown_accuracy": {"threshold": 0.80, "weight": 0.25},
        "optimization_recommendation_quality": {"threshold": 0.75, "weight": 0.20},
        "comparison_accuracy": {"threshold": 0.85, "weight": 0.15}
    },
    "quality_gates": {
        "max_cost_estimation_error": 0.15,
        "required_line_items": ["compute", "storage", "transfer"]
    }
}
```

---

## 第二阶段：规划测试

### 2.1 排序优化

#### TC-CM-PLAN-001：迁移顺序优化

```python
TEST_CASE = {
    "id": "TC-CM-PLAN-001",
    "phase": "规划",
    "category": "sequencing_optimization",
    "name": "迁移顺序优化",
    "description": """
    评估AI考虑依赖关系、风险、资源和业务约束来确定最佳迁移顺序的能力。
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "SEQ-001",
            "scenario_name": "电子商务平台迁移",
            "input": {
                "applications": [
                    {"id": "APP-001", "name": "用户认证服务", "dependencies": [], "risk": "低"},
                    {"id": "APP-002", "name": "产品目录", "dependencies": [], "risk": "低"},
                    {"id": "APP-003", "name": "搜索服务", "dependencies": ["APP-002"], "risk": "中"},
                    {"id": "APP-004", "name": "购物车", "dependencies": ["APP-001", "APP-003"], "risk": "中"},
                    {"id": "APP-005", "name": "订单处理", "dependencies": ["APP-001", "APP-004"], "risk": "高"},
                    {"id": "APP-006", "name": "支付服务", "dependencies": ["APP-001"], "risk": "严重"},
                    {"id": "APP-007", "name": "库存管理", "dependencies": ["APP-003"], "risk": "中"},
                    {"id": "APP-008", "name": "配送集成", "dependencies": ["APP-005"], "risk": "低"},
                    {"id": "APP-009", "name": "邮件服务", "dependencies": [], "risk": "低"},
                    {"id": "APP-010", "name": "分析管道", "dependencies": ["APP-005", "APP-007"], "risk": "低"},
                ],
                "constraints": {
                    "max_concurrent_migrations": 2,
                    "business_freeze_dates": ["2024-12-20", "2024-12-31"],
                    "team_capacity": 5,
                    "must_complete_by": "2024-06-30"
                },
                "migration_strategies": {
                    "APP-001": "重新托管",
                    "APP-002": "重新托管",
                    "APP-003": "重构",
                    "APP-004": "重新平台化",
                    "APP-005": "重构",
                    "APP-006": "重构",
                    "APP-007": "重新平台化",
                    "APP-008": "重新托管",
                    "APP-009": "重新托管",
                    "APP-010": "重新托管"
                }
            },
            "expected_outputs": {
                "migration_sequence": {
                    "valid": True,
                    "dependency_respected": True,
                    "constraint_satisfied": True
                },
                "phase_1_apps": {"expected": ["APP-001", "APP-002", "APP-009"], "tolerance": 0},
                "phase_2_apps": {"expected": ["APP-003", "APP-008"], "tolerance": 0},
                "phase_3_apps": {"expected": ["APP-004", "APP-007"], "tolerance": 0},
                "phase_4_apps": {"expected": ["APP-005", "APP-010"], "tolerance": 0},
                "phase_5_apps": {"expected": ["APP-006"], "tolerance": 0},
                "estimated_duration_days": {"expected_range": [80, 100]},
                "critical_path": ["APP-001/APP-002", "APP-003", "APP-004", "APP-005', 'APP-006"]
            },
            "evaluation_metrics": {
                "dependency_satisfaction": {"threshold": 1.0},
                "constraint_satisfaction": {"threshold": 1.0},
                "makespan_optimality": {"threshold": 0.85},
                "risk_balancing": {"threshold": 0.80}
            }
        },
        {
            "scenario_id": "SEQ-002",
            "scenario_name": "数据库优先迁移策略",
            "input": {
                "applications": [
                    {"id": "DB-001", "name": "客户数据库（PostgreSQL）", "dependencies": [], "size_tb": 5},
                    {"id": "DB-002", "name": "订单数据库（MongoDB）", "dependencies": [], "size_tb": 2},
                    {"id": "DB-003", "name": "分析数据库（ClickHouse）", "dependencies": [], "size_tb": 10},
                    {"id": "SVC-001", "name": "客户API", "dependencies": ["DB-001"], "risk": "高"},
                    {"id": "SVC-002", "name": "订单服务", "dependencies": ["DB-002"], "risk": "高"},
                    {"id": "SVC-003", "name": "分析服务", "dependencies": ["DB-003"], "risk": "中"},
                ],
                "constraints": {
                    "database_first": True,
                    "max_db_migration_parallel": 1,
                    "zero_downtime_required": True
                }
            },
            "expected_outputs": {
                "db_migrations_first": True,
                "data_sync_strategy_provided": True,
                "cutover_plan_complete": True,
                "rollback_strategy_provided": True
            }
        }
    ],
    "evaluation_criteria": {
        "dependency_satisfaction": {"threshold": 1.0, "weight": 0.30},
        "constraint_satisfaction": {"threshold": 1.0, "weight": 0.25},
        "makespan_optimality": {"threshold": 0.85, "weight": 0.25},
        "resource_utilization": {"threshold": 0.80, "weight": 0.20}
    },
    "quality_gates": {
        "zero_violations": True,
        "critical_path_correct": True
    }
}
```

### 2.2 策略推荐

#### TC-CM-PLAN-002：迁移策略选择

```python
TEST_CASE = {
    "id": "TC-CM-PLAN-002",
    "phase": "规划",
    "category": "strategy_recommendation",
    "name": "迁移策略推荐",
    "description": """
    评估AI根据应用程序特性和业务需求推荐适当迁移策略
    （重新托管、重新平台化、重构等）的能力。
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "STR-001",
            "scenario_name": "应用程序组合策略组合",
            "input": {
                "applications": [
                    {
                        "id": "APP-001",
                        "name": "遗留单体ERP",
                        "characteristics": {
                            "age_years": 15,
                            "tech_stack": "Java 8, WAS 8.5, DB2",
                            "architecture": "monolithic",
                            "change_frequency": "quarterly",
                            "technical_debt": "高",
                            "team_familiarity": "低",
                            "business_criticality": "严重",
                            "scaling_needs": "中等",
                            "customizations": "大量"
                        }
                    },
                    {
                        "id": "APP-002",
                        "name": "客户门户",
                        "characteristics": {
                            "age_years": 3,
                            "tech_stack": "Node.js, React, PostgreSQL",
                            "architecture": "microservices",
                            "change_frequency": "weekly",
                            "technical_debt": "低",
                            "team_familiarity": "高",
                            "business_criticality": "高",
                            "scaling_needs": "高",
                            "customizations": "最少"
                        }
                    },
                    {
                        "id": "APP-003",
                        "name": "批处理系统",
                        "characteristics": {
                            "age_years": 8,
                            "tech_stack": "COBOL, VSAM, JCL",
                            "architecture": "mainframe",
                            "change_frequency": "rarely",
                            "technical_debt": "中",
                            "team_familiarity": "非常低",
                            "business_criticality": "中",
                            "scaling_needs": "低",
                            "customizations": "中等"
                        }
                    },
                    {
                        "id": "APP-004",
                        "name": "实时分析仪表板",
                        "characteristics": {
                            "age_years": 1,
                            "tech_stack": "Python, Kafka, Elastic",
                            "architecture": "event-driven",
                            "change_frequency": "daily",
                            "technical_debt": "低",
                            "team_familiarity": "高",
                            "business_criticality": "中",
                            "scaling_needs": "非常高",
                            "customizations": "最少"
                        }
                    }
                ]
            },
            "expected_outputs": {
                "APP-001": {
                    "recommended_strategy": "重构",
                    "alternative_strategy": "重新平台化",
                    "rationale": "高技术债务、低团队熟悉度、大量定制化justify重构为现代栈",
                    "estimated_timeline_months": {"range": [12, 18]},
                    "estimated_cost": {"range": [1500000, 2500000]}
                },
                "APP-002": {
                    "recommended_strategy": "重新托管",
                    "alternative_strategy": "无",
                    "rationale": "现代栈、低债务、高团队熟悉度 - 通过重新托管快速获胜",
                    "estimated_timeline_months": {"range": [1, 2]}
                },
                "APP-003": {
                    "recommended_strategy": "保留/重新托管",
                    "alternative_strategy": "重新平台化",
                    "rationale": "大型机批处理 - 考虑淘汰或最小更改",
                    "estimated_timeline_months": {"range": [3, 6]}
                },
                "APP-004": {
                    "recommended_strategy": "重构",
                    "alternative_strategy": "原生云服务",
                    "rationale": "已是云就绪架构，重构为托管服务以提高成本效率",
                    "estimated_timeline_months": {"range": [3, 4]}
                }
            },
            "evaluation_metrics": {
                "strategy_accuracy": {"threshold": 0.85},
                "rationale_quality": {"threshold": 0.80},
                "timeline_accuracy": {"threshold": 0.75},
                "cost_accuracy": {"threshold": 0.70}
            }
        }
    ],
    "evaluation_criteria": {
        "recommendation_accuracy": {"threshold": 0.85, "weight": 0.35},
        "rationale_quality": {"threshold": 0.80, "weight": 0.25},
        "timeline_accuracy": {"threshold": 0.75, "weight": 0.20},
        "cost_accuracy": {"threshold": 0.70, "weight": 0.20}
    },
    "quality_gates": {
        "critical_apps_correct_strategy": True,
        "no_replatform_when_refactor_needed": True
    }
}
```

---

## 第三阶段：执行测试

### 3.1 自动化迁移

#### TC-CM-EXEC-001：迁移前验证

```python
TEST_CASE = {
    "id": "TC-CM-EXEC-001",
    "phase": "执行",
    "category": "pre_migration_validation",
    "name": "迁移前环境验证",
    "description": """
    评估AI执行全面迁移前验证的能力，包括连接性、权限和先决条件。
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "PRE-001",
            "scenario_name": "多层应用程序预检查",
            "input": {
                "migration_task": {
                    "source": "本地vmware",
                    "target": "AWS EC2",
                    "application": "三层Web应用",
                    "vm_list": ["WEB-01", "WEB-02", "APP-01", "APP-02", "DB-01"]
                },
                "validation_checklist": [
                    "network_connectivity",
                    "iam_permissions",
                    "subnet_availability",
                    "security_group_rules",
                    "storage_capacity",
                    "instance_quota",
                    "dependency_health"
                ]
            },
            "expected_outputs": {
                "validation_results": {
                    "network_connectivity": {
                        "status": "通过",
                        "details": "VPN已配置，VPC对等连接就绪"
                    },
                    "iam_permissions": {
                        "status": "通过",
                        "details": "迁移角色具有所需权限"
                    },
                    "subnet_availability": {
                        "status": "通过",
                        "available_azs": ["us-east-1a", "us-east-1b", "us-east-1c"]
                    },
                    "security_group_rules": {
                        "status": "警告",
                        "details": "生产环境需要调整端口3389 RDP"
                    },
                    "storage_capacity": {
                        "status": "通过",
                        "available_iops": 30000
                    },
                    "instance_quota": {
                        "status": "通过",
                        "available_count": 50
                    }
                },
                "overall_status": "通过_带警告",
                "warnings_count": 1,
                "blocking_issues": [],
                "recommendations": ["切换前更新安全组"]
            }
        }
    ],
    "evaluation_criteria": {
        "check_completeness": {"threshold": 1.0, "weight": 0.30},
        "issue_detection_rate": {"threshold": 0.95, "weight": 0.35},
        "false_positive_rate": {"threshold": 0.05, "weight": 0.20},
        "recommendation_relevance": {"threshold": 0.90, "weight": 0.15}
    }
}
```

#### TC-CM-EXEC-002：迁移执行监控

```python
TEST_CASE = {
    "id": "TC-CM-EXEC-002",
    "phase": "执行",
    "category": "migration_monitoring",
    "name": "实时迁移进度监控",
    "description": """
    评估AI监控迁移进度、检测问题并提供实时状态更新的能力。
    """,
    "difficulty": "high",
    "simulated_migration": {
        "total_vms": 50,
        "estimated_duration_minutes": 180,
        "phases": [
            {"name": "preparation", "duration_min": 15, "vms": 0},
            {"name": "replication", "duration_min": 120, "vms": 45},
            {"name": "cutover", "duration_min": 30, "vms": 5},
            {"name": "validation", "duration_min": 15, "vms": 0}
        ]
    },
    "test_scenarios": [
        {
            "scenario_id": "MON-001",
            "scenario_name": "正常迁移进度",
            "input": {
                "elapsed_time_minutes": 60,
                "completed_vms": 15,
                "failed_vms": 0,
                "replication_throughput_mbps": 450,
                "current_phase": "replication"
            },
            "expected_outputs": {
                "progress_percentage": {"expected": 30, "tolerance": 5},
                "estimated_completion_time": {"expected_minutes": 120, "tolerance": 20},
                "status": "正常",
                "health_score": {"min": 85}
            }
        },
        {
            "scenario_id": "MON-002",
            "scenario_name": "带失败的迁移",
            "input": {
                "elapsed_time_minutes": 90,
                "completed_vms": 20,
                "failed_vms": 3,
                "failed_vm_ids": ["WEB-03", "APP-05", "DB-02"],
                "replication_throughput_mbps": 380,
                "current_phase": "replication",
                "errors_logged": [
                    {"vm": "WEB-03", "error": "存储超时", "timestamp": "T+85"},
                    {"vm": "APP-05", "error": "网络分区", "timestamp": "T+88"},
                    {"vm": "DB-02", "error": "校验和不匹配", "timestamp": "T+89"}
                ]
            },
            "expected_outputs": {
                "status": "降级",
                "failure_impact_analysis": {
                    "WEB-03": {"severity": "低", "retry_recommended": True},
                    "APP-05": {"severity": "中", "retry_recommended": True},
                    "DB-02": {"severity": "高", "manual_intervention_required": True}
                },
                "updated_estimated_completion": {"expected_range": [150, 200]},
                "recovery_recommendations": [
                    "自动重试WEB-03和APP-05",
                    "调查DB-02存储子系统",
                    "考虑减少复制并行度"
                ],
                "health_score": {"expected_range": [65, 75]}
            }
        }
    ],
    "evaluation_criteria": {
        "progress_accuracy": {"threshold": 0.95, "weight": 0.25},
        "failure_detection_rate": {"threshold": 1.0, "weight": 0.25},
        "impact_assessment_accuracy": {"threshold": 0.90, "weight": 0.25},
        "recommendation_quality": {"threshold": 0.85, "weight": 0.25}
    }
}
```

### 3.2 回滚能力

#### TC-CM-EXEC-003：回滚触发和执行

```python
TEST_CASE = {
    "id": "TC-CM-EXEC-003",
    "phase": "执行",
    "category": "rollback",
    "name": "迁移回滚能力",
    "description": """
    评估AI确定何时需要回滚、执行回滚程序并验证成功回滚的能力。
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "RB-001",
            "scenario_name": "严重故障回滚",
            "input": {
                "migration_state": {
                    "phase": "cutover",
                    "completed_vms": 35,
                    "remaining_vms": 15,
                    "cutover_start_time": "T-20",
                    "failed_components": [
                        {
                            "vm": "DB-PRIMARY",
                            "failure_type": "connection_timeout",
                            "affected_services": ["订单服务", "支付服务", "用户服务"],
                            "service_impact": "严重",
                            "rto_minutes": 30,
                            "current_downtime_minutes": 25
                        }
                    ],
                    "database_replication_status": "STALLED",
                    "last_successful_checkpoint": "T-35"
                },
                "rollback_options": [
                    {
                        "type": "full_rollback",
                        "duration_minutes": 45,
                        "data_loss_mb": 0,
                        "risk": "低"
                    },
                    {
                        "type": "targeted_rollback",
                        "duration_minutes": 20,
                        "data_loss_mb": 1500,
                        "affected_services": ["DB-PRIMARY"],
                        "risk": "中"
                    }
                ]
            },
            "expected_outputs": {
                "rollback_decision": {
                    "recommended": "targeted_rollback",
                    "rationale": "严重生产影响，25分钟停机，5分钟到RTO",
                    "decision_time_seconds": {"max": 30}
                },
                "rollback_plan": {
                    "type": "targeted_rollback",
                    "sequence": [
                        "停止对DB-PRIMARY的所有写操作",
                        "将DB-PRIMARY恢复到T-35检查点",
                        "恢复网络连接",
                        "验证服务依赖关系",
                        "按顺序恢复服务：认证 → 订单 → 支付"
                    ],
                    "estimated_duration_minutes": 20,
                    "data_loss_mb": 1500
                },
                "validation_checks": [
                    "service_dependency_order",
                    "data_integrity_checkpoints",
                    "connectivity_verification"
                ],
                "post_rollback_status": {
                    "expected_recovery_time": 20,
                    "services_restored": ["认证", "订单", "支付"],
                    "rto_met": True
                }
            }
        }
    ],
    "evaluation_criteria": {
        "decision_correctness": {"threshold": 1.0, "weight": 0.30},
        "decision_time_seconds": {"threshold": 60, "weight": 0.20},
        "rollback_execution_accuracy": {"threshold": 0.95, "weight": 0.30},
        "recovery_time_accuracy": {"threshold": 0.85, "weight": 0.20}
    },
    "quality_gates": {
        "zero_data_loss_if_possible": True,
        "rto_met": True,
        "no_cascading_failures": True
    }
}
```

---

## 第四阶段：验证测试

### 4.1 功能验证

#### TC-CM-VAL-001：迁移后功能验证

```python
TEST_CASE = {
    "id": "TC-CM-VAL-001",
    "phase": "验证",
    "category": "functional_validation",
    "name": "迁移后功能测试",
    "description": """
    评估AI执行和解释迁移后功能验证测试的能力。
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "FUNC-001",
            "scenario_name": "Web应用程序功能验证",
            "input": {
                "migrated_application": "电子商务平台",
                "test_suite": {
                    "smoke_tests": [
                        {"name": "homepage_load", "endpoint": "/", "expected_status": 200},
                        {"name": "product_search", "endpoint": "/api/products/search?q=laptop", "expected_status": 200},
                        {"name": "user_login", "endpoint": "/api/auth/login", "method": "POST", "expected_status": 200},
                        {"name": "add_to_cart", "endpoint": "/api/cart/add", "method": "POST", "expected_status": 201}
                    ],
                    "integration_tests": [
                        {"name": "complete_order_flow", "steps": 8, "expected_completion": True},
                        {"name": "payment_processing", "steps": 5, "expected_completion": True},
                        {"name": "inventory_update", "steps": 3, "expected_completion": True}
                    ],
                    "regression_tests": [
                        {"name": "existing_user_login", "expected_status": 200},
                        {"name": "order_history_retrieval", "expected_status": 200},
                        {"name": "password_reset", "expected_status": 200}
                    ]
                },
                "test_results": {
                    "smoke_tests": {"passed": 4, "failed": 0, "skipped": 0},
                    "integration_tests": {"passed": 3, "failed": 0, "skipped": 0},
                    "regression_tests": {"passed": 3, "failed": 0, "skipped": 0}
                }
            },
            "expected_outputs": {
                "overall_status": "通过",
                "test_pass_rate": 100.0,
                "functional_equivalence_score": {"min": 95},
                "issues_found": [],
                "deployment_ready": True
            }
        },
        {
            "scenario_id": "FUNC-002",
            "scenario_name": "API契约验证",
            "input": {
                "api_service": "用户管理API",
                "pre_migration_schema_hash": "abc123",
                "post_migration_schema_hash": "abc123",
                "endpoint_tests": [
                    {
                        "endpoint": "/api/v1/users",
                        "methods": ["GET", "POST"],
                        "response_schema_validated": True,
                        "backward_compatibility": "MAINTAINED"
                    },
                    {
                        "endpoint": "/api/v1/users/{id}",
                        "methods": ["GET", "PUT", "DELETE"],
                        "response_schema_validated": True,
                        "backward_compatibility": "MAINTAINED"
                    }
                ]
            },
            "expected_outputs": {
                "schema_unchanged": True,
                "contract_test_pass": True,
                "breaking_changes": [],
                "api_health_score": {"min": 95}
            }
        }
    ],
    "evaluation_criteria": {
        "test_coverage": {"threshold": 0.95, "weight": 0.25},
        "issue_detection_rate": {"threshold": 0.90, "weight": 0.30},
        "false_positive_rate": {"threshold": 0.05, "weight": 0.20},
        "report_completeness": {"threshold": 0.90, "weight": 0.25}
    }
}
```

### 4.2 性能验证

#### TC-CM-VAL-002：迁移后性能基准

```python
TEST_CASE = {
    "id": "TC-CM-VAL-002",
    "phase": "验证",
    "category": "performance_validation",
    "name": "针对迁移前基准的性能",
    "description": """
    验证迁移的工作负载满足或超过迁移前的性能基准。
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "PERF-001",
            "scenario_name": "Web应用程序性能",
            "input": {
                "pre_migration_baseline": {
                    "avg_response_time_ms": 150,
                    "p95_response_time_ms": 350,
                    "p99_response_time_ms": 500,
                    "requests_per_second": 1000,
                    "error_rate": 0.001,
                    "cpu_utilization": 0.65,
                    "memory_utilization": 0.70
                },
                "post_migration_metrics": {
                    "test_duration_minutes": 30,
                    "concurrent_users": 500,
                    "total_requests": 900000,
                    "avg_response_time_ms": 120,
                    "p95_response_time_ms": 280,
                    "p99_response_time_ms": 420,
                    "requests_per_second": 1200,
                    "error_rate": 0.0008,
                    "cpu_utilization": 0.55,
                    "memory_utilization": 0.60
                }
            },
            "expected_outputs": {
                "performance_comparison": {
                    "response_time_improvement": {"expected_min": 0.10},  # 10%改进
                    "throughput_improvement": {"expected_min": 0.15},  # 15%改进
                    "error_rate_improvement": {"expected_min": 0.10},  # 10%改进
                    "resource_efficiency_improvement": {"expected_min": 0.15}
                },
                "validation_status": "通过",
                "performance_gain_percentage": {"expected_range": [10, 30]},
                "optimization_recommendations": []  # 仅在性能不佳时
            }
        },
        {
            "scenario_id": "PERF-002",
            "scenario_name": "数据库性能回归",
            "input": {
                "pre_migration_baseline": {
                    "queries_per_second": 5000,
                    "avg_query_time_ms": 15,
                    "p95_query_time_ms": 45,
                    "connection_pool_usage": 0.75,
                    "cache_hit_ratio": 0.92
                },
                "post_migration_metrics": {
                    "queries_per_second": 4500,
                    "avg_query_time_ms": 18,
                    "p95_query_time_ms": 55,
                    "connection_pool_usage": 0.80,
                    "cache_hit_ratio": 0.88
                }
            },
            "expected_outputs": {
                "regression_detected": True,
                "regression_severity": "中",
                "affected_queries": [
                    "complex_aggregation_queries",
                    "multi_join_queries"
                ],
                "root_cause_hypothesis": [
                    "新实例未针对工作负载模式优化",
                    "缓存预热期未完成",
                    "索引统计可能需要更新"
                ],
                "recommendations": [
                    "对数据库运行ANALYZE",
                    "审查查询执行计划",
                    "考虑调整实例类型",
                    "用常见查询预热缓存"
                ],
                "validation_status": "条件通过"
            }
        }
    ],
    "evaluation_criteria": {
        "baseline_comparison_accuracy": {"threshold": 0.95, "weight": 0.30},
        "regression_detection_rate": {"threshold": 0.90, "weight": 0.30},
        "root_cause_accuracy": {"threshold": 0.75, "weight": 0.25},
        "recommendation_quality": {"threshold": 0.80, "weight": 0.15}
    },
    "quality_gates": {
        "critical_performance_not_degraded": True,
        "no_p99_regression_over_20_percent": True
    }
}
```

---

## 质量门禁总结

### 评估阶段

| 指标 | 阈值 | 权重 |
|--------|-----------|--------|
| 基础设施发现率 | >= 98% | 0.35 |
| 误报率 | <= 3% | 0.25 |
| 风险检测率 | >= 95% | 0.25 |
| 成本估算准确性 | >= 85% | 0.15 |

### 规划阶段

| 指标 | 阈值 | 权重 |
|--------|-----------|--------|
| 依赖满意度 | 100% | 0.30 |
| 约束满意度 | 100% | 0.25 |
| 排序优化性 | >= 85% | 0.25 |
| 策略推荐准确性 | >= 85% | 0.20 |

### 执行阶段

| 指标 | 阈值 | 权重 |
|--------|-----------|--------|
| 迁移成功率 | >= 99% | 0.40 |
| 预验证准确性 | >= 95% | 0.20 |
| 回滚成功率 | >= 95% | 0.25 |
| 问题检测率 | >= 90% | 0.15 |

### 验证阶段

| 指标 | 阈值 | 权重 |
|--------|-----------|--------|
| 功能测试通过率 | >= 95% | 0.30 |
| 性能基准匹配 | >= 90% | 0.35 |
| 数据完整性 | 100% | 0.20 |
| 安全验证 | 100% | 0.15 |

---

## 运行云迁移测试

### Python API

```python
from ai_testing_benchmark.migration import CloudMigrationJourneyEvaluator

# 初始化评估器
evaluator = CloudMigrationJourneyEvaluator(
    model="gpt-4",
    provider="openai"
)

# 运行评估阶段测试
assessment_results = evaluator.evaluate_phase(
    phase="assessment",
    test_scenarios=["TC-CM-ASSESS-001", "TC-CM-ASSESS-002", "TC-CM-ASSESS-003"],
    user_inputs=[...],
    verbose=True
)

# 运行规划阶段测试
planning_results = evaluator.evaluate_phase(
    phase="planning",
    test_scenarios=["TC-CM-PLAN-001", "TC-CM-PLAN-002"]
)

# 运行执行阶段测试
execution_results = evaluator.evaluate_phase(
    phase="execution",
    test_scenarios=["TC-CM-EXEC-001", "TC-CM-EXEC-002", "TC-CM-EXEC-003"]
)

# 运行验证阶段测试
validation_results = evaluator.evaluate_phase(
    phase="validation",
    test_scenarios=["TC-CM-VAL-001", "TC-CM-VAL-002"]
)

# 生成综合报告
report = evaluator.generate_migration_report(
    results={
        "assessment": assessment_results,
        "planning": planning_results,
        "execution": execution_results,
        "validation": validation_results
    }
)

print(f"迁移旅程分数: {report['overall_score']}")
print(f"阶段分数: {report['phase_scores']}")
print(f"质量门禁: {report['quality_gates_passed']}")
```

### CLI用法

```bash
# 运行所有迁移阶段测试
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase all

# 运行特定阶段
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase assessment \
    --tests TC-CM-ASSESS-001 TC-CM-ASSESS-002

# 使用自定义场景运行
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase planning \
    --scenarios-file custom_scenarios.json

# 生成报告
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase all \
    --output-format html \
    --output-dir ./results/migration
```

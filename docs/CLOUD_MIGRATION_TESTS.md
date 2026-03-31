# Cloud Migration AI Test Suite

## Overview

This document provides comprehensive test specifications for evaluating AI systems that guide users through cloud migration journeys. The tests are organized by migration phase and cover the complete lifecycle of a migration project.

---

## Migration Journey Phases

```
┌────────────────────────────────────────────────────────────────────┐
│                      CLOUD MIGRATION JOURNEY                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │         │    │         │    │         │    │         │         │
│  │ASSESS-  │───▶│ PLANNING │───▶│EXECUTION│───▶│VALIDA-  │         │
│  │   MENT  │    │         │    │         │    │  TION   │         │
│  │         │    │         │    │         │    │         │         │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘         │
│       │              │              │              │               │
│       ▼              ▼              ▼              ▼               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │Inventory│    │Sequence │    │Automated│    │Functional│         │
│  │Risk ID  │    │Strategy │    │Migration│    │Performance│        │
│  │Cost Est │    │Resource │    │Rollback │    │Security  │        │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Assessment Tests

### 1.1 Infrastructure Discovery

**Objective**: Verify AI can accurately discover and catalog cloud infrastructure resources.

#### TC-CM-ASSESS-001: Server Infrastructure Discovery

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-001",
    "phase": "Assessment",
    "category": "infrastructure_discovery",
    "name": "Server Infrastructure Discovery",
    "description": """
    Evaluates the AI's ability to discover, catalog, and report on
    server infrastructure from user descriptions or data exports.
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "SS-001",
            "scenario_name": "Medium Enterprise Setup",
            "input": {
                "description": """
                We have a typical mid-size e-commerce company:
                - 2 data centers (primary in NYC, DR in Chicago)
                - 100 physical servers (40 Windows, 60 Linux)
                - 150 virtual machines managed by VMware
                - 8 database servers (4 SQL Server, 2 MySQL, 2 PostgreSQL)
                - 15 application servers running Java microservices
                - 10 web servers with Apache and Nginx
                - 5 load balancers (F5 BigIP)
                - 20 switches, 10 routers
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
            "scenario_name": "Complex Microservices Architecture",
            "input": {
                "description": """
                Our platform runs on Kubernetes with:
                - 3 clusters (prod, staging, dev)
                - Each prod cluster: 50 nodes (mixed: 30 compute-optimized, 20 memory-optimized)
                - Staging: 10 nodes
                - Dev: 5 nodes
                - 200 microservices across all environments
                - Each microservice: 2-10 pods (average 4)
                - Services: API Gateway, Auth Service, User Service, Product Service,
                  Order Service, Payment Service, Notification Service, etc.
                - Ingress controllers: 3 (one per cluster)
                - Service mesh: Istio
                - Container registry: Harbor
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

#### TC-CM-ASSESS-002: Dependency Mapping

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-002",
    "phase": "Assessment",
    "category": "dependency_mapping",
    "name": "Application Dependency Identification",
    "description": """
    Evaluates the AI's ability to identify and document dependencies
    between applications, services, and infrastructure components.
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "DM-001",
            "scenario_name": "Three-Tier Web Application",
            "input": {
                "description": """
                Classic three-tier e-commerce architecture:

                WEB TIER:
                - Frontend: React SPA hosted on S3 + CloudFront
                - CDN serving static assets

                APPLICATION TIER:
                - API Gateway: Kong API Gateway
                - Product Service (Java Spring Boot) → port 8080
                - Order Service (Python FastAPI) → port 8000
                - User Service (Node.js Express) → port 3000
                - Payment Service (Go) → port 9090
                - Inventory Service (Rust) → port 8081

                DATA TIER:
                - PostgreSQL: Products, Orders, Users (primary)
                - Redis: Session cache, rate limiting
                - Elasticsearch: Product search
                - S3: Static assets, order documents

                MESSAGE QUEUES:
                - RabbitMQ: Async order processing
                - Kafka: Event streaming for analytics

                DEPENDENCIES:
                - Frontend calls API Gateway
                - API Gateway routes to services
                - Services query PostgreSQL
                - Order Service publishes to RabbitMQ
                - Payment Service reads from RabbitMQ
                - Product Service indexes to Elasticsearch
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
                "cycle_detection": {"threshold": 1.0}  # Must detect cycles if any
            }
        },
        {
            "scenario_id": "DM-002",
            "scenario_name": "Microservices with Circuit Breakers",
            "input": {
                "architecture_diagram": "see test_data/diagrams/microservices.pdf",
                "description": """
                Complex microservices with circuit breaker patterns:

                API Gateway → Auth → Rate Limiter → Service Mesh (Istio)
                    ↓
                [Product Catalog] ←→ [Search Service]
                    ↓                    ↓
                [Inventory]     ←→     [Cache]
                    ↓
                [Orders]  ──→  [Payments]
                    ↓
                [Shipping] ←── [Notifications]

                Each service has:
                - Circuit breaker (Hystrix/Envoy)
                - Retry policies
                - Fallback mechanisms
                - Health check endpoints
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

### 1.2 Risk Identification

#### TC-CM-ASSESS-003: Risk Detection and Classification

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-003",
    "phase": "Assessment",
    "category": "risk_identification",
    "name": "Migration Risk Detection",
    "description": """
    Evaluates the AI's ability to identify, classify, and assess
    risks associated with cloud migration scenarios.
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "RI-001",
            "scenario_name": "Data Sovereignty Risk",
            "input": {
                "description": """
                Financial services company migrating to cloud:

                INFRASTRUCTURE:
                - Customer databases with PII (names, SSNs, financial data)
                - Regulatory requirement: Data must remain in US region
                - Current setup: Multi-region US data centers
                - 15 PB of structured and unstructured data
                - Real-time replication between sites

                COMPLIANCE:
                - SOX, PCI-DSS Level 1, GDPR (for EU customers)
                - Data retention policies: 7 years
                - Annual SOC 2 audits

                STAKEHOLDER CONCERNS:
                - CEO: "We cannot afford any data breach"
                - Legal: "We need to maintain data sovereignty"
                - CTO: "Cloud will save us 30% on infrastructure costs"
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
                        "severity": "HIGH",
                        "probability": 0.70,
                        "impact": "HIGH",
                        "detection_confidence": 0.95
                    },
                    "compliance_violation": {
                        "severity": "CRITICAL",
                        "probability": 0.60,
                        "impact": "CRITICAL",
                        "detection_confidence": 0.92
                    },
                    "security_breach": {
                        "severity": "HIGH",
                        "probability": 0.40,
                        "impact": "CRITICAL",
                        "detection_confidence": 0.88
                    },
                    "cost_overrun": {
                        "severity": "MEDIUM",
                        "probability": 0.50,
                        "impact": "MEDIUM",
                        "detection_confidence": 0.85
                    }
                },
                "mitigation_strategies_provided": True,
                "risk_register_complete": True
            }
        },
        {
            "scenario_id": "RI-002",
            "scenario_name": "Legacy Application Dependencies",
            "input": {
                "description": """
                Manufacturing company with legacy systems:

                LEGACY INFRASTRUCTURE:
                - 30-year-old ERP system (AS/400, COBOL)
                - Custom batch processing jobs running since 1995
                - Integration via flat file exchanges
                - No API layer, direct database connections

                MODERN SYSTEMS:
                - Salesforce CRM
                - SAP S/4HANA
                - Custom MES system

                INTEGRATION CHALLENGES:
                - AS/400 communicates via MQSeries
                - File-based batch jobs run daily at 2 AM
                - Some COBOL programs read from DB2

                TEAM CAPABILITIES:
                - 5 COBOL developers (all >50 years old, retiring in 5 years)
                - No documentation for 40% of legacy code
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
                    "severity": "HIGH",
                    "detection_confidence": 0.93
                },
                "skill_gap_risk": {
                    "severity": "MEDIUM",
                    "detection_confidence": 0.88
                },
                "documentation_risk": {
                    "severity": "HIGH",
                    "detection_confidence": 0.85
                },
                "migration_strategy_impact": "Refactor or Re-platform recommended"
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

### 1.3 Cost Estimation

#### TC-CM-ASSESS-004: Cloud Cost Estimation Accuracy

```python
TEST_CASE = {
    "id": "TC-CM-ASSESS-004",
    "phase": "Assessment",
    "category": "cost_estimation",
    "name": "Migration Cost Estimation",
    "description": """
    Evaluates the AI's ability to estimate cloud migration costs
    including infrastructure, migration, and operational expenses.
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "CE-001",
            "scenario_name": "Medium Enterprise AWS Migration",
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
                "current_monthly_cost": "$45,000 (on-premise)",
                "migration_type": "lift_and_shift_initial",
                "target_provider": "AWS",
                "assumptions_provided": True
            },
            "expected_outputs": {
                "monthly_aws_cost": {
                    "expected_range": [32000, 45000],  # Based on AWS pricing
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
            "scenario_name": "Cost Comparison Multi-Provider",
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

## Phase 2: Planning Tests

### 2.1 Sequencing Optimization

#### TC-CM-PLAN-001: Migration Order Optimization

```python
TEST_CASE = {
    "id": "TC-CM-PLAN-001",
    "phase": "Planning",
    "category": "sequencing_optimization",
    "name": "Migration Sequence Optimization",
    "description": """
    Evaluates the AI's ability to determine optimal migration order
    considering dependencies, risks, resources, and business constraints.
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "SEQ-001",
            "scenario_name": "E-commerce Platform Migration",
            "input": {
                "applications": [
                    {"id": "APP-001", "name": "User Auth Service", "dependencies": [], "risk": "LOW"},
                    {"id": "APP-002", "name": "Product Catalog", "dependencies": [], "risk": "LOW"},
                    {"id": "APP-003", "name": "Search Service", "dependencies": ["APP-002"], "risk": "MEDIUM"},
                    {"id": "APP-004", "name": "Shopping Cart", "dependencies": ["APP-001", "APP-003"], "risk": "MEDIUM"},
                    {"id": "APP-005", "name": "Order Processing", "dependencies": ["APP-001", "APP-004"], "risk": "HIGH"},
                    {"id": "APP-006", "name": "Payment Service", "dependencies": ["APP-001"], "risk": "CRITICAL"},
                    {"id": "APP-007", "name": "Inventory Management", "dependencies": ["APP-003"], "risk": "MEDIUM"},
                    {"id": "APP-008", "name": "Shipping Integration", "dependencies": ["APP-005"], "risk": "LOW"},
                    {"id": "APP-009", "name": "Email Service", "dependencies": [], "risk": "LOW"},
                    {"id": "APP-010", "name": "Analytics Pipeline", "dependencies": ["APP-005", "APP-007"], "risk": "LOW"},
                ],
                "constraints": {
                    "max_concurrent_migrations": 2,
                    "business_freeze_dates": ["2024-12-20", "2024-12-31"],
                    "team_capacity": 5,
                    "must_complete_by": "2024-06-30"
                },
                "migration_strategies": {
                    "APP-001": "Rehost",
                    "APP-002": "Rehost",
                    "APP-003": "Refactor",
                    "APP-004": "Replatform",
                    "APP-005": "Refactor",
                    "APP-006": "Refactor",
                    "APP-007": "Replatform",
                    "APP-008": "Rehost",
                    "APP-009": "Rehost",
                    "APP-010": "Rehost"
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
            "scenario_name": "Database-First Migration Strategy",
            "input": {
                "applications": [
                    {"id": "DB-001", "name": "Customer DB (PostgreSQL)", "dependencies": [], "size_tb": 5},
                    {"id": "DB-002", "name": "Order DB (MongoDB)", "dependencies": [], "size_tb": 2},
                    {"id": "DB-003", "name": "Analytics DB (ClickHouse)", "dependencies": [], "size_tb": 10},
                    {"id": "SVC-001", "name": "Customer API", "dependencies": ["DB-001"], "risk": "HIGH"},
                    {"id": "SVC-002", "name": "Order Service", "dependencies": ["DB-002"], "risk": "HIGH"},
                    {"id": "SVC-003", "name": "Analytics Service", "dependencies": ["DB-003"], "risk": "MEDIUM"},
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

### 2.2 Strategy Recommendation

#### TC-CM-PLAN-002: Migration Strategy Selection

```python
TEST_CASE = {
    "id": "TC-CM-PLAN-002",
    "phase": "Planning",
    "category": "strategy_recommendation",
    "name": "Migration Strategy Recommendation",
    "description": """
    Evaluates the AI's ability to recommend appropriate migration
    strategies (Rehost, Replatform, Refactor, etc.) based on
    application characteristics and business requirements.
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "STR-001",
            "scenario_name": "Application Portfolio Strategy Mix",
            "input": {
                "applications": [
                    {
                        "id": "APP-001",
                        "name": "Legacy monolith ERP",
                        "characteristics": {
                            "age_years": 15,
                            "tech_stack": "Java 8, WAS 8.5, DB2",
                            "architecture": "monolithic",
                            "change_frequency": "quarterly",
                            "technical_debt": "HIGH",
                            "team_familiarity": "LOW",
                            "business_criticality": "CRITICAL",
                            "scaling_needs": "MODERATE",
                            "customizations": "EXTENSIVE"
                        }
                    },
                    {
                        "id": "APP-002",
                        "name": "Customer Portal",
                        "characteristics": {
                            "age_years": 3,
                            "tech_stack": "Node.js, React, PostgreSQL",
                            "architecture": "microservices",
                            "change_frequency": "weekly",
                            "technical_debt": "LOW",
                            "team_familiarity": "HIGH",
                            "business_criticality": "HIGH",
                            "scaling_needs": "HIGH",
                            "customizations": "MINIMAL"
                        }
                    },
                    {
                        "id": "APP-003",
                        "name": "Batch Processing System",
                        "characteristics": {
                            "age_years": 8,
                            "tech_stack": "COBOL, VSAM, JCL",
                            "architecture": "mainframe",
                            "change_frequency": "rarely",
                            "technical_debt": "MEDIUM",
                            "team_familiarity": "VERY_LOW",
                            "business_criticality": "MEDIUM",
                            "scaling_needs": "LOW",
                            "customizations": "MODERATE"
                        }
                    },
                    {
                        "id": "APP-004",
                        "name": "Real-time Analytics Dashboard",
                        "characteristics": {
                            "age_years": 1,
                            "tech_stack": "Python, Kafka, Elastic",
                            "architecture": "event-driven",
                            "change_frequency": "daily",
                            "technical_debt": "LOW",
                            "team_familiarity": "HIGH",
                            "business_criticality": "MEDIUM",
                            "scaling_needs": "VERY_HIGH",
                            "customizations": "MINIMAL"
                        }
                    }
                ]
            },
            "expected_outputs": {
                "APP-001": {
                    "recommended_strategy": "Refactor",
                    "alternative_strategy": "Replatform",
                    "rationale": "High technical debt, low team familiarity, extensive customizations justify refactoring to modern stack",
                    "estimated_timeline_months": {"range": [12, 18]},
                    "estimated_cost": {"range": [1500000, 2500000]}
                },
                "APP-002": {
                    "recommended_strategy": "Rehost",
                    "alternative_strategy": "None",
                    "rationale": "Modern stack, low debt, high team familiarity - quick win via rehost",
                    "estimated_timeline_months": {"range": [1, 2]}
                },
                "APP-003": {
                    "recommended_strategy": "Retain/Rehost",
                    "alternative_strategy": "Replatform",
                    "rationale": "Mainframe batch processing - consider retiring or minimal changes",
                    "estimated_timeline_months": {"range": [3, 6]}
                },
                "APP-004": {
                    "recommended_strategy": "Refactor",
                    "alternative_strategy": "Native Cloud Services",
                    "rationale": "Already cloud-ready architecture, refactor to managed services for cost efficiency",
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

## Phase 3: Execution Tests

### 3.1 Automated Migration

#### TC-CM-EXEC-001: Pre-Migration Validation

```python
TEST_CASE = {
    "id": "TC-CM-EXEC-001",
    "phase": "Execution",
    "category": "pre_migration_validation",
    "name": "Pre-Migration Environment Validation",
    "description": """
    Evaluates the AI's ability to perform comprehensive pre-migration
    validation including connectivity, permissions, and prerequisites.
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "PRE-001",
            "scenario_name": "Multi-Tier Application Pre-Check",
            "input": {
                "migration_task": {
                    "source": "on-premise vmware",
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
                        "status": "PASS",
                        "details": "VPN configured, VPC peering ready"
                    },
                    "iam_permissions": {
                        "status": "PASS",
                        "details": "Migration role has required permissions"
                    },
                    "subnet_availability": {
                        "status": "PASS",
                        "available_azs": ["us-east-1a", "us-east-1b", "us-east-1c"]
                    },
                    "security_group_rules": {
                        "status": "WARNING",
                        "details": "Port 3389 RDP needs adjustment for production"
                    },
                    "storage_capacity": {
                        "status": "PASS",
                        "available_iops": 30000
                    },
                    "instance_quota": {
                        "status": "PASS",
                        "available_count": 50
                    }
                },
                "overall_status": "PASS_WITH_WARNINGS",
                "warnings_count": 1,
                "blocking_issues": [],
                "recommendations": ["Update security group before cutover"]
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

#### TC-CM-EXEC-002: Migration Execution Monitoring

```python
TEST_CASE = {
    "id": "TC-CM-EXEC-002",
    "phase": "Execution",
    "category": "migration_monitoring",
    "name": "Real-time Migration Progress Monitoring",
    "description": """
    Evaluates the AI's ability to monitor migration progress,
    detect issues, and provide real-time status updates.
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
            "scenario_name": "Normal Migration Progress",
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
                "status": "ON_TRACK",
                "health_score": {"min": 85}
            }
        },
        {
            "scenario_id": "MON-002",
            "scenario_name": "Migration with Failures",
            "input": {
                "elapsed_time_minutes": 90,
                "completed_vms": 20,
                "failed_vms": 3,
                "failed_vm_ids": ["WEB-03", "APP-05", "DB-02"],
                "replication_throughput_mbps": 380,
                "current_phase": "replication",
                "errors_logged": [
                    {"vm": "WEB-03", "error": "Storage timeout", "timestamp": "T+85"},
                    {"vm": "APP-05", "error": "Network partition", "timestamp": "T+88"},
                    {"vm": "DB-02", "error": "Checksum mismatch", "timestamp": "T+89"}
                ]
            },
            "expected_outputs": {
                "status": "DEGRADED",
                "failure_impact_analysis": {
                    "WEB-03": {"severity": "LOW", "retry_recommended": True},
                    "APP-05": {"severity": "MEDIUM", "retry_recommended": True},
                    "DB-02": {"severity": "HIGH", "manual_intervention_required": True}
                },
                "updated_estimated_completion": {"expected_range": [150, 200]},
                "recovery_recommendations": [
                    "Retry WEB-03 and APP-05 automatically",
                    "Investigate DB-02 storage subsystem",
                    "Consider reducing replication parallelism"
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

### 3.2 Rollback Capability

#### TC-CM-EXEC-003: Rollback Trigger and Execution

```python
TEST_CASE = {
    "id": "TC-CM-EXEC-003",
    "phase": "Execution",
    "category": "rollback",
    "name": "Migration Rollback Capability",
    "description": """
    Evaluates the AI's ability to determine when rollback is needed,
    execute rollback procedures, and validate successful rollback.
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "RB-001",
            "scenario_name": "Critical Failure Rollback",
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
                            "affected_services": ["Order Service", "Payment Service", "User Service"],
                            "service_impact": "CRITICAL",
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
                        "risk": "LOW"
                    },
                    {
                        "type": "targeted_rollback",
                        "duration_minutes": 20,
                        "data_loss_mb": 1500,
                        "affected_services": ["DB-PRIMARY"],
                        "risk": "MEDIUM"
                    }
                ]
            },
            "expected_outputs": {
                "rollback_decision": {
                    "recommended": "targeted_rollback",
                    "rationale": "Critical production impact, 25 min downtime, 5 min to RTO",
                    "decision_time_seconds": {"max": 30}
                },
                "rollback_plan": {
                    "type": "targeted_rollback",
                    "sequence": [
                        "Stop all write operations to DB-PRIMARY",
                        "Revert DB-PRIMARY to T-35 checkpoint",
                        "Restore network connectivity",
                        "Verify service dependencies",
                        "Resume services in order: Auth → Order → Payment"
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
                    "services_restored": ["Auth", "Order", "Payment"],
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

## Phase 4: Validation Tests

### 4.1 Functional Validation

#### TC-CM-VAL-001: Post-Migration Functional Verification

```python
TEST_CASE = {
    "id": "TC-CM-VAL-001",
    "phase": "Validation",
    "category": "functional_validation",
    "name": "Post-Migration Functional Tests",
    "description": """
    Evaluates the AI's ability to execute and interpret post-migration
    functional validation tests.
    """,
    "difficulty": "medium",
    "test_scenarios": [
        {
            "scenario_id": "FUNC-001",
            "scenario_name": "Web Application Functional Validation",
            "input": {
                "migrated_application": "E-commerce Platform",
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
                "overall_status": "PASS",
                "test_pass_rate": 100.0,
                "functional_equivalence_score": {"min": 95},
                "issues_found": [],
                "deployment_ready": True
            }
        },
        {
            "scenario_id": "FUNC-002",
            "scenario_name": "API Contract Validation",
            "input": {
                "api_service": "User Management API",
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

### 4.2 Performance Validation

#### TC-CM-VAL-002: Post-Migration Performance Benchmark

```python
TEST_CASE = {
    "id": "TC-CM-VAL-002",
    "phase": "Validation",
    "category": "performance_validation",
    "name": "Performance Against Pre-Migration Baselines",
    "description": """
    Validates that migrated workloads meet or exceed pre-migration
    performance benchmarks.
    """,
    "difficulty": "high",
    "test_scenarios": [
        {
            "scenario_id": "PERF-001",
            "scenario_name": "Web Application Performance",
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
                    "response_time_improvement": {"expected_min": 0.10},  # 10% improvement
                    "throughput_improvement": {"expected_min": 0.15},  # 15% improvement
                    "error_rate_improvement": {"expected_min": 0.10},  # 10% improvement
                    "resource_efficiency_improvement": {"expected_min": 0.15}
                },
                "validation_status": "PASS",
                "performance_gain_percentage": {"expected_range": [10, 30]},
                "optimization_recommendations": []  # Only if underperforming
            }
        },
        {
            "scenario_id": "PERF-002",
            "scenario_name": "Database Performance Regression",
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
                "regression_severity": "MEDIUM",
                "affected_queries": [
                    "complex_aggregation_queries",
                    "multi_join_queries"
                ],
                "root_cause_hypothesis": [
                    "New instance not optimized for workload pattern",
                    "Cache warming period not complete",
                    "Index statistics may need update"
                ],
                "recommendations": [
                    "Run ANALYZE on database",
                    "Review query execution plans",
                    "Consider instance type adjustment",
                    "Pre-warm cache with common queries"
                ],
                "validation_status": "CONDITIONAL_PASS"
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

## Quality Gates Summary

### Assessment Phase

| Metric | Threshold | Weight |
|--------|-----------|--------|
| Infrastructure Discovery Rate | >= 98% | 0.35 |
| False Positive Rate | <= 3% | 0.25 |
| Risk Detection Rate | >= 95% | 0.25 |
| Cost Estimation Accuracy | >= 85% | 0.15 |

### Planning Phase

| Metric | Threshold | Weight |
|--------|-----------|--------|
| Dependency Satisfaction | 100% | 0.30 |
| Constraint Satisfaction | 100% | 0.25 |
| Sequencing Optimality | >= 85% | 0.25 |
| Strategy Recommendation Accuracy | >= 85% | 0.20 |

### Execution Phase

| Metric | Threshold | Weight |
|--------|-----------|--------|
| Migration Success Rate | >= 99% | 0.40 |
| Pre-validation Accuracy | >= 95% | 0.20 |
| Rollback Success Rate | >= 95% | 0.25 |
| Issue Detection Rate | >= 90% | 0.15 |

### Validation Phase

| Metric | Threshold | Weight |
|--------|-----------|--------|
| Functional Test Pass Rate | >= 95% | 0.30 |
| Performance Baseline Match | >= 90% | 0.35 |
| Data Integrity | 100% | 0.20 |
| Security Validation | 100% | 0.15 |

---

## Running Cloud Migration Tests

### Python API

```python
from ai_testing_benchmark.migration import CloudMigrationJourneyEvaluator

# Initialize evaluator
evaluator = CloudMigrationJourneyEvaluator(
    model="gpt-4",
    provider="openai"
)

# Run Assessment Phase tests
assessment_results = evaluator.evaluate_phase(
    phase="assessment",
    test_scenarios=["TC-CM-ASSESS-001", "TC-CM-ASSESS-002", "TC-CM-ASSESS-003"],
    user_inputs=[...],
    verbose=True
)

# Run Planning Phase tests
planning_results = evaluator.evaluate_phase(
    phase="planning",
    test_scenarios=["TC-CM-PLAN-001", "TC-CM-PLAN-002"]
)

# Run Execution Phase tests
execution_results = evaluator.evaluate_phase(
    phase="execution",
    test_scenarios=["TC-CM-EXEC-001", "TC-CM-EXEC-002", "TC-CM-EXEC-003"]
)

# Run Validation Phase tests
validation_results = evaluator.evaluate_phase(
    phase="validation",
    test_scenarios=["TC-CM-VAL-001", "TC-CM-VAL-002"]
)

# Generate comprehensive report
report = evaluator.generate_migration_report(
    results={
        "assessment": assessment_results,
        "planning": planning_results,
        "execution": execution_results,
        "validation": validation_results
    }
)

print(f"Migration Journey Score: {report['overall_score']}")
print(f"Phase Scores: {report['phase_scores']}")
print(f"Quality Gates: {report['quality_gates_passed']}")
```

### CLI Usage

```bash
# Run all migration phase tests
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase all

# Run specific phase
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase assessment \
    --tests TC-CM-ASSESS-001 TC-CM-ASSESS-002

# Run with custom scenarios
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase planning \
    --scenarios-file custom_scenarios.json

# Generate report
python -m ai_testing_benchmark migration \
    --model gpt-4 \
    --phase all \
    --output-format html \
    --output-dir ./results/migration
```

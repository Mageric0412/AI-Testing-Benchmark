# AI Testing Benchmark - Evaluation Framework Guide

## Table of Contents

1. [Overview](#overview)
2. [Five-Layer Architecture](#five-layer-architecture)
3. [Foundation Model Evaluation](#foundation-model-evaluation)
4. [Conversational AI Evaluation](#conversational-ai-evaluation)
5. [Cloud Migration Journey Evaluation](#cloud-migration-journey-evaluation)
6. [Safety & Alignment Evaluation](#safety--alignment-evaluation)
7. [Performance Evaluation](#performance-evaluation)
8. [Scoring Methodology](#scoring-methodology)
9. [Running Evaluations](#running-evaluations)

---

## Overview

AI-Testing-Benchmark implements a comprehensive five-layer evaluation framework designed specifically for AI systems that guide users through cloud migration journeys. Each layer addresses critical aspects of AI capability assessment.

### Design Principles

1. **Domain Specificity**: Tailored for cloud migration AI assistants
2. **Measurability**: All metrics are quantifiable and reproducible
3. **Graduated Coverage**: From basic language abilities to complex domain tasks
4. **Safety First**: Strong emphasis on safety and alignment testing
5. **Production Ready**: Suitable for CI/CD integration

---

## Five-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 5: PERFORMANCE                         │
│         Latency, Throughput, Scalability, Cost                  │
├─────────────────────────────────────────────────────────────────┤
│                    LAYER 4: SAFETY & ALIGNMENT                 │
│      Security, Fairness, Truthfulness, Robustness               │
├─────────────────────────────────────────────────────────────────┤
│                 LAYER 3: CLOUD MIGRATION AI                     │
│   Assessment, Planning, Execution, Validation, Optimization     │
├─────────────────────────────────────────────────────────────────┤
│                   LAYER 2: CONVERSATIONAL AI                    │
│    Intent Recognition, Entity Extraction, Dialogue Flow,        │
│                    Response Quality                             │
├─────────────────────────────────────────────────────────────────┤
│                  LAYER 1: FOUNDATION MODEL                      │
│        Language Understanding, Reasoning, Generation             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Foundation Model Evaluation

### 1.1 Language Understanding

#### Test Categories

| Category | Description | Metrics |
|----------|-------------|---------|
| Text Classification | Categorize input text into predefined classes | Accuracy, F1 (macro/weighted) |
| Named Entity Recognition | Extract structured entities from text | Entity F1, Precision, Recall |
| Sentiment Analysis | Detect positive/negative/neutral sentiment | Accuracy, F1 per class |
| Semantic Similarity | Measure semantic closeness between texts | Cosine similarity, Spearman correlation |
| Natural Language Inference | Determine entailment/contradiction/neutral | Accuracy |

#### Example Test Cases

**TC-FU-001: Text Classification - Infrastructure Type Detection**

```python
"""
Test Case: TC-FU-001
Category: Text Classification
Objective: Evaluate model's ability to classify cloud infrastructure descriptions
"""

TEST_CASE = {
    "id": "TC-FU-001",
    "name": "Infrastructure Type Classification",
    "category": "text_classification",
    "description": """
    Evaluates the model's ability to correctly classify cloud infrastructure
    descriptions into appropriate categories (IaaS, PaaS, SaaS, FaaS, etc.)
    """,
    "test_data": [
        {
            "input": "We have 50 virtual machines running Ubuntu and Windows Server, "
                    "with manual scaling based on traffic patterns.",
            "expected_category": "IaaS",
            "confidence_range": (0.85, 1.0)
        },
        {
            "input": "Our development team uses managed Kubernetes pods with built-in "
                    "load balancing and automatic container orchestration.",
            "expected_category": "CaaS/Kubernetes",
            "confidence_range": (0.80, 1.0)
        },
        {
            "input": "Employees access Salesforce CRM through browsers for customer "
                    "relationship management with no local installation required.",
            "expected_category": "SaaS",
            "confidence_range": (0.90, 1.0)
        },
        {
            "input": "The application runs on AWS Lambda functions triggered by API "
                    "Gateway events, processing images on-demand.",
            "expected_category": "FaaS",
            "confidence_range": (0.85, 1.0)
        }
    ],
    "evaluation_criteria": {
        "accuracy": {"threshold": 0.90, "weight": 0.4},
        "f1_weighted": {"threshold": 0.88, "weight": 0.3},
        "avg_confidence_accuracy": {"threshold": 0.15, "weight": 0.15},  # conf diff
        "rejection_quality": {"threshold": 0.05, "weight": 0.15}  # low conf handling
    },
    "pass_threshold": 0.85,
    "fail_threshold": 0.75,
    "datasets": ["20newsgroups", "custom_infrastructure_corpus"],
    "reference": "NIST SP 500-332"
}
```

**TC-FU-002: Named Entity Recognition - Cloud Resource Extraction**

```python
"""
Test Case: TC-FU-002
Category: Named Entity Recognition
Objective: Extract cloud resources and their attributes from natural language
"""

TEST_CASE = {
    "id": "TC-FU-002",
    "name": "Cloud Resource Entity Extraction",
    "category": "ner",
    "description": """
    Evaluates the model's ability to identify and extract cloud resource
    entities (VMs, databases, storage, networks) with their attributes
    (region, size, configuration) from unstructured text.
    """,
    "entity_types": [
        "RESOURCE_TYPE",  # VM, Database, Storage, LoadBalancer, etc.
        "PROVIDER",       # AWS, Azure, GCP, On-premise
        "REGION",         # us-east-1, westus2, etc.
        "SIZE",           # small, medium, large, t2.micro, etc.
        "STATUS",         # running, stopped, maintenance
        "TECHNOLOGY"     # PostgreSQL, Kubernetes, Docker, etc.
    ],
    "test_data": [
        {
            "text": "We have three m5.large EC2 instances in us-east-1 running "
                    "Ubuntu 22.04, connected to an RDS PostgreSQL database "
                    "in us-east-1b with 100GB storage.",
            "expected_entities": [
                {"type": "RESOURCE_TYPE", "value": "EC2 instances", "start": 12, "end": 27},
                {"type": "SIZE", "value": "m5.large", "start": 28, "end": 36},
                {"type": "PROVIDER", "value": "AWS", "start": 40, "end": 43},
                {"type": "REGION", "value": "us-east-1", "start": 47, "end": 56},
                {"type": "RESOURCE_TYPE", "value": "RDS PostgreSQL database", "start": 95, "end": 119},
                {"type": "TECHNOLOGY", "value": "PostgreSQL", "start": 120, "end": 130},
                {"type": "REGION", "value": "us-east-1b", "start": 139, "end": 149},
                {"type": "SIZE", "value": "100GB", "start": 159, "end": 164}
            ]
        },
        {
            "text": "Our Kubernetes cluster on Azure has 5 node pools of size Standard_D4s_v3 "
                    "running AKS version 1.28.",
            "expected_entities": [
                {"type": "RESOURCE_TYPE", "value": "Kubernetes cluster", "start": 5, "end": 23},
                {"type": "PROVIDER", "value": "Azure", "start": 29, "end": 34},
                {"type": "SIZE", "value": "Standard_D4s_v3", "start": 53, "end": 68},
                {"type": "TECHNOLOGY", "value": "AKS", "start": 85, "end": 88}
            ]
        }
    ],
    "evaluation_criteria": {
        "entity_f1": {"threshold": 0.90, "weight": 0.40},
        "entity_precision": {"threshold": 0.88, "weight": 0.25},
        "entity_recall": {"threshold": 0.88, "weight": 0.25},
        "type_accuracy": {"threshold": 0.92, "weight": 0.10}
    },
    "pass_threshold": 0.88,
    "fail_threshold": 0.80,
    "datasets": ["CoNLL-2003", "custom_cloud_resource_corpus"]
}
```

**TC-FU-003: Sentiment Analysis - User Feedback Analysis**

```python
TEST_CASE = {
    "id": "TC-FU-003",
    "name": "Migration Sentiment Analysis",
    "category": "sentiment_analysis",
    "description": """
    Evaluates the model's ability to detect sentiment in user feedback
    related to cloud migration experiences, including technical frustration,
    satisfaction, and concerns.
    """,
    "test_data": [
        {
            "text": "The migration to AWS was smoother than expected. "
                    "Our team is impressed with the performance improvements.",
            "expected_sentiment": "positive",
            "expected_scores": {"positive": 0.92, "neutral": 0.05, "negative": 0.03}
        },
        {
            "text": "We're experiencing constant connection drops after migrating "
                    "to the new database. This is affecting our production environment.",
            "expected_sentiment": "negative",
            "expected_scores": {"positive": 0.02, "neutral": 0.08, "negative": 0.90}
        },
        {
            "text": "The migration window has been scheduled for next weekend. "
                    "We need to complete the testing by Friday.",
            "expected_sentiment": "neutral",
            "expected_scores": {"positive": 0.05, "neutral": 0.90, "negative": 0.05}
        }
    ],
    "evaluation_criteria": {
        "accuracy": {"threshold": 0.88, "weight": 0.35},
        "f1_macro": {"threshold": 0.85, "weight": 0.25},
        "f1_positive": {"threshold": 0.88, "weight": 0.20},
        "f1_negative": {"threshold": 0.85, "weight": 0.20}
    },
    "pass_threshold": 0.85
}
```

---

### 1.2 Reasoning Capabilities

#### Test Categories

| Category | Description | Metrics |
|----------|-------------|---------|
| Mathematical Reasoning | Solve math problems with steps | Accuracy, Pass@K |
| Logical Deduction | Draw conclusions from premises | Accuracy |
| Common Sense Reasoning | Apply everyday knowledge | Accuracy, HellaSwag |
| Chain-of-Thought | Generate reasoning steps | Step Accuracy, Coherence |

#### Example Test Cases

**TC-RE-001: Mathematical Reasoning - Cost Estimation**

```python
TEST_CASE = {
    "id": "TC-RE-001",
    "name": "Cloud Cost Mathematical Reasoning",
    "category": "mathematical_reasoning",
    "description": """
    Evaluates the model's ability to perform multi-step mathematical
    reasoning for cloud cost calculations, including reserved instances,
    savings plans, and tiered pricing.
    """,
    "test_data": [
        {
            "problem": """
            A company uses 50 t3.medium instances running 24/7 in us-east-1.
            On-demand pricing is $0.0416/hour per instance.
            They are considering a 1-year Reserved Instance with upfront payment
            at $0.0224/hour (72% savings).

            1. Calculate the annual on-demand cost
            2. Calculate the annual Reserved Instance cost
            3. Calculate the annual savings
            4. What is the break-even point in months?

            Show your reasoning step by step.
            """,
            "expected_steps": [
                "Calculate annual on-demand: 50 × $0.0416 × 24 × 365 = $18,412.80",
                "Calculate annual RI cost: 50 × $0.0224 × 24 × 365 = $9,820.80",
                "Calculate savings: $18,412.80 - $9,820.80 = $8,592.00",
                "Monthly savings: $8,592.00 / 12 = $716.00",
                "One-time RI payment: $9,820.80",
                "Break-even: $9,820.80 / $716.00 ≈ 13.7 months → Month 14"
            ],
            "expected_answers": {
                "on_demand_annual": 18412.80,
                "ri_annual": 9820.80,
                "savings": 8592.00,
                "break_even_month": 14
            },
            "partial_credit": True  # Allow partial credit for partial correct steps
        },
        {
            "problem": """
            Data transfer costs:
            - First 10 TB/month: $0.09/GB
            - Next 40 TB/month: $0.085/GB
            - Over 50 TB/month: $0.07/GB

            If a company transfers 75 TB in a month, calculate:
            1. Cost for first 10 TB
            2. Cost for next 40 TB
            3. Cost for remaining 25 TB
            4. Total cost

            (Note: 1 TB = 1024 GB)
            """,
            "expected_answers": {
                "tier1_cost": 10 * 1024 * 0.09,  # $921.60
                "tier2_cost": 40 * 1024 * 0.085,  # $3,512.32
                "tier3_cost": 25 * 1024 * 0.07,  # $1,792.00
                "total_cost": 921.60 + 3512.32 + 1792.00  # $6,225.92
            }
        }
    ],
    "evaluation_criteria": {
        "final_answer_accuracy": {"threshold": 0.95, "weight": 0.50},
        "step_accuracy": {"threshold": 0.85, "weight": 0.30},
        "reasoning_coherence": {"threshold": 0.80, "weight": 0.20}
    },
    "pass_threshold": 0.88,
    "datasets": ["GSM8K", "custom_cloud_math_problems"]
}
```

**TC-RE-002: Logical Deduction - Dependency Resolution**

```python
TEST_CASE = {
    "id": "TC-RE-002",
    "name": "Infrastructure Dependency Logical Deduction",
    "category": "logical_reasoning",
    "description": """
    Evaluates the model's ability to deduce correct migration order
    based on dependency constraints between services and infrastructure.
    """,
    "test_data": [
        {
            "scenario": """
            Given the following infrastructure dependencies:
            - Database (DB) must be migrated before Application (APP)
            - Load Balancer (LB) must be operational before Web Server (WEB)
            - APP depends on both DB and Cache
            - Cache can be migrated independently
            - WEB depends on APP
            - Monitoring (MON) can be set up anytime

            Question 1: What is the valid migration order?
            Question 2: Identify the critical path (longest dependency chain)
            Question 3: What is the minimum number of sequential migration groups?
            """,
            "expected_answers": {
                "migration_order": ["Cache", "DB", "APP", "WEB", "LB", "MON"],
                "critical_path": ["DB", "APP", "WEB", "LB"],
                "sequential_groups": 4
            },
            "alternative_valid_orders": [
                # Any order that respects dependencies
                ["Cache", "DB", "APP", "LB", "WEB", "MON"],
                ["Cache", "DB", "APP", "WEB", "LB", "MON"]  # LB and WEB could swap if LB doesn't depend on WEB
            ]
        }
    ],
    "evaluation_criteria": {
        "order_correctness": {"threshold": 1.0, "weight": 0.40},  # Must be exactly correct
        "dependency_respected": {"threshold": 1.0, "weight": 0.35},  # All dependencies met
        "critical_path_identification": {"threshold": 0.90, "weight": 0.25}
    },
    "pass_threshold": 0.90
}
```

---

### 1.3 Generation Capabilities

#### Test Categories

| Category | Description | Metrics |
|----------|-------------|---------|
| Text Generation | Coherent, relevant text generation | BLEU, ROUGE, BERTScore |
| Code Generation | Generate valid, efficient code | Pass@K, HumanEval |
| Creative Writing | Generate novel, creative content | Human evaluation |
| Summarization | Condense information accurately | ROUGE-L, Factuality |

#### Example Test Cases

**TC-GN-001: Code Generation - Infrastructure as Code**

```python
TEST_CASE = {
    "id": "TC-GN-001",
    "name": "Terraform Code Generation",
    "category": "code_generation",
    "description": """
    Evaluates the model's ability to generate valid Terraform code
    for cloud infrastructure provisioning based on requirements.
    """,
    "test_data": [
        {
            "requirement": """
            Generate Terraform code to create:
            1. A VPC with CIDR 10.0.0.0/16 in us-east-1
            2. Two public subnets in different availability zones
            3. An Internet Gateway attached to the VPC
            4. A route table with default route to the IGW
            5. Associate route table with both subnets

            Use appropriate naming conventions and tags.
            """,
            "expected_components": [
                "resource \"aws_vpc\"",
                "resource \"aws_subnet\"",
                "resource \"aws_internet_gateway\"",
                "resource \"aws_route_table\"",
                "resource \"aws_route\"",
                "resource \"aws_route_table_association\"",
                "cidr_block = \"10.0.0.0/16\"",
                "availability_zone",
                "tags"
            ],
            "validation_checks": [
                "syntax_valid",  # Terraform validate passes
                "resources_complete",  # All 5 resource types present
                "dependencies_correct",  # IGW attached to VPC, routes target IGW
                "subnets_different_az",  # Two different AZs
                "naming_convention"  # Follows terraform naming conventions
            ]
        },
        {
            "requirement": """
            Create an AWS Lambda function with:
            - Runtime: Python 3.11
            - Handler: index.handler
            - Memory: 256 MB
            - Timeout: 30 seconds
            - Environment variables: REGION, TABLE_NAME
            - IAM role with basic execution permissions
            """,
            "expected_components": [
                "aws_lambda_function",
                "runtime = \"python3.11\"",
                "handler = \"index.handler\"",
                "memory_size = 256",
                "timeout = 30",
                "environment",
                "aws_iam_role",
                "aws_iam_policy"
            ]
        }
    ],
    "evaluation_criteria": {
        "syntax_validity": {"threshold": 1.0, "weight": 0.20},
        "component_completeness": {"threshold": 0.95, "weight": 0.30},
        "functional_correctness": {"threshold": 0.90, "weight": 0.30},
        "best_practices_adherence": {"threshold": 0.85, "weight": 0.20}
    },
    "pass_threshold": 0.88,
    "datasets": ["HumanEval", "custom_terraform_corpus"]
}
```

**TC-GN-002: Summarization - Migration Report Generation**

```python
TEST_CASE = {
    "id": "TC-GN-002",
    "name": "Migration Assessment Report Summarization",
    "category": "summarization",
    "description": """
    Evaluates the model's ability to generate clear, accurate summaries
    of migration assessment reports while preserving key findings.
    """,
    "test_data": [
        {
            "source_text": """
            ASSESSMENT SUMMARY - Project CloudLift

            INFRASTRUCTURE OVERVIEW:
            Current State: 120 VMs across 3 data centers (NYC, LA, Chicago)
            - Production: 60 VMs (Windows Server 2019, RHEL 8)
            - Development: 40 VMs (Ubuntu 22.04)
            - Testing: 20 VMs (Mixed)

            WORKLOAD ANALYSIS:
            - Database Servers: 15 (SQL Server, PostgreSQL, MongoDB)
            - Web Servers: 30 (IIS, Apache, Nginx)
            - Application Servers: 45 (Java Spring Boot, Node.js)
            - Cache Servers: 12 (Redis, Memcached)
            - Message Queues: 8 (RabbitMQ, Kafka)

            MIGRATION RECOMMENDATION:
            Re-architect 30% of workloads (microservices) to containers
            Re-platform 50% to managed services (RDS, ElastiCache)
            Rehost 20% with minimal changes (lift-and-shift)

            RISK FACTORS:
            - High: Data sovereignty requirements (10% workloads)
            - Medium: Legacy application dependencies (25% workloads)
            - Low: Network latency sensitivity (15% workloads)

            ESTIMATED TIMELINE: 18 months
            ESTIMATED COST: $2.4M (first year), $890K (ongoing annual)
            """,
            "expected_summary_length": "100-150 words",
            "key_points_to_include": [
                "120 VMs across 3 data centers",
                "Re-architect 30%, Re-platform 50%, Rehost 20%",
                "18 month timeline",
                "$2.4M first year cost",
                "High risk: Data sovereignty (10%)",
                "Medium risk: Legacy dependencies (25%)"
            ],
            "critical_info_that_must_not_be_hallucinated": [
                "VM count (120)",
                "Timeline (18 months)",
                "Cost figures ($2.4M, $890K)",
                "Migration strategy percentages"
            ]
        }
    ],
    "evaluation_criteria": {
        "rouge_l": {"threshold": 0.40, "weight": 0.25},
        "factuality": {"threshold": 0.95, "weight": 0.40},  # Critical facts preserved
        "key_point_coverage": {"threshold": 0.90, "weight": 0.25},
        "no_hallucination": {"threshold": 1.0, "weight": 0.10}  # Must not add false info
    },
    "pass_threshold": 0.85
}
```

---

## Foundation Model Benchmark Reference

### Standard Benchmarks

| Benchmark | Type | Tasks | Scores Reported |
|-----------|------|-------|-----------------|
| MMLU | Knowledge | 57 subjects, MCQ | 5-shot accuracy |
| GSM8K | Math | 8.5K problems | Accuracy, Pass@K |
| BIG-Bench | Comprehensive | 150+ tasks | Normalized score |
| HellaSwag | Common Sense | 70K samples | Accuracy |
| TruthfulQA | Truthfulness | 817 questions | MC2 |
| HumanEval | Code | 164 problems | Pass@K |

### Custom Benchmarks for Cloud Migration

```python
CLOUD_MIGRATION_BENCHMARKS = {
    "infrastructure_classification": {
        "description": "Classify infrastructure descriptions",
        "test_count": 500,
        "categories": ["IaaS", "PaaS", "SaaS", "CaaS", "FaaS", "Hybrid"],
        "expected_accuracy": 0.88
    },
    "dependency_resolution": {
        "description": "Resolve infrastructure dependencies",
        "test_count": 200,
        "complexity_levels": ["simple (3-5 nodes)", "medium (6-10)", "complex (11+)"],
        "expected_accuracy": 0.85
    },
    "cost_estimation": {
        "description": "Calculate cloud costs",
        "test_count": 300,
        "providers": ["AWS", "Azure", "GCP"],
        "expected_accuracy": 0.90
    },
    "migration_strategy_selection": {
        "description": "Recommend migration strategies",
        "test_count": 400,
        "strategies": ["Rehost", "Replatform", "Refactor", "Repurchase", "Retire", "Retain"],
        "expected_accuracy": 0.82
    }
}
```

---

## Running Foundation Evaluations

### Python API

```python
from ai_testing_benchmark.evaluation import FoundationModelEvaluator

# Initialize evaluator
evaluator = FoundationModelEvaluator(
    model="gpt-4",
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Run language understanding tests
lu_results = evaluator.run_tests(
    category="language_understanding",
    test_cases=["TC-FU-001", "TC-FU-002", "TC-FU-003"],
    verbose=True
)

# Run reasoning tests
reasoning_results = evaluator.run_tests(
    category="reasoning",
    test_cases=["TC-RE-001", "TC-RE-002"]
)

# Run generation tests
gen_results = evaluator.run_tests(
    category="generation",
    test_cases=["TC-GN-001", "TC-GN-002"]
)

# Generate comprehensive report
report = evaluator.generate_report(
    results=[lu_results, reasoning_results, gen_results],
    output_format="json"
)
print(f"Overall Foundation Score: {report['overall_score']}")
```

### CLI Usage

```bash
# Run all foundation tests
python -m ai_testing_benchmark evaluation foundation \
    --model gpt-4 \
    --category all

# Run specific test category
python -m ai_testing_benchmark evaluation foundation \
    --model gpt-4 \
    --category language_understanding \
    --tests TC-FU-001 TC-FU-002

# Run with custom dataset
python -m ai_testing_benchmark evaluation foundation \
    --model gpt-4 \
    --category reasoning \
    --dataset custom_cloud_math_problems.json
```

### Configuration

```yaml
# foundation_evaluation_config.yaml
foundation_evaluation:
  model:
    name: "gpt-4"
    provider: "openai"
    version: "latest"
    parameters:
      temperature: 0.0
      max_tokens: 2048

  language_understanding:
    enabled: true
    tests:
      - TC-FU-001
      - TC-FU-002
      - TC-FU-003
      - TC-FU-004
      - TC-FU-005
    thresholds:
      accuracy: 0.85
      f1_score: 0.83

  reasoning:
    enabled: true
    tests:
      - TC-RE-001
      - TC-RE-002
      - TC-RE-003
      - TC-RE-004
    thresholds:
      accuracy: 0.80
      step_accuracy: 0.75

  generation:
    enabled: true
    tests:
      - TC-GN-001
      - TC-GN-002
      - TC-GN-003
    thresholds:
      bleu: 0.30
      rouge_l: 0.35

  reporting:
    format: ["json", "html"]
    output_dir: "./results/foundation"
    include_raw_outputs: true
```

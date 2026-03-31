# AI Testing Benchmark - 评估框架指南

## 目录

1. [概述](#概述)
2. [五层架构](#五层架构)
3. [基础模型评估](#基础模型评估)
4. [对话式AI评估](#对话式ai评估)
5. [云迁移旅程评估](#云迁移旅程评估)
6. [安全与对齐评估](#安全与对齐评估)
7. [性能评估](#性能评估)
8. [评分方法论](#评分方法论)
9. [运行评估](#运行评估)

---

## 概述

AI-Testing-Benchmark 实现了一套综合性的五层评估框架，专门为引导用户完成云迁移旅程的AI系统设计。每一层针对AI能力评估的关键方面。

### 设计原则

1. **领域特异性**：专为云迁移AI助手定制
2. **可测量性**：所有指标均可量化且可重现
3. **渐进覆盖**：从基础语言能力到复杂领域任务
4. **安全优先**：强调安全和对齐测试
5. **生产就绪**：适合CI/CD集成

---

## 五层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    第五层: 性能                                   │
│              延迟、吞吐量、可扩展性、成本                            │
├─────────────────────────────────────────────────────────────────┤
│                    第四层: 安全与对齐                              │
│            安全性、公平性、真实性、鲁棒性                            │
├─────────────────────────────────────────────────────────────────┤
│                    第三层: 云迁移AI                                │
│          评估、规划、执行、验证、优化                                │
├─────────────────────────────────────────────────────────────────┤
│                    第二层: 对话式AI                               │
│         意图识别、实体提取、对话流程、响应质量                      │
├─────────────────────────────────────────────────────────────────┤
│                    第一层: 基础模型                                │
│              语言理解、推理、生成                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 基础模型评估

### 1.1 语言理解

#### 测试类别

| 类别 | 描述 | 指标 |
|------|------|------|
| 文本分类 | 将输入文本分类到预定义类别 | 准确率、F1(宏/加权) |
| 命名实体识别 | 从文本中提取结构化实体 | 实体F1、精确率、召回率 |
| 情感分析 | 检测积极/消极/中性情感 | 准确率、各类F1 |
| 语义相似度 | 测量文本间的语义 closeness | 余弦相似度、Spearman相关性 |
| 自然语言推理 | 判断 entailment/矛盾/中性 | 准确率 |

#### 示例测试用例

**TC-FU-001: 文本分类 - 基础设施类型检测**

```python
"""
测试用例: TC-FU-001
类别: 文本分类
目标: 评估模型对云基础设施描述进行分类的能力
"""

TEST_CASE = {
    "id": "TC-FU-001",
    "name": "基础设施类型分类",
    "category": "text_classification",
    "description": """
    评估模型将云基础设施描述正确分类为适当类别的能力
    (IaaS、PaaS、SaaS、FaaS等)
    """,
    "test_data": [
        {
            "input": "我们有50台运行Ubuntu和Windows Server的虚拟机，"
                    "根据流量模式进行手动扩展。",
            "expected_category": "IaaS",
            "confidence_range": (0.85, 1.0)
        },
        {
            "input": "我们的开发团队使用托管的Kubernetes pods，"
                    "具有内置负载均衡和自动容器编排。",
            "expected_category": "CaaS/Kubernetes",
            "confidence_range": (0.80, 1.0)
        },
        {
            "input": "员工通过浏览器访问Salesforce CRM进行客户关系管理，"
                    "无需本地安装。",
            "expected_category": "SaaS",
            "confidence_range": (0.90, 1.0)
        },
        {
            "input": "应用程序运行在AWS Lambda函数上，由API Gateway事件触发，"
                    "按需处理图像。",
            "expected_category": "FaaS",
            "confidence_range": (0.85, 1.0)
        }
    ],
    "evaluation_criteria": {
        "accuracy": {"threshold": 0.90, "weight": 0.4},
        "f1_weighted": {"threshold": 0.88, "weight": 0.3},
        "avg_confidence_accuracy": {"threshold": 0.15, "weight": 0.15},
        "rejection_quality": {"threshold": 0.05, "weight": 0.15}
    },
    "pass_threshold": 0.85,
    "fail_threshold": 0.75,
    "datasets": ["20newsgroups", "custom_infrastructure_corpus"]
}
```

**TC-FU-002: 命名实体识别 - 云资源提取**

```python
"""
测试用例: TC-FU-002
类别: 命名实体识别
目标: 从自然语言中提取云资源和属性
"""

TEST_CASE = {
    "id": "TC-FU-002",
    "name": "云资源实体提取",
    "category": "ner",
    "description": """
    评估模型从非结构化文本中识别和提取云资源实体
    (VM、数据库、存储、网络)及其属性
    (区域、大小、配置)的能力。
    """,
    "entity_types": [
        "RESOURCE_TYPE",  # VM、数据库、存储、负载均衡器等
        "PROVIDER",       # AWS、Azure、GCP、本地
        "REGION",         # us-east-1、westus2等
        "SIZE",           # small、medium、large、t2.micro等
        "STATUS",         # running、stopped、maintenance
        "TECHNOLOGY"     # PostgreSQL、Kubernetes、Docker等
    ],
    "test_data": [
        {
            "text": "我们在us-east-1有三台m5.large EC2实例，"
                    "运行Ubuntu 22.04，连接到us-east-1b的"
                    "RDS PostgreSQL数据库，100GB存储。",
            "expected_entities": [
                {"type": "RESOURCE_TYPE", "value": "EC2实例", "start": 12, "end": 27},
                {"type": "SIZE", "value": "m5.large", "start": 28, "end": 36},
                {"type": "PROVIDER", "value": "AWS", "start": 40, "end": 43},
                {"type": "REGION", "value": "us-east-1", "start": 47, "end": 56},
                {"type": "RESOURCE_TYPE", "value": "RDS PostgreSQL数据库", "start": 95, "end": 119}
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
    "fail_threshold": 0.80
}
```

**TC-FU-003: 情感分析 - 用户反馈分析**

```python
TEST_CASE = {
    "id": "TC-FU-003",
    "name": "迁移情感分析",
    "category": "sentiment_analysis",
    "description": """
    评估模型检测与云迁移体验相关的用户反馈情感的能力，
    包括技术挫折感、满意度和关切。
    """,
    "test_data": [
        {
            "text": "迁移到AWS比预期更顺利。我们的团队对性能提升印象深刻。",
            "expected_sentiment": "positive",
            "expected_scores": {"positive": 0.92, "neutral": 0.05, "negative": 0.03}
        },
        {
            "text": "迁移到新数据库后我们不断遇到连接断开。这正在影响我们的生产环境。",
            "expected_sentiment": "negative",
            "expected_scores": {"positive": 0.02, "neutral": 0.08, "negative": 0.90}
        },
        {
            "text": "迁移窗口已安排在下周末。我们需要在周五前完成测试。",
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

### 1.2 推理能力

#### 测试类别

| 类别 | 描述 | 指标 |
|------|------|------|
| 数学推理 | 分步解决数学问题 | 准确率、Pass@K |
| 逻辑推理 | 从前提得出结论 | 准确率 |
| 常识推理 | 运用日常知识 | 准确率、HellaSwag |
| 思维链 | 生成推理步骤 | 步骤准确率、连贯性 |

#### 示例测试用例

**TC-RE-001: 数学推理 - 成本估算**

```python
TEST_CASE = {
    "id": "TC-RE-001",
    "name": "云成本数学推理",
    "category": "mathematical_reasoning",
    "description": """
    评估模型执行云成本多步数学推理的能力，
    包括预留实例节省计划和分层定价。
    """,
    "test_data": [
        {
            "problem": """
            一家公司使用50台t3.medium实例，7x24小时运行于us-east-1。
            按需定价为每实例每小时$0.0416。
            他们正在考虑1年期预付预留实例，每小时$0.0224(节省72%)。

            1. 计算年度按需成本
            2. 计算年度预留实例成本
            3. 计算年度节省
            4. 盈亏平衡点是第几个月?

            逐步展示你的推理过程。
            """,
            "expected_steps": [
                "计算年度按需成本: 50 × $0.0416 × 24 × 365 = $18,412.80",
                "计算年度RI成本: 50 × $0.0224 × 24 × 365 = $9,820.80",
                "计算节省: $18,412.80 - $9,820.80 = $8,592.00",
                "月度节省: $8,592.00 / 12 = $716.00",
                "一次性RI支付: $9,820.80",
                "盈亏平衡: $9,820.80 / $716.00 ≈ 13.7个月 → 第14个月"
            ],
            "expected_answers": {
                "on_demand_annual": 18412.80,
                "ri_annual": 9820.80,
                "savings": 8592.00,
                "break_even_month": 14
            },
            "partial_credit": True
        }
    ],
    "evaluation_criteria": {
        "final_answer_accuracy": {"threshold": 0.95, "weight": 0.50},
        "step_accuracy": {"threshold": 0.85, "weight": 0.30},
        "reasoning_coherence": {"threshold": 0.80, "weight": 0.20}
    },
    "pass_threshold": 0.88
}
```

**TC-RE-002: 逻辑推理 - 依赖解析**

```python
TEST_CASE = {
    "id": "TC-RE-002",
    "name": "基础设施依赖逻辑推理",
    "category": "logical_reasoning",
    "description": """
    评估模型根据服务和基础设施之间的依赖约束
    推导正确迁移顺序的能力。
    """,
    "test_data": [
        {
            "scenario": """
            给定以下基础设施依赖:
            - 数据库(DB)必须在应用程序(APP)之前迁移
            - 负载均衡器(LB)必须在Web服务器(WEB)之前运行
            - APP依赖于DB和缓存
            - 缓存可以独立迁移
            - WEB依赖于APP
            - 监控(MON)可以随时设置

            问题1: 有效的迁移顺序是什么?
            问题2: 识别关键路径(最长的依赖链)
            问题3: 最少的顺序迁移组数是多少?
            """,
            "expected_answers": {
                "migration_order": ["缓存", "DB", "APP", "WEB", "LB", "MON"],
                "critical_path": ["DB", "APP", "WEB", "LB"],
                "sequential_groups": 4
            }
        }
    ],
    "evaluation_criteria": {
        "order_correctness": {"threshold": 1.0, "weight": 0.40},
        "dependency_respected": {"threshold": 1.0, "weight": 0.35},
        "critical_path_identification": {"threshold": 0.90, "weight": 0.25}
    },
    "pass_threshold": 0.90
}
```

---

### 1.3 生成能力

#### 测试类别

| 类别 | 描述 | 指标 |
|------|------|------|
| 文本生成 | 连贯、相关的文本生成 | BLEU、ROUGE、BERTScore |
| 代码生成 | 生成有效、高效的代码 | Pass@K、HumanEval |
| 创意写作 | 生成新颖、创意的内容 | 人工评估 |
| 摘要 | 准确概括信息 | ROUGE-L、事实性 |

#### 示例测试用例

**TC-GN-001: 代码生成 - 基础设施即代码**

```python
TEST_CASE = {
    "id": "TC-GN-001",
    "name": "Terraform代码生成",
    "category": "code_generation",
    "description": """
    评估模型根据需求生成有效Terraform代码
    用于云基础设施配置的能力。
    """,
    "test_data": [
        {
            "requirement": """
            生成Terraform代码以创建:
            1. us-east-1中CIDR为10.0.0.0/16的VPC
            2. 不同可用区的两个公有子网
            3. 附加到VPC的Internet Gateway
            4. 具有到IGW默认路由的路由表
            5. 将路由表与两个子网关联

            使用适当的命名约定和标签。
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
                "syntax_valid",
                "resources_complete",
                "dependencies_correct",
                "subnets_different_az",
                "naming_convention"
            ]
        }
    ],
    "evaluation_criteria": {
        "syntax_validity": {"threshold": 1.0, "weight": 0.20},
        "component_completeness": {"threshold": 0.95, "weight": 0.30},
        "functional_correctness": {"threshold": 0.90, "weight": 0.30},
        "best_practices_adherence": {"threshold": 0.85, "weight": 0.20}
    },
    "pass_threshold": 0.88
}
```

---

## 基础模型基准参考

### 标准基准

| 基准 | 类型 | 任务 | 报告分数 |
|------|------|------|----------|
| MMLU | 知识 | 57个科目、MCQ | 5-shot准确率 |
| GSM8K | 数学 | 8.5K问题 | 准确率、Pass@K |
| BIG-Bench | 综合 | 150+任务 | 标准化分数 |
| HellaSwag | 常识 | 70K样本 | 准确率 |
| TruthfulQA | 真实性 | 817问题 | MC2 |
| HumanEval | 代码 | 164问题 | Pass@K |

### 云迁移自定义基准

```python
CLOUD_MIGRATION_BENCHMARKS = {
    "infrastructure_classification": {
        "description": "将基础设施描述分类",
        "test_count": 500,
        "categories": ["IaaS", "PaaS", "SaaS", "CaaS", "FaaS", "混合"],
        "expected_accuracy": 0.88
    },
    "dependency_resolution": {
        "description": "解析云资源之间的依赖",
        "test_count": 200,
        "complexity_levels": ["简单(3-5节点)", "中等(6-10)", "复杂(11+)"],
        "expected_accuracy": 0.85
    },
    "cost_estimation": {
        "description": "估算云成本",
        "test_count": 300,
        "providers": ["AWS", "Azure", "GCP"],
        "expected_accuracy": 0.90
    },
    "migration_strategy_selection": {
        "description": "推荐迁移策略",
        "test_count": 400,
        "strategies": ["重新托管", "重新平台化", "重构", "重新购买", "淘汰", "保留"],
        "expected_accuracy": 0.82
    }
}
```

---

## 运行基础评估

### Python API

```python
from ai_testing_benchmark.evaluation import FoundationModelEvaluator

# 初始化评估器
evaluator = FoundationModelEvaluator(
    model="gpt-4",
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 运行语言理解测试
lu_results = evaluator.run_tests(
    category="language_understanding",
    test_cases=["TC-FU-001", "TC-FU-002", "TC-FU-003"],
    verbose=True
)

# 运行推理测试
reasoning_results = evaluator.run_tests(
    category="reasoning",
    test_cases=["TC-RE-001", "TC-RE-002"]
)

# 生成综合报告
report = evaluator.generate_report(
    results=[lu_results, reasoning_results, gen_results],
    output_format="json"
)
print(f"总体基础分数: {report['overall_score']}")
```

### CLI用法

```bash
# 运行所有基础测试
python -m ai_testing_benchmark evaluation foundation \
    --model gpt-4 \
    --category all

# 运行特定测试类别
python -m ai_testing_benchmark evaluation foundation \
    --model gpt-4 \
    --category language_understanding \
    --tests TC-FU-001 TC-FU-002
```

### 配置

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
    thresholds:
      accuracy: 0.85
      f1_score: 0.83

  reasoning:
    enabled: true
    tests:
      - TC-RE-001
      - TC-RE-002
    thresholds:
      accuracy: 0.80
      step_accuracy: 0.75

  generation:
    enabled: true
    tests:
      - TC-GN-001
      - TC-GN-002
    thresholds:
      bleu: 0.30
      rouge_l: 0.35

  reporting:
    format: ["json", "html"]
    output_dir: "./results/foundation"
    include_raw_outputs: true
```

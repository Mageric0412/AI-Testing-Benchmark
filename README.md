# AI-Testing-Benchmark

面向AI引导云迁移旅程系统的综合工程级评估框架。

## 概述

AI-Testing-Benchmark 提供了一套系统化的方法，用于评估引导用户完成云迁移旅程的AI系统。涵盖基础模型能力、对话式AI质量、迁移专项AI能力、安全与对齐以及性能指标等五大评估维度。

## 架构

```
AI-Testing-Benchmark/
├── src/ai_testing_benchmark/     # 核心评估框架
│   ├── core/                      # 基础类和接口
│   │   ├── config.py              # 配置管理
│   │   ├── test_suite_loader.py   # XLSX多Sheet加载器
│   │   ├── scoring_engine.py      # 配置驱动评分引擎
│   │   ├── metrics.py             # 指标计算
│   │   ├── result.py              # 结果管理
│   │   └── benchmark_runner.py    # 基准测试运行器
│   ├── evaluation/                # 基础模型评估
│   ├── dialogue/                  # 对话式AI评估
│   ├── migration/                 # 云迁移专项测试
│   ├── safety/                   # 安全与对齐测试
│   └── performance/               # 性能基准测试
├── web/                           # Web界面
│   └── app.py                     # Streamlit应用
├── templates/                      # 模板生成器
├── tests/                         # 测试套件
├── examples/                      # 使用示例
├── docs/                          # 详细文档
└── data/                          # 样本数据集
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/Mageric0412/AI-Testing-Benchmark.git
cd AI-Testing-Benchmark

# 安装依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .
```

## 新特性 (v2.0)

### XLSX多Sheet测试套件支持
支持导入包含多个Sheet的Excel测试套件文件：
- `test_cases` - 测试用例表
- `scenarios` - 场景定义表
- `config` - 配置表

### 配置驱动的评分引擎
所有评分公式和置信值均可通过YAML/JSON配置文件管理：
- 自定义评分公式权重
- 可配置通过/危险阈值
- 置信度计算方法可配置

### Web界面
基于Streamlit的图形化界面：
- 拖拽上传XLSX测试套件
- 可视化评测结果
- 配置管理可视化
- 报告导出

```bash
# 启动Web界面
cd web
pip install -r requirements.txt
python app.py
```

### 评分配置文件示例

```yaml
# scoring_config.yaml
formulas:
  accuracy:
    type: accuracy
    thresholds:
      pass: 0.80
      warning: 0.70

  migration_success:
    type: custom
    weights:
      resource_discovery: 0.20
      strategy_recommendation: 0.30
      cost_estimation: 0.25
      risk_identification: 0.25
    thresholds:
      pass: 0.80
      warning: 0.70

confidence:
  levels:
    high: 0.90
    medium: 0.70
    low: 0.50
  calculation_method: sample_size_based
  min_samples_for_high_confidence: 30

phase_weights:
  foundation: 0.20
  dialogue: 0.20
  migration: 0.25
  safety: 0.20
  performance: 0.15

pass_threshold: 0.80
critical_threshold: 0.60
```

## 快速开始

```python
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.evaluation import FoundationModelEvaluator
from ai_testing_benchmark.migration import CloudMigrationJourneyEvaluator

# 运行基础模型评估
runner = BenchmarkRunner()
results = runner.run_foundation_evaluation(
    model="gpt-4",
    benchmarks=["mmlu", "gsm8k", "truthfulqa"]
)

# 运行云迁移旅程评估
migration_evaluator = CloudMigrationJourneyEvaluator()
journey_results = migration_evaluator.evaluate_phase("assessment", user_input={
    "infrastructure_description": "100台虚拟机, 5个数据库"
})
```

## 五层评估框架

### 第一层：基础模型能力
- 语言理解（分类、实体识别、情感分析）
- 推理能力（数学推理、逻辑推理、常识推理）
- 生成能力（文本、代码、创意写作）
- 知识应用

### 第二层：对话式AI评估
- 意图识别准确率
- 实体提取F1分数
- 对话流程质量
- 响应延迟与自然度

### 第三层：云迁移AI评估
- **评估阶段**：基础设施发现、风险识别
- **规划阶段**：顺序优化、策略推荐
- **执行阶段**：自动化迁移、回滚能力
- **验证阶段**：前后对比、异常检测

### 第四层：安全与对齐
- 提示注入抵抗
- 越狱攻击抵抗
- 偏见检测（人口统计平等、刻板印象）
- 幻觉预防

### 第五层：性能指标
- 延迟（P50、P95、P99）
- 吞吐量（Tokens/秒）
- 成本效率
- 可扩展性

## 文档

详细文档位于 [docs](./docs/) 目录：

- [评估框架指南](./docs/EVALUATION_FRAMEWORK.md)
- [云迁移测试套件](./docs/CLOUD_MIGRATION_TESTS.md)
- [工具集成指南](./docs/TOOL_INTEGRATIONS.md)
- [API参考](./docs/API_REFERENCE.md)
- [测试用例目录](./docs/TEST_CASE_CATALOG.md)

## 支持的工具

| 类别 | 工具 |
|------|------|
| LLM评估 | LangTest, LM Evaluation Harness |
| RAG评估 | RAGAS, Trulens |
| 公平性 | AIF360, Fairlearn |
| 内容审核 | Perspective API, OpenAI Moderation |
| 基准测试 | 自定义框架, Prometheus |

## 质量门禁

| 指标 | 阈值 |
|------|------|
| 总体评分 | >= 80/100 |
| 严重问题数 | = 0 |
| 高优先级问题数 | <= 3 |
| 意图识别准确率 | >= 85% |
| 迁移成功率 | >= 99% |
| 安全评分 | >= 90% |

## 贡献

欢迎贡献！请在提交PR前阅读贡献指南。

## 许可证

MIT许可证 - 详见 [LICENSE](LICENSE)。

## 参考资料

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [Stanford HELM](https://crfm.stanford.edu/helm/)
- [HuggingFace Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard)
- [RASA Testing](https://rasa.com/docs/rasa/testing)
- [MITRE ATLAS](https://attack.mitre.org/docs/ATLAS/)

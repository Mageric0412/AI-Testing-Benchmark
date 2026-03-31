# API 参考

## 目录

1. [核心类](#核心类)
2. [评估类](#评估类)
3. [配置类](#配置类)
4. [结果类](#结果类)

---

## 核心类

### BenchmarkRunner

运行综合AI基准测试的主要协调器。

```python
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig

# 从配置初始化
runner = BenchmarkRunner(config=BenchmarkConfig(...))

# 从文件初始化
runner = BenchmarkRunner(config_path="/path/to/config.yaml")

# 运行完整基准测试
report = runner.run_full_benchmark(
    phases=["foundation", "dialogue", "migration"],
    stop_on_first_failure=False
)

# 运行特定阶段
phase_result = runner.run_phase("foundation")

# 生成报告
json_report = runner.generate_report(output_format="json")
runner.generate_report(output_path="./report.html", output_format="html")
```

#### 方法

##### `__init__(config=None, config_path=None, verbose=False)`

初始化基准测试运行器。

**参数:**
- `config` (BenchmarkConfig, 可选): 配置对象
- `config_path` (str, 可选): YAML配置文件路径
- `verbose` (bool): 启用详细日志

##### `run_full_benchmark(phases=None, stop_on_first_failure=False)`

在所有或指定阶段上运行完整基准测试。

**参数:**
- `phases` (list, 可选): 要运行的阶段列表。默认为所有启用的阶段。
- `stop_on_first_failure` (bool): 如果关键测试失败则停止

**返回:**
- `BenchmarkReport`: 完整基准测试结果

##### `run_phase(phase, test_cases=None)`

运行特定评估阶段。

**参数:**
- `phase` (str): 阶段名称 (foundation, dialogue, migration, safety, performance)
- `test_cases` (list, 可选): 要运行的特定测试用例

**返回:**
- `PhaseResult`: 阶段评估结果

##### `generate_report(output_format='json', output_path=None, include_raw=False)`

生成基准测试报告。

**参数:**
- `output_format` (str): 格式 ('json' 或 'html')
- `output_path` (str, 可选): 保存报告的路径
- `include_raw` (bool): 包含原始模型输出

**返回:**
- `str`: 报告内容

---

### BaseEvaluator

所有评估器的抽象基类。

```python
from ai_testing_benchmark.core.base_evaluator import BaseEvaluator

class MyEvaluator(BaseEvaluator):
    def evaluate_single(self, test_case):
        # 评估单个测试用例
        return EvaluationResult(...)

    def calculate_overall_score(self, results):
        # 计算聚合分数
        return {"overall_score": 85.0}
```

#### 抽象方法

##### `evaluate_single(test_case) -> EvaluationResult`

评估单个测试用例。

##### `calculate_overall_score(results) -> Dict`

从结果计算总体分数。

#### 方法

##### `run_evaluation(test_cases, stop_on_first_failure=False, early_stopping_threshold=0.5)`

在多个测试用例上运行评估。

---

## 评估类

### FoundationModelEvaluator

基础模型能力的评估器。

```python
from ai_testing_benchmark.evaluation import FoundationModelEvaluator

evaluator = FoundationModelEvaluator(
    model_name="gpt-4",
    provider="openai",
    config={"custom_setting": value},
    verbose=True
)

result = evaluator.run_phase()
```

**评估类别:**
- 语言理解（分类、NER、情感）
- 推理（数学、逻辑、常识）
- 生成（文本、代码、摘要）

### DialogueEvaluator

对话式AI能力的评估器。

```python
from ai_testing_benchmark.dialogue import DialogueEvaluator

evaluator = DialogueEvaluator(
    model_name="gpt-4",
    provider="openai"
)

result = evaluator.evaluate_single({
    "id": "TC-DIAL-001",
    "category": "intent_recognition",
    "user_utterance": "I need help with migration",
    "expected_intent": "greeting"
})
```

**评估类别:**
- 意图识别
- 实体提取
- 对话流程
- 响应质量
- 用户旅程完成度

### CloudMigrationEvaluator

云迁移AI能力的评估器。

```python
from ai_testing_benchmark.migration import CloudMigrationEvaluator

evaluator = CloudMigrationEvaluator(
    model_name="gpt-4",
    provider="openai",
    config={"phase": "assessment"}
)
```

**评估阶段:**
- 评估（基础设施发现、风险识别、成本估算）
- 规划（排序优化、策略推荐）
- 执行（迁移自动化、回滚）
- 验证（功能、性能）

### SafetyEvaluator

AI安全和对齐的评估器。

```python
from ai_testing_benchmark.safety import SafetyEvaluator

evaluator = SafetyEvaluator(
    model_name="gpt-4",
    provider="openai"
)
```

**评估类别:**
- 提示注入抵抗
- 越狱攻击抵抗
- 偏见检测
- 毒性预防
- 幻觉预防

### PerformanceEvaluator

AI系统性能的评估器。

```python
from ai_testing_benchmark.performance import PerformanceEvaluator

evaluator = PerformanceEvaluator(
    model_name="gpt-4",
    provider="openai"
)
```

**评估类别:**
- 延迟（P50、P95、P99）
- 吞吐量（Tokens/秒）
- 成本效率
- 可扩展性

---

## 配置类

### BenchmarkConfig

基准测试的主要配置。

```python
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig

config = BenchmarkConfig(
    model=ModelConfig(
        name="gpt-4",
        provider="openai",
        parameters={"temperature": 0.0}
    ),
    foundation={"enabled": True},
    migration={"enabled": True}
)
```

#### 类方法

##### `from_yaml(path) -> BenchmarkConfig`

从YAML文件加载。

##### `from_dict(config_dict) -> BenchmarkConfig`

从字典创建。

##### `from_env() -> BenchmarkConfig`

从环境变量加载。

#### 属性

##### `is_phase_enabled(phase) -> bool`

检查阶段是否启用。

##### `get_thresholds(phase) -> ThresholdConfig`

获取阶段的阈值。

### ModelConfig

被评估模型的配置。

```python
model_config = ModelConfig(
    name="gpt-4",
    provider="openai",
    version="latest",
    parameters={
        "temperature": 0.0,
        "max_tokens": 2048,
        "top_p": 1.0
    },
    credentials={"api_key": "..."}
)
```

### ThresholdConfig

评估阈值的配置。

```python
from ai_testing_benchmark.core.config import ThresholdConfig

thresholds = ThresholdConfig(
    accuracy=0.85,
    f1_score=0.83,
    latency_p95_ms=500.0,
    toxicity=0.10,
    fairness_score=0.90
)
```

---

## 结果类

### EvaluationResult

单个测试用例评估的完整结果。

```python
result = EvaluationResult(
    test_case_id="TC-001",
    test_case_name="测试用例1",
    category="foundation",
    phase="foundation",
    status=ResultStatus.PASS,
    score=85.0,
    pass_threshold=80.0,
    metrics={
        "accuracy": 0.92,
        "f1_score": 0.88
    },
    details={
        "expected": "IaaS",
        "predicted": "IaaS"
    },
    execution_time_ms=150.0
)
```

#### 属性

##### `passed -> bool`

检查测试是否通过阈值。

##### `failed -> bool`

检查测试是否失败。

#### 方法

##### `add_issue(severity, message, details=None)`

向结果添加问题。

### PhaseResult

评估阶段的聚合结果。

```python
phase = PhaseResult(phase="foundation")
phase.add_result(result1)
phase.add_result(result2)

print(f"通过率: {phase.pass_rate}%")
print(f"阶段分数: {phase.overall_score}")
print(f"通过: {phase.passed}")
```

#### 属性

##### `pass_rate -> float`

计算通过率百分比。

##### `passed -> bool`

检查阶段是否整体通过。

### BenchmarkReport

完整的基准测试报告。

```python
report = BenchmarkReport(
    model_name="gpt-4",
    model_provider="openai",
    phases={
        "foundation": phase_result,
        "dialogue": phase_result
    }
)

report.calculate_overall_score()
report.check_quality_gates({"overall_score": 80.0, "critical_issues": 0})
```

#### 属性

##### `quality_gate_passed -> bool`

检查所有质量门禁是否通过。

#### 方法

##### `calculate_overall_score() -> float`

从阶段分数计算总体分数。

##### `check_quality_gates(gates) -> bool`

检查质量门禁合规性。

##### `to_dict(include_raw=False) -> Dict`

转换为字典。

---

## ResultStatus 枚举

```python
from ai_testing_benchmark.core.result import ResultStatus

status = ResultStatus.PASS   # 测试通过
status = ResultStatus.FAIL  # 测试失败
status = ResultStatus.WARNING  # 测试带警告通过
status = ResultStatus.ERROR    # 测试遇到错误
status = ResultStatus.SKIPPED   # 测试被跳过
```

---

## Severity 枚举

```python
from ai_testing_benchmark.core.result import Severity

severity = Severity.CRITICAL  # 严重问题
severity = Severity.HIGH     # 高优先级
severity = Severity.MEDIUM   # 中优先级
severity = Severity.LOW      # 低优先级
severity = Severity.INFO     # 信息
```

---

## 指标计算器

计算各种评估指标的工具类。

```python
from ai_testing_benchmark.core.metrics import MetricsCalculator

# 准确率
accuracy = MetricsCalculator.accuracy(y_true, y_pred)

# F1分数
f1 = MetricsCalculator.f1_score(y_true, y_pred, average="weighted")

# RMSE
rmse = MetricsCalculator.rmse(y_true, y_pred)

# BLEU分数
bleu = MetricsCalculator.bleu_score(reference, hypothesis)

# ROUGE-L
rouge = MetricsCalculator.rouge_l(reference, hypothesis)

# 余弦相似度
similarity = MetricsCalculator.cosine_similarity(vec1, vec2)

# 聚合分数
mean_score = MetricsCalculator.aggregate_scores([0.8, 0.9, 0.85], method="mean")

# 百分位数
p95 = MetricsCalculator.percentile(values, 95)

# 置信区间
lower, upper = MetricsCalculator.confidence_interval(scores, confidence=0.95)
```

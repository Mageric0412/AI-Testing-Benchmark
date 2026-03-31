# API Reference

## Table of Contents

1. [Core Classes](#core-classes)
2. [Evaluation Classes](#evaluation-classes)
3. [Configuration Classes](#configuration-classes)
4. [Result Classes](#result-classes)

---

## Core Classes

### BenchmarkRunner

Main orchestrator for running comprehensive AI benchmarks.

```python
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig

# Initialize from config
runner = BenchmarkRunner(config=BenchmarkConfig(...))

# Initialize from file
runner = BenchmarkRunner(config_path="/path/to/config.yaml")

# Run full benchmark
report = runner.run_full_benchmark(
    phases=["foundation", "dialogue", "migration"],
    stop_on_first_failure=False
)

# Run specific phase
phase_result = runner.run_phase("foundation")

# Generate report
json_report = runner.generate_report(output_format="json")
runner.generate_report(output_path="./report.html", output_format="html")
```

#### Methods

##### `__init__(config=None, config_path=None, verbose=False)`

Initialize the benchmark runner.

**Parameters:**
- `config` (BenchmarkConfig, optional): Configuration object
- `config_path` (str, optional): Path to YAML config file
- `verbose` (bool): Enable verbose logging

##### `run_full_benchmark(phases=None, stop_on_first_failure=False)`

Run complete benchmark across all or specified phases.

**Parameters:**
- `phases` (list, optional): List of phases to run. Defaults to all enabled.
- `stop_on_first_failure` (bool): Stop if critical test fails

**Returns:**
- `BenchmarkReport`: Complete benchmark results

##### `run_phase(phase, test_cases=None)`

Run a specific evaluation phase.

**Parameters:**
- `phase` (str): Phase name (foundation, dialogue, migration, safety, performance)
- `test_cases` (list, optional): Specific test cases to run

**Returns:**
- `PhaseResult`: Phase evaluation results

##### `generate_report(output_format='json', output_path=None, include_raw=False)`

Generate benchmark report.

**Parameters:**
- `output_format` (str): Format ('json' or 'html')
- `output_path` (str, optional): Path to save report
- `include_raw` (bool): Include raw model outputs

**Returns:**
- `str`: Report content

---

### BaseEvaluator

Abstract base class for all evaluators.

```python
from ai_testing_benchmark.core.base_evaluator import BaseEvaluator

class MyEvaluator(BaseEvaluator):
    def evaluate_single(self, test_case):
        # Evaluate single test case
        return EvaluationResult(...)

    def calculate_overall_score(self, results):
        # Calculate aggregated scores
        return {"overall_score": 85.0}
```

#### Abstract Methods

##### `evaluate_single(test_case) -> EvaluationResult`

Evaluate a single test case.

##### `calculate_overall_score(results) -> Dict`

Calculate overall score from results.

#### Methods

##### `run_evaluation(test_cases, stop_on_first_failure=False, early_stopping_threshold=0.5)`

Run evaluation on multiple test cases.

---

## Evaluation Classes

### FoundationModelEvaluator

Evaluates foundation model capabilities.

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

**Categories Evaluated:**
- Language Understanding (classification, NER, sentiment)
- Reasoning (mathematical, logical, common sense)
- Generation (text, code, summarization)

### DialogueEvaluator

Evaluates conversational AI capabilities.

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

**Categories Evaluated:**
- Intent Recognition
- Entity Extraction
- Dialogue Flow
- Response Quality
- User Journey Completion

### CloudMigrationEvaluator

Evaluates cloud migration AI capabilities.

```python
from ai_testing_benchmark.migration import CloudMigrationEvaluator

evaluator = CloudMigrationEvaluator(
    model_name="gpt-4",
    provider="openai",
    config={"phase": "assessment"}
)
```

**Phases Evaluated:**
- Assessment (infrastructure discovery, risk identification, cost estimation)
- Planning (sequencing optimization, strategy recommendation)
- Execution (migration automation, rollback)
- Validation (functional, performance)

### SafetyEvaluator

Evaluates AI safety and alignment.

```python
from ai_testing_benchmark.safety import SafetyEvaluator

evaluator = SafetyEvaluator(
    model_name="gpt-4",
    provider="openai"
)
```

**Categories Evaluated:**
- Prompt Injection Resistance
- Jailbreak Resistance
- Bias Detection
- Toxicity Prevention
- Hallucination Prevention

### PerformanceEvaluator

Evaluates AI system performance.

```python
from ai_testing_benchmark.performance import PerformanceEvaluator

evaluator = PerformanceEvaluator(
    model_name="gpt-4",
    provider="openai"
)
```

**Categories Evaluated:**
- Latency (P50, P95, P99)
- Throughput (tokens/second)
- Cost Efficiency
- Scalability

---

## Configuration Classes

### BenchmarkConfig

Main configuration for the benchmark.

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

#### Class Methods

##### `from_yaml(path) -> BenchmarkConfig`

Load from YAML file.

##### `from_dict(config_dict) -> BenchmarkConfig`

Create from dictionary.

##### `from_env() -> BenchmarkConfig`

Load from environment variables.

#### Properties

##### `is_phase_enabled(phase) -> bool`

Check if a phase is enabled.

##### `get_thresholds(phase) -> ThresholdConfig`

Get thresholds for a phase.

### ModelConfig

Configuration for the model under evaluation.

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

Configuration for evaluation thresholds.

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

## Result Classes

### EvaluationResult

Result for a single test case evaluation.

```python
result = EvaluationResult(
    test_case_id="TC-001",
    test_case_name="Test Case 1",
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

#### Properties

##### `passed -> bool`

Check if test passed threshold.

##### `failed -> bool`

Check if test failed.

#### Methods

##### `add_issue(severity, message, details=None)`

Add an issue to the result.

### PhaseResult

Aggregated results for an evaluation phase.

```python
phase = PhaseResult(phase="foundation")
phase.add_result(result1)
phase.add_result(result2)

print(f"Pass rate: {phase.pass_rate}%")
print(f"Phase score: {phase.overall_score}")
print(f"Passed: {phase.passed}")
```

#### Properties

##### `pass_rate -> float`

Calculate pass rate percentage.

##### `passed -> bool`

Check if phase passed overall.

### BenchmarkReport

Complete benchmark report.

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

#### Properties

##### `quality_gate_passed -> bool`

Check if all quality gates passed.

#### Methods

##### `calculate_overall_score() -> float`

Calculate weighted overall score.

##### `check_quality_gates(gates) -> bool`

Check quality gate compliance.

##### `to_dict(include_raw=False) -> Dict`

Convert to dictionary.

---

## ResultStatus Enum

```python
from ai_testing_benchmark.core.result import ResultStatus

status = ResultStatus.PASS  # Test passed
status = ResultStatus.FAIL   # Test failed
status = ResultStatus.WARNING  # Test passed with warnings
status = ResultStatus.ERROR    # Test encountered error
status = ResultStatus.SKIPPED   # Test was skipped
```

---

## Severity Enum

```python
from ai_testing_benchmark.core.result import Severity

severity = Severity.CRITICAL  # Critical issue
severity = Severity.HIGH      # High severity
severity = Severity.MEDIUM    # Medium severity
severity = Severity.LOW       # Low severity
severity = Severity.INFO      # Informational
```

---

## Metrics Calculator

Utility class for calculating evaluation metrics.

```python
from ai_testing_benchmark.core.metrics import MetricsCalculator

# Accuracy
accuracy = MetricsCalculator.accuracy(y_true, y_pred)

# F1 Score
f1 = MetricsCalculator.f1_score(y_true, y_pred, average="weighted")

# RMSE
rmse = MetricsCalculator.rmse(y_true, y_pred)

# BLEU Score
bleu = MetricsCalculator.bleu_score(reference, hypothesis)

# ROUGE-L
rouge = MetricsCalculator.rouge_l(reference, hypothesis)

# Cosine Similarity
similarity = MetricsCalculator.cosine_similarity(vec1, vec2)

# Aggregate scores
mean_score = MetricsCalculator.aggregate_scores([0.8, 0.9, 0.85], method="mean")

# Percentile
p95 = MetricsCalculator.percentile(values, 95)

# Confidence interval
lower, upper = MetricsCalculator.confidence_interval(scores, confidence=0.95)
```

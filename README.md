# AI-Testing-Benchmark

A comprehensive, engineering-grade evaluation framework for AI-guided cloud migration journey systems.

## Overview

AI-Testing-Benchmark provides a systematic approach to evaluating AI systems that guide users through cloud migration journeys. It covers foundation model capabilities, conversational AI quality, migration-specific AI abilities, safety & alignment, and performance metrics.

## Architecture

```
AI-Testing-Benchmark/
├── src/ai_testing_benchmark/     # Core evaluation framework
│   ├── core/                      # Base classes and interfaces
│   ├── evaluation/                # Foundation model evaluation
│   ├── dialogue/                  # Conversational AI evaluation
│   ├── migration/                 # Cloud migration specific tests
│   ├── safety/                    # Safety and alignment tests
│   └── performance/                # Performance benchmarking
├── tests/                         # Test suites
├── examples/                      # Usage examples
├── tools/                         # Tool integrations
├── docs/                          # Documentation
└── data/                          # Sample datasets
```

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/AI-Testing-Benchmark.git
cd AI-Testing-Benchmark

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```python
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.evaluation import FoundationModelEvaluator
from ai_testing_benchmark.migration import CloudMigrationJourneyEvaluator

# Run foundation model evaluation
runner = BenchmarkRunner()
results = runner.run_foundation_evaluation(
    model="gpt-4",
    benchmarks=["mmlu", "gsm8k", "truthfulqa"]
)

# Run cloud migration journey evaluation
migration_evaluator = CloudMigrationJourneyEvaluator()
journey_results = migration_evaluator.evaluate_phase("assessment", user_input={
    "infrastructure_description": "100 VMs, 5 databases"
})
```

## Five-Layer Evaluation Framework

### Layer 1: Foundation Model Capabilities
- Language Understanding (Classification, NER, Sentiment)
- Reasoning (Mathematical, Logical, Common Sense)
- Generation (Text, Code, Creative)
- Knowledge Application

### Layer 2: Conversational AI Evaluation
- Intent Recognition Accuracy
- Entity Extraction F1
- Dialogue Flow Quality
- Response Latency & Naturalness

### Layer 3: Cloud Migration AI Evaluation
- **Assessment Phase**: Infrastructure discovery, risk identification
- **Planning Phase**: Sequencing optimization, strategy recommendation
- **Execution Phase**: Automated migration, rollback capability
- **Validation Phase**: Pre/post comparison, anomaly detection

### Layer 4: Safety & Alignment
- Prompt Injection Resistance
- Jailbreak Resistance
- Bias Detection (Demographic parity, Stereotypes)
- Hallucination Prevention

### Layer 5: Performance Metrics
- Latency (P50, P95, P99)
- Throughput (Tokens/second)
- Cost Efficiency
- Scalability

## Documentation

Detailed documentation is available in the [docs](./docs/) directory:

- [Evaluation Framework Guide](./docs/EVALUATION_FRAMEWORK.md)
- [Cloud Migration Test Suite](./docs/CLOUD_MIGRATION_TESTS.md)
- [Tool Integration Guide](./docs/TOOL_INTEGRATIONS.md)
- [API Reference](./docs/API_REFERENCE.md)
- [Test Case Catalog](./docs/TEST_CASE_CATALOG.md)

## Supported Tools

| Category | Tools |
|----------|-------|
| LLM Evaluation | LangTest, LM Evaluation Harness |
| RAG Assessment | RAGAS, Trulens |
| Fairness | AIF360, Fairlearn |
| Content Moderation | Perspective API, OpenAI Moderation |
| Benchmarking | Custom Framework, Prometheus |

## Quality Gates

| Metric | Threshold |
|--------|-----------|
| Overall Score | >= 80/100 |
| Critical Issues | = 0 |
| High Issues | <= 3 |
| Intent Accuracy | >= 85% |
| Migration Success | >= 99% |
| Safety Score | >= 90% |

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

MIT License - see [LICENSE](LICENSE) for details.

## References

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [Stanford HELM](https://crfm.stanford.edu/helm/)
- [HuggingFace Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard)
- [RASA Testing](https://rasa.com/docs/rasa/testing)
- [MITRE ATLAS](https://attack.mitre.org/docs/ATLAS/)

# Test Case Catalog

This document catalogs all test cases in the AI-Testing-Benchmark framework.

---

## Foundation Model Test Cases

### Language Understanding (TC-FU-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-FU-001 | classification | Infrastructure Type Classification | 0.85 | Classify cloud infrastructure into IaaS/PaaS/SaaS/CaaS/FaaS |
| TC-FU-002 | ner | Cloud Resource Entity Extraction | 0.88 | Extract resource entities from text |
| TC-FU-003 | sentiment | Migration Sentiment Analysis | 0.85 | Detect sentiment in migration feedback |
| TC-FU-004 | semantic_similarity | Requirement Similarity | 0.80 | Measure semantic similarity between requirements |
| TC-FU-005 | inference | Logical Inference | 0.78 | Determine entailment/contradiction |

### Reasoning (TC-RE-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-RE-001 | mathematical | Cloud Cost Calculation | 0.88 | Multi-step cost estimation |
| TC-RE-002 | logical | Dependency Resolution | 0.90 | Deduce correct migration order |
| TC-RE-003 | common_sense | Infrastructure Commonsense | 0.75 | Apply common sense to infrastructure scenarios |
| TC-RE-004 | chain_of_thought | Multi-step Reasoning | 0.80 | Generate reasoning steps |

### Generation (TC-GN-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-GN-001 | code | Terraform Generation | 0.88 | Generate valid Terraform code |
| TC-GN-002 | summarization | Report Summarization | 0.85 | Summarize migration reports |
| TC-GN-003 | creative | Migration Communication | 0.75 | Generate clear migration communications |
| TC-GN-004 | transformation | Format Transformation | 0.80 | Transform data between formats |

---

## Dialogue Test Cases

### Intent Recognition (TC-DIAL-INT-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-DIAL-INT-001 | Greeting Intent | 0.90 | Detect greeting intents |
| TC-DIAL-INT-002 | Migration Inquiry | 0.88 | Detect migration-related inquiries |
| TC-DIAL-INT-003 | Risk Question | 0.85 | Detect risk assessment questions |
| TC-DIAL-INT-004 | Cost Question | 0.85 | Detect cost estimation requests |
| TC-DIAL-INT-005 | Status Query | 0.90 | Detect status check requests |

### Entity Extraction (TC-DIAL-ENT-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-DIAL-ENT-001 | Resource Count | 0.88 | Extract server/VM counts |
| TC-DIAL-ENT-002 | Cloud Provider | 0.95 | Extract provider names (AWS/Azure/GCP) |
| TC-DIAL-ENT-003 | Region | 0.90 | Extract region identifiers |
| TC-DIAL-ENT-004 | Service Type | 0.85 | Extract service types |

### Dialogue Flow (TC-DIAL-FLOW-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-DIAL-FLOW-001 | Assessment Journey | 0.85 | Complete assessment conversation |
| TC-DIAL-FLOW-002 | Planning Journey | 0.82 | Complete planning conversation |
| TC-DIAL-FLOW-003 | Troubleshooting Journey | 0.80 | Handle troubleshooting flow |

---

## Cloud Migration Test Cases

### Assessment Phase (TC-CM-ASSESS-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-CM-ASSESS-001 | infrastructure | Server Discovery | 0.95 | Discover server infrastructure |
| TC-CM-ASSESS-002 | dependency | Dependency Mapping | 0.92 | Map application dependencies |
| TC-CM-ASSESS-003 | risk | Risk Detection | 0.90 | Identify migration risks |
| TC-CM-ASSESS-004 | cost | Cost Estimation | 0.85 | Estimate migration costs |
| TC-CM-ASSESS-005 | compliance | Compliance Check | 0.88 | Check regulatory compliance |

### Planning Phase (TC-CM-PLAN-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-CM-PLAN-001 | sequencing | Migration Order | 0.90 | Optimize migration sequence |
| TC-CM-PLAN-002 | strategy | Strategy Selection | 0.85 | Recommend migration strategies |
| TC-CM-PLAN-003 | timeline | Timeline Estimation | 0.80 | Estimate migration timeline |
| TC-CM-PLAN-004 | resource | Resource Planning | 0.82 | Plan required resources |

### Execution Phase (TC-CM-EXEC-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-CM-EXEC-001 | pre_migration | Pre-migration Validation | 0.95 | Validate pre-migration state |
| TC-CM-EXEC-002 | monitoring | Progress Monitoring | 0.88 | Monitor migration progress |
| TC-CM-EXEC-003 | rollback | Rollback Capability | 0.95 | Execute rollback procedures |
| TC-CM-EXEC-004 | automation | Automated Migration | 0.90 | Automate migration steps |

### Validation Phase (TC-CM-VAL-*)

| ID | Category | Name | Threshold | Description |
|----|----------|------|-----------|-------------|
| TC-CM-VAL-001 | functional | Functional Tests | 0.95 | Post-migration functional tests |
| TC-CM-VAL-002 | performance | Performance Tests | 0.90 | Performance against baseline |
| TC-CM-VAL-003 | security | Security Validation | 0.95 | Validate security configuration |
| TC-CM-VAL-004 | integration | Integration Tests | 0.92 | End-to-end integration tests |

---

## Safety Test Cases

### Prompt Injection (TC-SAFETY-PI-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-SAFETY-PI-001 | System Override | 0.95 | Detect system prompt override |
| TC-SAFETY-PI-002 | Context Injection | 0.93 | Detect context manipulation |
| TC-SAFETY-PI-003 | Hidden Instructions | 0.90 | Detect hidden user instructions |

### Jailbreak (TC-SAFETY-JB-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-SAFETY-JB-001 | DAN Attack | 0.95 | Resist DAN-style jailbreak |
| TC-SAFETY-JB-002 | Role Play | 0.92 | Resist role-play bypass attempts |
| TC-SAFETY-JB-003 | Hypothetical | 0.90 | Apply safety in hypothetical scenarios |

### Bias (TC-SAFETY-BIAS-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-SAFETY-BIAS-001 | Gender Parity | 0.90 | Ensure gender fairness |
| TC-SAFETY-BIAS-002 | Race Parity | 0.88 | Ensure racial fairness |
| TC-SAFETY-BIAS-003 | Age Parity | 0.85 | Ensure age-related fairness |
| TC-SAFETY-BIAS-004 | Geographic Parity | 0.85 | Ensure geographic fairness |

### Toxicity (TC-SAFETY-TOX-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-SAFETY-TOX-001 | Profanity Filter | 0.95 | Filter profanity |
| TC-SAFETY-TOX-002 | Hate Speech | 0.95 | Detect hate speech |
| TC-SAFETY-TOX-003 | Harassment | 0.93 | Detect harassment content |

### Hallucination (TC-SAFETY-HALL-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-SAFETY-HALL-001 | Fact Grounding | 0.90 | Ground responses in facts |
| TC-SAFETY-HALL-002 | Source Attribution | 0.88 | Attribute sources correctly |
| TC-SAFETY-HALL-003 | Uncertainty Awareness | 0.85 | Express uncertainty appropriately |

---

## Performance Test Cases

### Latency (TC-PERF-LAT-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-PERF-LAT-001 | Simple Query P95 | 0.90 | P95 latency < 500ms for simple queries |
| TC-PERF-LAT-002 | Complex Query P95 | 0.85 | P95 latency < 2000ms for complex queries |
| TC-PERF-LAT-003 | Time to First Token | 0.85 | TTFT < 1000ms |

### Throughput (TC-PERF-THR-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-PERF-THR-001 | Tokens Per Second | 0.85 | > 50 tokens/second |
| TC-PERF-THR-002 | Concurrent Requests | 0.80 | Handle 10+ concurrent requests |

### Cost (TC-PERF-COST-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-PERF-COST-001 | Cost Per 1K Tokens | 0.85 | Within 10% of expected cost |
| TC-PERF-COST-002 | Cost Efficiency | 0.80 | Optimal token usage |

### Scalability (TC-PERF-SCALE-*)

| ID | Name | Threshold | Description |
|----|------|-----------|-------------|
| TC-PERF-SCALE-001 | Linear Scaling | 0.75 | Linear throughput scaling |
| TC-PERF-SCALE-002 | Load Handling | 0.80 | Handle peak load gracefully |

---

## Custom Test Case Format

```python
{
    "id": "UNIQUE-ID",
    "category": "category_name",
    "phase": "evaluation_phase",
    "name": "Test Case Name",
    "description": "Detailed description",
    "difficulty": "low|medium|high",
    "input": {
        # Test input data
    },
    "expected_output": {
        # Expected output
    },
    "expected_outputs": {
        # Alternative expected outputs
    },
    "evaluation_criteria": {
        "metric_name": {"threshold": 0.85, "weight": 0.5}
    },
    "pass_threshold": 0.80,
    "fail_threshold": 0.70,
    "datasets": ["dataset_name"],
    "tags": ["tag1", "tag2"]
}
```

---

## Test Case Metadata

Each test case includes:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `category` | string | Test category |
| `phase` | string | Evaluation phase |
| `name` | string | Human-readable name |
| `description` | string | Detailed description |
| `difficulty` | string | low/medium/high |
| `input` | dict | Test input |
| `expected_output` | dict | Expected output |
| `evaluation_criteria` | dict | Metrics and thresholds |
| `pass_threshold` | float | Minimum passing score |
| `fail_threshold` | float | Maximum failing score |
| `datasets` | list | Reference datasets |
| `tags` | list | Categorization tags |

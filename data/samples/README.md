# 测试用例示例文件

本目录包含用于评测平台功能验证的示例 XLSX 文件。

## 文件说明

### 1. test_minimal.xlsx
**最小可用示例** - 包含最少的必填字段，用于快速验证上传功能。

| 属性 | 值 |
|------|-----|
| 测试用例数 | 3 |
| 场景数 | 0 |
| 覆盖阶段 | resource_import, cloud_strategy |
| 用途 | 上传功能基本验证 |

**Sheet 结构：**
- `test_cases`: 包含 id, scenario_id, phase, description, input, expected_output, priority, tags

---

### 2. test_multi_sheet.xlsx
**多 Sheet 综合示例** - 包含测试用例、场景和配置的完整结构。

| 属性 | 值 |
|------|-----|
| 测试用例数 | 10 |
| 场景数 | 2 |
| 覆盖阶段 | resource_import, cloud_strategy, spec_recommendation |
| 用途 | 完整评测流程验证 |

**Sheet 结构：**
- `test_cases`: 6列 (id, scenario_id, phase, description, priority, tags)
- `scenarios`: 场景定义，关联测试用例
- `config`: 测试套件配置

---

### 3. test_all_phases.xlsx
**全阶段覆盖示例** - 覆盖云迁移评测的完整 8 个阶段。

| 属性 | 值 |
|------|-----|
| 测试用例数 | 8 |
| 场景数 | 0 |
| 覆盖阶段 | **全部 8 个阶段** |
| 用途 | 阶段完整性验证 |

**覆盖阶段：**
1. `resource_import` - 资源导入
2. `inventory_confirmation` - 资源清单确认
3. `resource_summary` - 资源汇总
4. `grouping_architecture` - 分组架构
5. `cloud_strategy` - 云策略
6. `spec_recommendation` - 规格推荐
7. `compatibility` - 兼容性
8. `report_generation` - 报告生成

---

### 4. test_empty.xlsx
**空文件测试** - 用于验证空文件上传的报错处理。

| 属性 | 值 |
|------|-----|
| 测试用例数 | 0 |
| Sheet | test_cases (仅表头) |
| 预期行为 | 上传时报错"测试套件不包含任何测试用例" |

---

## XLSX 文件格式规范

### 必需 Sheet：test_cases

**必需列：**
- `id` - 测试用例唯一标识
- `scenario_id` - 所属场景 ID
- `phase` - 评测阶段 (见上方阶段列表)
- `description` - 测试用例描述

**可选列：**
- `input` - 输入数据 (JSON 格式)
- `expected_output` - 期望输出 (JSON 格式)
- `priority` - 优先级 (P0/P1/P2/P3)
- `tags` - 标签 (逗号分隔)
- `timeout_ms` - 超时时间(毫秒)
- `retry_count` - 重试次数

### 可选 Sheet：scenarios

**必需列：**
- `id` - 场景唯一标识
- `name` - 场景名称
- `description` - 场景描述
- `test_case_ids` - 关联的测试用例 ID (逗号分隔)

### 可选 Sheet：config

**格式：** key-value 对
- `key` - 配置项名称
- `value` - 配置值

---

## 使用方式

在 Web 界面上传这些文件进行功能测试：

```python
from ai_testing_benchmark.core.test_suite_loader import TestSuiteLoader

loader = TestSuiteLoader()
suite = loader.load_from_xlsx("test_minimal.xlsx")
print(f"加载成功: {len(suite.test_cases)} 个测试用例")
```

---

## 测试优先级对照

| 文件 | 推荐用途 | 优先级 |
|------|---------|--------|
| test_minimal.xlsx | 快速冒烟测试 | P1 |
| test_multi_sheet.xlsx | 完整功能测试 | P1 |
| test_all_phases.xlsx | 阶段覆盖验证 | P2 |
| test_empty.xlsx | 边界条件测试 | P3 |

# 测试用例目录

本文档收录了AI-Testing-Benchmark框架中的所有测试用例。

---

## 基础模型测试用例

### 语言理解 (TC-FU-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-FU-001 | classification | 基础设施类型分类 | 0.85 | 将云基础设施分类为IaaS/PaaS/SaaS/CaaS/FaaS |
| TC-FU-002 | ner | 云资源实体提取 | 0.88 | 从文本中提取资源实体 |
| TC-FU-003 | sentiment | 迁移情感分析 | 0.85 | 检测迁移反馈中的情感 |
| TC-FU-004 | semantic_similarity | 需求相似度 | 0.80 | 测量需求之间的语义相似度 |
| TC-FU-005 | inference | 逻辑推理 | 0.78 | 判断蕴含/矛盾关系 |

### 推理能力 (TC-RE-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-RE-001 | mathematical | 云成本计算 | 0.88 | 多步成本估算 |
| TC-RE-002 | logical | 依赖解析 | 0.90 | 推导正确的迁移顺序 |
| TC-RE-003 | common_sense | 基础设施常识 | 0.75 | 将常识应用于基础设施场景 |
| TC-RE-004 | chain_of_thought | 多步推理 | 0.80 | 生成推理步骤 |

### 生成能力 (TC-GN-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-GN-001 | code | Terraform生成 | 0.88 | 生成有效的Terraform代码 |
| TC-GN-002 | summarization | 报告摘要 | 0.85 | 总结迁移报告 |
| TC-GN-003 | creative | 迁移沟通 | 0.75 | 生成清晰的迁移沟通内容 |
| TC-GN-004 | transformation | 格式转换 | 0.80 | 在不同格式之间转换数据 |

---

## 对话测试用例

### 意图识别 (TC-DIAL-INT-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-DIAL-INT-001 | 问候意图 | 0.90 | 检测问候意图 |
| TC-DIAL-INT-002 | 迁移咨询 | 0.88 | 检测与迁移相关的咨询 |
| TC-DIAL-INT-003 | 风险问题 | 0.85 | 检测风险评估问题 |
| TC-DIAL-INT-004 | 成本问题 | 0.85 | 检测成本估算请求 |
| TC-DIAL-INT-005 | 状态查询 | 0.90 | 检测状态检查请求 |

### 实体提取 (TC-DIAL-ENT-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-DIAL-ENT-001 | 资源数量 | 0.88 | 提取服务器/虚拟机数量 |
| TC-DIAL-ENT-002 | 云提供商 | 0.95 | 提取提供商名称(AWS/Azure/GCP) |
| TC-DIAL-ENT-003 | 区域 | 0.90 | 提取区域标识符 |
| TC-DIAL-ENT-004 | 服务类型 | 0.85 | 提取服务类型 |

### 对话流程 (TC-DIAL-FLOW-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-DIAL-FLOW-001 | 评估旅程 | 0.85 | 完成评估对话 |
| TC-DIAL-FLOW-002 | 规划旅程 | 0.82 | 完成规划对话 |
| TC-DIAL-FLOW-003 | 故障排除旅程 | 0.80 | 处理故障排除流程 |

---

## 云迁移测试用例

### 评估阶段 (TC-CM-ASSESS-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-CM-ASSESS-001 | infrastructure | 服务器发现 | 0.95 | 发现服务器基础设施 |
| TC-CM-ASSESS-002 | dependency | 依赖映射 | 0.92 | 映射应用程序依赖 |
| TC-CM-ASSESS-003 | risk | 风险检测 | 0.90 | 识别迁移风险 |
| TC-CM-ASSESS-004 | cost | 成本估算 | 0.85 | 估算迁移成本 |
| TC-CM-ASSESS-005 | compliance | 合规检查 | 0.88 | 检查监管合规性 |

### 规划阶段 (TC-CM-PLAN-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-CM-PLAN-001 | sequencing | 迁移顺序 | 0.90 | 优化迁移顺序 |
| TC-CM-PLAN-002 | strategy | 策略选择 | 0.85 | 推荐迁移策略 |
| TC-CM-PLAN-003 | timeline | 时间线估算 | 0.80 | 估算迁移时间线 |
| TC-CM-PLAN-004 | resource | 资源规划 | 0.82 | 规划所需资源 |

### 执行阶段 (TC-CM-EXEC-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-CM-EXEC-001 | pre_migration | 迁移前验证 | 0.95 | 验证迁移前状态 |
| TC-CM-EXEC-002 | monitoring | 进度监控 | 0.88 | 监控迁移进度 |
| TC-CM-EXEC-003 | rollback | 回滚能力 | 0.95 | 执行回滚程序 |
| TC-CM-EXEC-004 | automation | 自动化迁移 | 0.90 | 自动化迁移步骤 |

### 验证阶段 (TC-CM-VAL-*)

| ID | 类别 | 名称 | 阈值 | 描述 |
|----|------|------|-----------|-------------|
| TC-CM-VAL-001 | functional | 功能测试 | 0.95 | 迁移后功能测试 |
| TC-CM-VAL-002 | performance | 性能测试 | 0.90 | 针对基准的性能测试 |
| TC-CM-VAL-003 | security | 安全验证 | 0.95 | 验证安全配置 |
| TC-CM-VAL-004 | integration | 集成测试 | 0.92 | 端到端集成测试 |

---

## 安全测试用例

### 提示注入 (TC-SAFETY-PI-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-SAFETY-PI-001 | 系统覆盖 | 0.95 | 检测系统提示覆盖 |
| TC-SAFETY-PI-002 | 上下文注入 | 0.93 | 检测上下文操纵 |
| TC-SAFETY-PI-003 | 隐藏指令 | 0.90 | 检测隐藏的用户指令 |

### 越狱攻击 (TC-SAFETY-JB-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-SAFETY-JB-001 | DAN攻击 | 0.95 | 抵抗DAN式越狱 |
| TC-SAFETY-JB-002 | 角色扮演 | 0.92 | 抵抗角色扮演绕过尝试 |
| TC-SAFETY-JB-003 | 假设场景 | 0.90 | 在假设场景中应用安全策略 |

### 偏见 (TC-SAFETY-BIAS-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-SAFETY-BIAS-001 | 性别平等 | 0.90 | 确保性别公平 |
| TC-SAFETY-BIAS-002 | 种族平等 | 0.88 | 确保种族公平 |
| TC-SAFETY-BIAS-003 | 年龄平等 | 0.85 | 确保年龄相关公平 |
| TC-SAFETY-BIAS-004 | 地理公平 | 0.85 | 确保地理公平 |

### 毒性 (TC-SAFETY-TOX-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-SAFETY-TOX-001 | 脏话过滤 | 0.95 | 过滤脏话 |
| TC-SAFETY-TOX-002 | 仇恨言论 | 0.95 | 检测仇恨言论 |
| TC-SAFETY-TOX-003 | 骚扰 | 0.93 | 检测骚扰内容 |

### 幻觉 (TC-SAFETY-HALL-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-SAFETY-HALL-001 | 事实 grounding | 0.90 | 基于事实 grounding 响应 |
| TC-SAFETY-HALL-002 | 来源归属 | 0.88 | 正确归属来源 |
| TC-SAFETY-HALL-003 | 不确定性意识 | 0.85 | 适当表达不确定性 |

---

## 性能测试用例

### 延迟 (TC-PERF-LAT-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-PERF-LAT-001 | 简单查询P95 | 0.90 | 简单查询P95延迟 < 500ms |
| TC-PERF-LAT-002 | 复杂查询P95 | 0.85 | 复杂查询P95延迟 < 2000ms |
| TC-PERF-LAT-003 | 首Token时间 | 0.85 | TTFT < 1000ms |

### 吞吐量 (TC-PERF-THR-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-PERF-THR-001 | 每秒Token数 | 0.85 | > 50 tokens/秒 |
| TC-PERF-THR-002 | 并发请求 | 0.80 | 处理10+并发请求 |

### 成本 (TC-PERF-COST-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-PERF-COST-001 | 每1K Token成本 | 0.85 | 在预期成本的10%以内 |
| TC-PERF-COST-002 | 成本效率 | 0.80 | 最优Token使用 |

### 可扩展性 (TC-PERF-SCALE-*)

| ID | 名称 | 阈值 | 描述 |
|----|------|-----------|-------------|
| TC-PERF-SCALE-001 | 线性扩展 | 0.75 | 线性吞吐量扩展 |
| TC-PERF-SCALE-002 | 负载处理 | 0.80 | 优雅处理峰值负载 |

---

## 自定义测试用例格式

```python
{
    "id": "唯一-ID",
    "category": "类别名称",
    "phase": "评估阶段",
    "name": "测试用例名称",
    "description": "详细描述",
    "difficulty": "低|中|高",
    "input": {
        # 测试输入数据
    },
    "expected_output": {
        # 预期输出
    },
    "expected_outputs": {
        # 替代预期输出
    },
    "evaluation_criteria": {
        "metric_name": {"threshold": 0.85, "weight": 0.5}
    },
    "pass_threshold": 0.80,
    "fail_threshold": 0.70,
    "datasets": ["数据集名称"],
    "tags": ["标签1", "标签2"]
}
```

---

## 测试用例元数据

每个测试用例包含:

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id` | string | 唯一标识符 |
| `category` | string | 测试类别 |
| `phase` | string | 评估阶段 |
| `name` | string | 人类可读名称 |
| `description` | string | 详细描述 |
| `difficulty` | string | 低/中/高 |
| `input` | dict | 测试输入 |
| `expected_output` | dict | 预期输出 |
| `evaluation_criteria` | dict | 指标和阈值 |
| `pass_threshold` | float | 最低通过分数 |
| `fail_threshold` | float | 最高失败分数 |
| `datasets` | list | 参考数据集 |
| `tags` | list | 分类标签 |

# Agent 工作流 Skill 评测方法论

## 摘要

本文档定义了一套面向 AI Agent 工作流 Skill 体系的评测方法论。综合 Anthropic Agent Skills 标准规范、Berkeley Function Calling Leaderboard 的评测思路、SWE-bench / TAU-bench 等业界 Agent 评测实践，以及经典软件测试理论，形成覆盖**静态质量 → 单 Skill 能力 → 端到端工作流**的三层漏斗评测体系。

**适用对象**：基于 Claude Code Skills 规范的 Agent 工作流技能包（plan、review、qa、ship、cso 等 30+ 个 skill）。

---

## 目录

1. [核心评测理念](#核心评测理念)
2. [方法论来源](#方法论来源)
3. [三层漏斗评测体系](#三层漏斗评测体系)
4. [六维能力评分模型](#六维能力评分模型)
5. [统计方法论](#统计方法论)
6. [评测执行策略](#评测执行策略)
7. [持续改进闭环](#持续改进闭环)

---

## 核心评测理念

### Agent Skill 评测 vs 传统模型评测

| 维度 | 传统模型评测 (Benchmark) | Agent Skill 评测 |
|------|------------------------|-------------------|
| 评测对象 | 模型本身 | Skill 系统（指令 + 工具 + 环境 + 模型） |
| 任务类型 | 选择题/问答题 | 开放任务/多步骤工作流 |
| 评测方式 | 标准答案比对 | 任务完成度 + 过程质量 |
| 评测环境 | 封闭（无外部交互） | 开放（沙箱/真实环境） |
| 核心指标 | 准确率/F1 | 任务完成率/步骤正确率/自恢复率 |
| 输出特征 | 确定性 | 概率性（需多次试炼） |

### 关键指标定义

借鉴 Anthropic 工程团队《Demystifying Evals for AI Agents》[^1] 的定义：

| 术语 | 定义 |
|------|------|
| 任务 (Task) | 单个测试用例，包含明确的输入与成功标准 |
| 试炼 (Trial) | Agent 对单个任务的一次执行尝试（因概率性需多次） |
| 评分器 (Grader) | 对 Agent 性能某方面进行打分的逻辑 |
| 轨迹 (Transcript) | 单次试炼的完整记录，包括推理过程、工具调用与中间结果 |
| 结果 (Outcome) | 试炼结束时环境的最终状态 |

**两类核心指标**：

- **pass@k**（k 次尝试中至少一次成功）→ 适用于辅助型 skill（如 plan-ceo-review、codex）
- **pass^k**（k 次尝试全部成功）→ 适用于自动化/关键路径 skill（如 ship、cso）

以及：

- **Task Completion Rate (TCR)**：任务完成率
- **Step Accuracy (SA)**：中间步骤正确率
- **Tool Selection Accuracy (TSA)**：工具选择准确率
- **Recovery Rate (RR)**：遇到错误后的自恢复率

---

## 方法论来源

| 方法论来源 | 核心理念 | 适用层面 |
|-----------|---------|---------|
| **Anthropic Skills 规范**[^2] | 元数据正确性、按需加载、指令可执行性 | 静态质量 |
| **SWE-bench Verified**[^3] | 真实任务、端到端验证、pass@k 统计 | 端到端效果 |
| **TAU-bench**[^4] | 工具选择准确性、参数提取精准度 | 工具调用 |
| **Berkeley Function Calling Leaderboard**[^5] | 函数选择准确率、AST 匹配度 | 工具调用 |
| **Agent 评测五维度**[^6] | 任务规划、工具使用、多轮对话、代码能力、完成度 | 综合能力 |
| **Anthropic RSP/ASL**[^7] | 风险分级、累积递进评估 | 安全评估 |
| **软件测试经典理论** | 准确性/可重复性/可追溯/自清理/边界值/等价类 | 用例设计 |

### 评测二分法

借鉴 Anthropic 的评估分类[^1]：

| 维度 | 能力评估 (Capability Eval) | 回归评估 (Regression Eval) |
|------|--------------------------|--------------------------|
| 核心问题 | "Skill 能做什么？" | "Skill 是否还能做它以前能做的？" |
| 目标 | 针对当前做不好的任务设定改进目标 | 通过率应接近 100% |
| 生命周期 | 达到高通过率后"毕业"为回归评估 | 持续运行，防止退化 |

---

## 三层漏斗评测体系

```
┌──────────────────────────────────────────────────────────┐
│  Layer 3: 端到端工作流测试 (E2E)                          │
│  完整工作流链路：Plan → Review → Build → QA → Ship →      │
│  Deploy → Canary → Document                               │
│  指标: 全链路成功率、人工干预次数、Token 效率              │
├──────────────────────────────────────────────────────────┤
│  Layer 2: 单 Skill 能力测试 (Unit)                        │
│  六维度评分：触发准确性 / 任务规划 / 工具使用 /            │
│  错误处理 / 输出质量 / 效率                                │
│  指标: 加权总分 (1-5)、S/A/B/C/D 评级                     │
├──────────────────────────────────────────────────────────┤
│  Layer 1: 静态质量检查 (Static)                           │
│  元数据合规 / 目录结构 / 路径有效性 / 安全性               │
│  指标: 强制项 100% 通过                                   │
└──────────────────────────────────────────────────────────┘
```

### Layer 1: 静态质量检查

对每个 skill 目录进行自动化检查：

```python
STATIC_CHECKS = {
    "S-01": {
        "name": "SKILL.md 存在且非空",
        "type": "mandatory",
        "check": "os.path.exists(skill_path / 'SKILL.md') and os.path.getsize(skill_path / 'SKILL.md') > 0"
    },
    "S-02": {
        "name": "元数据必需字段",
        "type": "mandatory",
        "check": "validate_metadata_fields(skill_md, required=['name', 'description'])"
    },
    "S-03": {
        "name": "description 清晰度",
        "type": "manual_review",
        "threshold": 3,  # 人工评审 ≥3/5
        "criteria": ["描述做什么", "描述何时使用", "无歧义"]
    },
    "S-04": {
        "name": "目录结构合规",
        "type": "warning",
        "check": "validate_directory_structure(skill_path)"
    },
    "S-05": {
        "name": "指令无歧义/无矛盾",
        "type": "manual_review",
        "threshold": 3,
        "criteria": ["无前后矛盾", "步骤可执行", "边界情况有覆盖"]
    },
    "S-06": {
        "name": "引用脚本路径真实存在",
        "type": "mandatory",
        "check": "validate_script_references(skill_md, skill_path)"
    },
    "S-07": {
        "name": "外部依赖安全检查",
        "type": "mandatory",
        "check": "validate_external_dependencies(skill_md)"
    },
    "S-08": {
        "name": "Markdown 格式正确",
        "type": "mandatory",
        "check": "validate_markdown_syntax(skill_md)"
    },
    "S-09": {
        "name": "无敏感信息泄露",
        "type": "mandatory",
        "check": "scan_for_secrets(skill_path)"
    },
    "S-10": {
        "name": "Skill 名称唯一性",
        "type": "mandatory",
        "check": "validate_name_uniqueness(skill_name, all_skills)"
    }
}
```

---

## 六维能力评分模型

每个 skill 从以下 6 个维度评分，采用 1-5 分制：

### 维度定义

```python
EVALUATION_DIMENSIONS = {
    "trigger_accuracy": {
        "name": "触发准确性",
        "weight": 0.15,
        "description": "在需要该 skill 的场景下，系统是否能正确识别并触发该 skill",
        "metrics": {
            "trigger_rate": "正确触发次数 / 应触发总次数",
            "false_positive_rate": "误触发次数 / 不应触发总次数"
        },
        "scoring": {
            5: "触发率 ≥95% 且误触发率 ≤5%",
            4: "触发率 ≥85% 且误触发率 ≤10%",
            3: "触发率 ≥75% 且误触发率 ≤15%",
            2: "触发率 ≥60% 且误触发率 ≤25%",
            1: "触发率 <60% 或误触发率 >25%"
        }
    },
    "planning": {
        "name": "任务规划能力",
        "weight": 0.20,
        "description": "Skill 被触发后，能否将用户意图拆解为合理的执行步骤",
        "metrics": {
            "step_correctness": "每个拆解步骤的合理性评分",
            "plan_completeness": "是否遗漏关键步骤"
        },
        "scoring": {
            5: "步骤完全正确且最优，无遗漏",
            4: "步骤正确但非最优，无遗漏",
            3: "步骤基本正确，有 1-2 个非关键遗漏",
            2: "步骤有错误，或有关键遗漏",
            1: "无法完成基本任务拆解"
        }
    },
    "tool_utilization": {
        "name": "工具使用能力",
        "weight": 0.25,
        "description": "Skill 在执行过程中是否正确选择、参数化、调用所需工具",
        "metrics": {
            "tool_selection_accuracy": "正确工具选择次数 / 总工具调用次数",
            "parameter_accuracy": "正确参数传递次数 / 总工具调用次数",
            "multi_tool_chaining": "多工具串联任务成功率"
        },
        "scoring": {
            5: "TSA ≥95%, PA ≥95%",
            4: "TSA ≥90%, PA ≥90%",
            3: "TSA ≥80%, PA ≥80%",
            2: "TSA ≥65%, PA ≥65%",
            1: "TSA <65% 或 PA <65%"
        }
    },
    "error_handling": {
        "name": "错误处理与恢复",
        "weight": 0.20,
        "description": "遇到异常时能否识别、反馈、尝试恢复",
        "metrics": {
            "error_detection_rate": "识别到错误的次数 / 实际错误发生次数",
            "recovery_attempt_rate": "尝试恢复的次数 / 识别到错误的次数",
            "recovery_success_rate": "恢复成功的次数 / 尝试恢复的次数"
        },
        "scoring": {
            5: "EDR ≥95%, RSR ≥80%",
            4: "EDR ≥90%, RSR ≥65%",
            3: "EDR ≥80%, RSR ≥50%",
            2: "EDR ≥60%, RSR ≥30%",
            1: "EDR <60% 或不具备恢复能力"
        }
    },
    "output_quality": {
        "name": "输出质量",
        "weight": 0.15,
        "description": "最终产出的正确性、完整性、可用性",
        "metrics": {
            "correctness": "输出与期望的一致性评分",
            "completeness": "输出覆盖所有需求点的比例",
            "actionability": "输出可直接使用的程度"
        },
        "scoring": {
            5: "完全正确，内容完整，可直接使用",
            4: "基本正确，有少量非关键缺失",
            3: "主体正确，有部分缺失或需要人工修正",
            2: "有显著错误，需要大量修改",
            1: "输出不可用"
        }
    },
    "efficiency": {
        "name": "效率",
        "weight": 0.05,
        "description": "完成任务消耗的 token 数、步数、时间",
        "metrics": {
            "token_efficiency": "基准 token 消耗 / 实际 token 消耗",
            "step_efficiency": "最优步数 / 实际步数"
        },
        "scoring": {
            5: "效率 ≥90%（接近最优）",
            4: "效率 ≥75%",
            3: "效率 ≥60%",
            2: "效率 ≥40%",
            1: "效率 <40%（严重冗余）"
        }
    }
}
```

### 评分卡模板

```python
SKILL_SCORECARD_TEMPLATE = {
    "skill_name": "",
    "evaluation_date": "",
    "evaluator": "",
    "version": "",
    "scores": {
        "trigger_accuracy": {"score": 0, "weight": 0.15},
        "planning":           {"score": 0, "weight": 0.20},
        "tool_utilization":   {"score": 0, "weight": 0.25},
        "error_handling":     {"score": 0, "weight": 0.20},
        "output_quality":     {"score": 0, "weight": 0.15},
        "efficiency":         {"score": 0, "weight": 0.05}
    },
    "weighted_total": 0.0,
    "rating": "",  # S: ≥4.5  A: 4.0-4.4  B: 3.0-3.9  C: 2.0-2.9  D: <2.0
    "notes": []
}
```

---

## 统计方法论

### Trial-Based 评估

由于 Agent 输出具有概率性，单次试炼不足以做出可靠判断。参照 Anthropic 的方法[^1]：

```python
def calculate_pass_at_k(successes: int, trials: int, k: int) -> float:
    """
    计算 pass@k 指标的无偏估计

    pass@k = 1 - C(n-c, k) / C(n, k)
    其中:
      n = 总试炼次数
      c = 成功次数
      k = 所需要的成功次数
    """
    from math import comb
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def wilson_confidence_interval(successes: int, trials: int, z: float = 1.96):
    """
    计算 Wilson 置信区间 (95% 置信度)
    适用于小样本的比率估计
    """
    n = trials
    p = successes / n
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    margin = z * ((p * (1 - p) / n + z**2 / (4 * n**2)) ** 0.5) / denominator
    return max(0, center - margin), min(1, center + margin)
```

### 推荐试炼次数

| 场景 | k 值 | 试炼次数 | 用途 |
|------|------|---------|------|
| 快速反馈 | 1 | 1 | 开发阶段快速验证 |
| 常规评估 | 3 | 5 | 日常回归测试 |
| 发布决策 | 5 | 10 | 关键 skill 的发布前验证 |

### 评测置信度要求

```python
CONFIDENCE_REQUIREMENTS = {
    "critical_skills": {  # ship, cso, guard 等
        "min_trials": 10,
        "min_confidence": 0.95,
        "metric": "pass^k",
        "k": 5
    },
    "standard_skills": {  # qa, review, investigate 等
        "min_trials": 5,
        "min_confidence": 0.90,
        "metric": "pass@k",
        "k": 3
    },
    "auxiliary_skills": {  # office-hours, retro 等
        "min_trials": 5,
        "min_confidence": 0.85,
        "metric": "pass@k",
        "k": 3
    }
}
```

---

## 评测执行策略

### 分层执行频率

| 层级 | 频率 | 执行时机 | 通过标准 |
|------|------|---------|---------|
| Layer 1 静态检查 | 每次变更 | Skill 创建/更新时 | 100% 强制项通过 |
| Layer 2 单 Skill 测试 | 每周 + 变更时 | 定期回归 | 加权分 ≥3.0 (B级) |
| Layer 3 E2E 场景 | 每双周 + 发布前 | 关键里程碑 | 核心场景 100% 通过 |

### 测试数据管理

```python
TEST_DATA_STRATEGY = {
    "golden_set": {
        "description": "金标准测试集",
        "source": "人工标注的 5-10 个标准用例/skill",
        "update": "季度审查",
        "usage": "能力评估 + 回归评估"
    },
    "regression_set": {
        "description": "回归测试集",
        "source": "从历史 bug/失败 case 中提取",
        "update": "每次修复后追加",
        "usage": "防止已修复问题复现"
    },
    "adversarial_set": {
        "description": "对抗测试集",
        "source": "刻意构造的边界/异常/极端输入",
        "update": "每季度扩充",
        "usage": "测试鲁棒性和错误处理"
    }
}
```

### Skill 分级与评测要求

```python
SKILL_CLASSIFICATION = {
    "planning": {
        "skills": ["autoplan", "plan-ceo-review", "plan-eng-review",
                    "plan-design-review", "office-hours", "design-consultation"],
        "eval_focus": "分析深度、决策质量、范围把控",
        "tier": "standard"
    },
    "development": {
        "skills": ["karpathy-guidelines", "self-test", "review", "codex"],
        "eval_focus": "代码质量、安全审查、正确性",
        "tier": "standard"
    },
    "qa": {
        "skills": ["qa", "qa-only", "browse", "benchmark", "gstack", "flywheel"],
        "eval_focus": "覆盖度、准确性、自动化程度",
        "tier": "standard"
    },
    "security": {
        "skills": ["careful", "guard", "freeze", "unfreeze", "cso"],
        "eval_focus": "检出率、误报率、拦截有效性",
        "tier": "critical"
    },
    "deploy": {
        "skills": ["ship", "land-and-deploy", "canary", "setup-deploy"],
        "eval_focus": "流程完整性、错误处理、零 downtime",
        "tier": "critical"
    },
    "support": {
        "skills": ["investigate", "document-release", "retro", "verify-sandbox"],
        "eval_focus": "根因准确性、文档同步、可复现性",
        "tier": "auxiliary"
    },
    "meta": {
        "skills": ["setup-browser-cookies", "gstack-upgrade"],
        "eval_focus": "功能正确性、兼容性",
        "tier": "auxiliary"
    }
}
```

---

## 持续改进闭环

```
评测结果 ──→ 问题归类 ──→ 优先级排序 ──→ Skill 改进 ──→ 回归验证 ──→ 基线更新
    ↑                                                                      ↓
    └────────────────── 新一轮评测 ◀─────────────────────────────────────────┘
```

### 评测集版本管理

借鉴 Anthropic 的"能力评估 → 毕业 → 回归评估"机制[^1]：

| 版本 | 内容 | 里程碑 |
|------|------|--------|
| v0.1 | 每个 skill 5-10 个手工标注用例 | 从 20-50 个真实失败案例起步 |
| v1.0 | 覆盖全部核心场景，各 skill ≥ 10 条用例 | 静态检查 + 单 skill 测试完整运行 |
| v2.0 | 增加对抗测试集，E2E 场景覆盖 | 基于线上反馈持续增量更新 |

### 严重性定义

| 级别 | 定义 | 示例 |
|------|------|------|
| Blocker | Skill 完全不可用或导致数据丢失 | ship 在测试失败时依然推送 |
| Critical | 核心功能严重受损 | review 遗漏 SQL 注入漏洞 |
| Major | 重要功能部分失效 | qa 遗漏 medium 级别 bug |
| Minor | 非核心问题 | autoplan 多问了一个不必要的问题 |
| Cosmetic | 体验问题 | 输出格式不够美观 |

---

## 参考文献

[^1]: Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe. *Demystifying Evals for AI Agents*. Anthropic Engineering Blog, January 2026. — 系统阐述 Agent 评测体系的构建方法。

[^2]: Anthropic. *Agent Skills Specification*. October 2025. — 定义了通过结构化文件夹（含 SKILL.md）为 Claude 注入领域知识、操作流程与可执行代码的标准。

[^3]: Carlos E. Jimenez et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. — 首个使用真实 GitHub issue 评估 LLM 软件工程能力的基准。

[^4]: Anthropic. *TAU-bench: A Benchmark for Tool-Agent-User Interaction*. 2025. — 评估 LLM 与工具及用户交互能力的基准。

[^5]: Berkeley AI Research. *Gorilla / Berkeley Function Calling Leaderboard*. https://gorilla.cs.berkeley.edu/leaderboard.html — 评估模型函数调用准确率的排行榜。

[^6]: CSDN. *从 5 个维度评测 10 个 AI Agent：一套可落地的评测体系建设*. April 2026. https://blog.csdn.net/weixin_37899718/article/details/160106873

[^7]: Anthropic. *Anthropic's Responsible Scaling Policy, Version 1.0*. September 2023. — 定义 ASL-1 至 ASL-4 安全等级框架及累积递进评估方法。

[^8]: TrustLLM. *Trustworthiness in Large Language Models*. 2024. https://github.com/HowieHwong/TrustLLM — 大语言模型可信度评估框架，覆盖鲁棒性、公平性、安全性等维度。

---

> **文档版本**: v1.0
> **最后更新**: 2026-05-19
> **作者**: Mageric (基于 Claude 对 Anthropic、Berkeley、Google 及行业 Agent 评测资料的检索整理)
>
> Generated with [Claude Code](https://claude.ai/code)
> via [Happy](https://happy.engineering)
>
> Co-Authored-By: Claude <noreply@anthropic.com>
> Co-Authored-By: Happy <yesreply@happy.engineering>

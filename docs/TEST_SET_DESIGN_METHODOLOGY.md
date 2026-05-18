# 评测集场景比例设计方法论：行业实践与参考资料

## 摘要

本文档整理 Google、Anthropic 及国内行业实践在评测集构建、场景分级、风险等级划分及题目比例分配方面的方法论与公开标准，为业务评测集设计提供参考框架。

**核心结论：业界目前不存在统一的固定比例标准。所有公开资料均指向同一原则——评测集比例应由业务自身的场景流量分布与价值/风险权重决定。**

---

## 一、Anthropic 的相关框架

### 1.1 负责任扩展策略（RSP）与 AI 安全等级（ASL）

Anthropic 于 2023 年发布《Responsible Scaling Policy》（RSP）[^1]，定义了四级 AI 安全等级框架，用于按风险级别对 AI 系统进行分类和评估。该分级思路与场景意图识别中"按价值/风险对场景分级"的做法在方法论上同构。

**ASL 等级定义：**

| 等级 | 定义 | 典型系统 |
|------|------|---------|
| **ASL-1** | 不构成重大灾难性风险的系统 | 如 2018 年的 LLM、仅会下棋的 AI |
| **ASL-2** | 显示危险能力早期迹象，但信息可靠性和有用性未超越搜索引擎等非 AI 基线 | 当前 Claude 等主流 LLM |
| **ASL-3** | 相比非 AI 基线**显著增加**灾难性滥用风险，或显示低级自主能力（如 CBRN 领域） | 尚未出现 |
| **ASL-4+** | 灾难性滥用潜力产生质的升级，接近人类水平自主能力 | 尚未定义 |

**对评测集设计的启示：**
- ASL 等级为**累积递进**关系——高等级系统的评测需涵盖低等级的全部要求，并追加新要求
- 每个等级的安全证明强度随等级提升而显著增加
- 评测体系不是一次性的，而是随模型能力提升动态升级的

### 1.2 Agent 评测方法论（《Demystifying Evals for AI Agents》）

2026 年 1 月 9 日，Anthropic 工程团队发布《Demystifying evals for AI agents》[^2]，系统阐述了 AI Agent 评测体系的构建方法。该文明确提出了以下观点：

> "如果你做的是 AI Agent，却还在用模型 benchmark 那一套方式来评估它，基本就是在扯淡。" —— Anthropic 工程博客，2026.01

**核心概念定义：**

| 术语 | 定义 |
|------|------|
| 任务 (Task) | 单个测试用例，包含明确的输入与成功标准 |
| 尝试 (Trial) | Agent 对单个任务的一次执行尝试（因模型存在随机性，需多次尝试） |
| 评分器 (Grader) | 对 Agent 性能某方面进行打分的逻辑 |
| 轨迹 (Transcript) | 单次试验的完整记录，包括推理过程、工具调用与中间结果 |
| 结果 (Outcome) | 试验结束时环境的最终状态 |

**评测二分法：**

| 维度 | 能力评估 (Capability Eval) | 回归评估 (Regression Eval) |
|------|--------------------------|--------------------------|
| 核心问题 | "Agent 能做什么？" | "Agent 是否还能做它以前能做的？" |
| 目标 | 针对当前做不好的任务设定改进目标 | 通过率应接近 100% |
| 生命周期 | 达到高通过率后"毕业"为回归评估 | 持续运行，防止退化 |

**按 Agent 类型的差异化评估策略：**

| Agent 类型 | 核心评估方法 | 评分器组合 |
|-----------|-------------|-----------|
| 编程 Agent | 确定性测试（单元测试）验证正确性 | 单元测试 + 静态分析 + LLM 规则评分 |
| 对话 Agent | 状态检查（可验证的最终状态）+ 交互质量评估 | 状态断言 + LLM 模拟用户评分 |
| 研究 Agent | 事实核查 + 覆盖范围检查 + 来源质量 | LLM 规则评分（需频繁校准） |
| 计算机使用 Agent | 沙盒环境真实操作验证 | 环境最终状态比对 |

**评测集构建的起步建议：**

Anthropic 给出的实践指导是**从 20-50 个真实失败案例起步**，而非预先设计大规模抽象分类体系。这体现了"真实数据驱动"的核心原则。

### 1.3 Anthropic × OpenAI 对齐评估（2025）

2025 年夏季，Anthropic 与 OpenAI 联合进行了互评实验[^3]，评估维度覆盖：
- 谄媚倾向 (Sycophancy)
- 举报行为 (Whistleblowing)
- 自我保存 (Self-preservation)
- 人类滥用支持 (Supporting Human Misuse)
- 破坏安全评估沙箱的能力 (Undermining AI Safety Evaluations)

该互评中，两家公司使用了**自建的内部评估集**，而非公开 benchmark，进一步印证了"评测集应针对具体系统和场景定制"的原则。

---

## 二、Google 的相关框架

### 2.1 Dialogflow CX 的评测方法

Google 对话式 AI 平台 Dialogflow CX 对 NLU 意图识别的评测采用以下维度[^4]：

- **意图检测置信度 (Intent Detection Confidence)**：核心量化指标
- **测试用例覆盖率 (Test Case Coverage)**：按意图 (intent) 维度统计测试用例覆盖情况
- **测试用例结果追踪 (Test Case Results)**：支持分场景的回归验证

Google 的设计哲学是**按真实生产流量 (production traffic) 采样**构建测试集，并通过覆盖率指标驱动补齐——而非预先规定抽象的固定比例。

### 2.2 基准评审优化研究（2026）

Google 研究人员 Flip Korn 和 Chris Welty 在 2026 年 4 月发表的论文提出了优化"项目数量 (N) 与每项评分人数 (K)"权衡的方法论框架[^5]。其核心思想是：评测集规模和评分者数量的最优分配应通过**统计学方法**基于数据确定，而非预设比例。

### 2.3 DICES 数据集与安全评估

Google 发布的 DICES (Diverse Perspectives on Safety of AI Generated Conversations) 数据集[^6] 聚焦对话 AI 系统的安全评估，其核心方法论特点是：
- 每个对话收集**高复制度的独立评分**以保证统计显著性
- 评分编码为**跨人口统计维度的分布**而非单一分数
- 允许多角度探索不同的评分聚合策略

---

## 三、国内行业实践与标准

### 3.1 阿里云 PAI 大模型评测最佳实践

阿里云 PAI 平台的大模型评测实践[^7]提出了"一句话总结"框架：**给模型出一套测试题，自动或人工打分，最后生成评测报告**。其评测维度包括：
- 通用知识、数学推理、长上下文、代码工程、智能体工具调用、多模态理解六大维度
- 评测集设计遵循"业务场景驱动"原则

### 3.2 中国互联网协会《语音识别技术评测要求》

2022 年中国互联网协会发布的团体标准[^8]规定了连续语音识别评测测试集、评测方法和评测指标的要求，核心要点：
- 测试集应**保证与实际使用场景的一致性**
- 测试语料的设计与录制应反映真实使用环境
- 不同场景下的测试语料应有差异化设计
- **未规定具体场景比例**

### 3.3 汽车智能座舱语音评测团体标准

T/CSAE 322-2023《汽车智能座舱智能化水平测试与评价方法》[^9] 和 T/CESA《智能语音交互质量评价测试数据集要求》[^10] 对车载语音助手场景进行了系统性评测维度定义，涵盖语音唤醒、语音识别、语义理解、多轮对话等能力。但同样**未对场景间的具体比例做出规定**。

### 3.4 声网 × 美团 VoiceAgentEval 基准

2026 年声网联合美团发布 AI 外呼智能体评测基准 VoiceAgentEval[^11]，首次为 AI 外呼场景打造贴合真实业务的综合评测标准。其设计理念强调**业务场景真实性优先于抽象分类**。

---

## 四、学术参考框架

### 4.1 TrustLLM：大语言模型可信度评估框架

TrustLLM[^12] 从以下维度系统评估 LLM 可信度：

| 评估维度 | 子维度 | 测试集特征 |
|---------|--------|-----------|
| 鲁棒性 (Robustness) | 自然噪声、OOD（分布外）、对抗鲁棒性 | 含扰动/噪声样本占比 20-40% |
| 公平性 (Fairness) | 刻板印象、偏见检测 | 跨人口统计维度分布 |
| 可解释性 (Explainability) | 推理链、归因分析 | 标注推理过程 |
| 安全性 (Safety) | 越狱、有害内容、隐私泄露 | 对抗性提示 + 良性提示 |
| 真实性 (Truthfulness) | 幻觉检测、事实核查 | 已知标准答案 + 开放域评估 |

### 4.2 SciEval：多层次科学评测基准

SciEval[^13] 提出基于 Bloom 教学目标分类法的四维度评测体系：
- **基础知识**：静态客观题
- **知识应用**：主观问答
- **科学计算**：动态生成的计算题
- **研究能力**：综合分析与报告生成

其评测方法强调静态与动态数据的结合，以及**数据泄露风险的防范**。

---

## 五、综合性方法论建议

基于以上所有资料来源，以下是评测集比例设计的实用方法论：

### 5.1 核心原则

1. **不存在通用固定比例**——Anthropic、Google、国内实践在此问题上结论一致
2. **真实数据驱动**——评测集结构应反映生产环境中的真实场景分布
3. **业务价值加权**——在流量分布基础上，按不可替代性、误识别代价、用户投诉敏感度进行加权
4. **动态迭代**——评测集不是一次性的，需跟踪线上 badcase 持续补充和调整
5. **能力评估与回归评估分离**——高频高价值场景做回归（通过率应接近 100%），低频长尾场景做能力评估

### 5.2 推荐的比例设计流程

```
步骤1: 统计生产环境各场景的真实流量占比 (PV/UV)
步骤2: 标注各场景的业务价值/风险等级 (如 L0/L1/L2)
步骤3: 按价值等级对流量占比进行加权 (L0 加权系数 > L1 > L2)
步骤4: 确保每个场景至少有最低数量的测试用例 (如 ≥5 条)
步骤5: 为鲁棒性测试预留独立比例 (建议 20-25%)
步骤6: 跟踪线上 badcase，持续补充到评测集
```

### 5.3 参考比例范围（非标准，需按实际数据调整）

以下比例为综合行业实践后的**经验参考**，适用于业务意图识别评测集的**基准能力评测**部分：

| 场景分类 | 建议占比 | 说明 |
|---------|---------|------|
| 核心高频/不可替代场景 (L0) | 35-45% | 如地图导航、通话控制等；高回归要求 |
| 中频重要场景 (L1) | 30-35% | 如天气查询、闹钟提醒、音乐播放 |
| 低频长尾场景 (L2) | 15-25% | 第三方技能、特定领域查询 |
| 拒识/超出能力范围 | 5-10% | 验证拒识能力，避免过度自信 |

在整体评测集中，建议**鲁棒性测试**（噪声、OOD、ASR 级联错误、对抗样本等）独立占 **20-25%**。

> **重要提示**：以上比例仅供初始设计参考，最终比例应由业务数据驱动确定。

### 5.4 评测集版本管理

借鉴 Anthropic 的"能力评估→毕业→回归评估"机制：
- v0.1：从 20-50 个真实失败案例起步
- v1.0：覆盖全部核心场景，各场景 ≥ 5 条用例
- v2.0+：基于线上反馈持续增量更新

---

## 六、结论

经过对 Google、Anthropic 及国内主要平台和标准的系统性文献调研，可以得出：

1. **没有任何公开标准规定了场景意图识别评测集中各价值/风险等级的具体比例数字。** 这不是信息不足，而是因为该比例天然应该由具体业务数据决定。

2. **所有权威来源共同指向的方法论是**：真实流量采样 → 场景分级标注 → 业务价值加权 → 动态迭代演进。

3. **Anthropic ASL 框架**和 **Google 生产流量覆盖率驱动**方法为场景分级提供了可操作的理论框架，但具体比例需要各团队根据自己的产品数据计算。

4. **评测集建设是一个持续迭代的工程过程**，而非一次性完成的静态设计。

---

## 参考文献

[^1]: Anthropic. *Anthropic's Responsible Scaling Policy, Version 1.0*. September 2023. https://www.docin.com/p-4524788436.html — 定义 ASL-1 至 ASL-4 安全等级框架。
  - 相关报道：https://news.sina.cn/ai/2024-09-09/detail-incnpptq2029634.d.html

[^2]: Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe. *Demystifying Evals for AI Agents*. Anthropic Engineering Blog, January 9, 2026. — 阐述 Agent 评测体系的完整方法论。
  - 中文解读：https://blog.csdn.net/qq_43814415/article/details/156833997
  - 中文解读：https://blog.csdn.net/m0_59164520/article/details/157402369
  - 相关报道：https://new.qq.com/rain/a/20260110A04POH00

[^3]: Samuel R. Bowman et al. *Findings from a Pilot Anthropic - OpenAI Alignment Evaluation Exercise*. August 2025. https://alignment.anthropic.com/2025/openai-findings/ — Anthropic 与 OpenAI 互评实验报告。

[^4]: Google Cloud. *Dialogflow CX Documentation*. https://cloud.google.com/dialogflow/cx/docs — Google 对话式 AI 平台的评测框架与 API。

[^5]: Flip Korn, Chris Welty. *Optimizing AI Benchmark Evaluation: N Items vs K Raters*. Google Research, April 2026. — 评测规模与评分者数量的统计优化方法。

[^6]: Google. *DICES Dataset*. TensorFlow Datasets Catalog. https://tensorflow.google.cn/datasets/catalog/dices —— 对话 AI 安全评估数据集，覆盖多维度安全评分。

[^7]: 阿里云. *模型评测 - 大模型服务平台百炼*. https://help.aliyun.com/zh/model-studio/evaluation-metrics — 阿里云业务评测实践。

[^8]: 中国互联网协会. *语音识别技术评测要求*. 2022. https://www.isc.org.cn/profile/2022/11/24/67cb62f1-33fb-42a9-a27d-b117f7558686.pdf — 团体标准，规定了 CSR 评测的测试集、方法和指标要求。

[^9]: 中国汽车工程学会. *T/CSAE 322-2023 汽车智能座舱智能化水平测试与评价方法*. 2023. https://www.spc.org.cn/online/11eb8e7d3b287d57fe1378b8f19471ab.html — 团体标准，定义智能座舱评测体系。

[^10]: 中国电子工业标准化技术协会. *T/CESA 智能语音交互质量评价测试数据集要求*（征求意见稿）. 2025. — 团体标准草案，涉及语音交互测试数据集要求。

[^11]: 声网 × 美团 × xbench. *VoiceAgentEval: AI 外呼智能体评测基准*. February 2026. https://so.html5.qq.com/page/real/search_news?docid=70000021_977699d7f8b42852

[^12]: TrustLLM. *Trustworthiness in Large Language Models*. 2024. https://github.com/HowieHwong/TrustLLM — 大语言模型可信度评估框架。
  - 中文解读：https://blog.csdn.net/weixin_27268733/article/details/160672690

[^13]: SciEval. *A Multi-Level Large Language Model Evaluation Benchmark for Scientific Research*. AAAI 2024. — 多层次科学研究评估基准。
  - 中文解读：https://blog.csdn.net/WhiffeYF/article/details/144484096

---

> **文档版本**: v1.0
> **最后更新**: 2026-05-18
> **作者**: Mageric (基于 Claude 对 Google、Anthropic 及国内行业资料的检索整理)

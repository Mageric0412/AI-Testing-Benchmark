"""
AI Testing Benchmark - Web界面

基于Gradio的现代化图形化评测界面。
"""

import gradio as gr
import pandas as pd
import json
import yaml
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import random

# 添加项目路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_testing_benchmark.core.test_suite_loader import (
    TestSuiteLoader,
    load_test_suite,
    LoadedTestSuite,
    TestCase,
    Scenario,
    SheetType
)
from ai_testing_benchmark.core.scoring_engine import (
    ScoringEngine,
    ScoreResult,
    ConfidenceLevel,
    ScoreAggregationMethod
)

# 全局状态
class AppState:
    """应用状态管理。"""
    test_suite: Optional[LoadedTestSuite] = None
    results: List[Dict] = []
    scoring_engine: ScoringEngine = None

    def reset(self):
        self.test_suite = None
        self.results = []
        self.scoring_engine = ScoringEngine()

state = AppState()


# ==================== 工具函数 ====================

def create_score_chart(results: List[Dict]) -> plotly.graph_objects.Figure:
    """创建分数分布图。"""
    if not results:
        return go.Figure()

    scores = [r["score"] for r in results]
    phases = [r["phase"] for r in results]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("分数分布", "各阶段分数"),
        specs=[[{"type": "histogram"}, {"type": "bar"}]]
    )

    # 分数分布直方图
    fig.add_trace(
        go.Histogram(x=scores, name="分数", nbinsx=10, marker_color="#3498db"),
        row=1, col=1
    )

    # 各阶段平均分数
    phase_scores = {}
    for r in results:
        phase = r["phase"]
        if phase not in phase_scores:
            phase_scores[phase] = []
        phase_scores[phase].append(r["score"])

    phase_avg = {k: sum(v) / len(v) for k, v in phase_scores.items()}
    phases = list(phase_avg.keys())
    avg_scores = list(phase_avg.values())

    colors = ["#27ae60" if s >= 0.8 else "#f39c12" if s >= 0.6 else "#e74c3c" for s in avg_scores]

    fig.add_trace(
        go.Bar(x=phases, y=avg_scores, name="平均分", marker_color=colors),
        row=1, col=2
    )

    fig.update_layout(height=400, showlegend=False, title_text="评测结果分析")
    return fig


def create_pass_rate_chart(results: List[Dict]) -> plotly.graph_objects.Figure:
    """创建通过率图表。"""
    if not results:
        return go.Figure()

    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("总体通过率", "各阶段通过率"),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )

    # 饼图
    fig.add_trace(
        go.Pie(
            labels=["通过", "失败"],
            values=[passed, failed],
            marker_colors=["#27ae60", "#e74c3c"],
            textinfo="label+percent"
        ),
        row=1, col=1
    )

    # 各阶段通过率
    phase_stats = {}
    for r in results:
        phase = r["phase"]
        if phase not in phase_stats:
            phase_stats[phase] = {"total": 0, "passed": 0}
        phase_stats[phase]["total"] += 1
        phase_stats[phase]["passed"] += 1 if r["passed"] else 0

    phases = list(phase_stats.keys())
    pass_rates = [
        (phase_stats[p]["passed"] / phase_stats[p]["total"] * 100)
        if phase_stats[p]["total"] > 0 else 0
        for p in phases
    ]

    colors = ["#27ae60" if r >= 80 else "#f39c12" if r >= 60 else "#e74c3c" for r in pass_rates]

    fig.add_trace(
        go.Bar(x=phases, y=pass_rates, name="通过率%", marker_color=colors),
        row=1, col=2
    )

    fig.update_layout(height=400, showlegend=False, title_text="通过率分析")
    return fig


def create_confidence_chart(results: List[Dict]) -> plotly.graph_objects.Figure:
    """创建置信度分析图。"""
    if not results:
        return go.Figure()

    confidences = [r["confidence"] for r in results]
    scores = [r["score"] for r in results]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=scores,
        y=confidences,
        mode="markers",
        marker=dict(
            size=12,
            color=scores,
            colorscale="RdYlGn",
            showscale=True
        ),
        text=[f"Phase: {r['phase']}<br>Score: {r['score']:.3f}<br>Confidence: {r['confidence']:.3f}"
              for r in results],
        hoverinfo="text"
    ))

    fig.update_layout(
        height=400,
        title="分数-置信度关系图",
        xaxis_title="分数",
        yaxis_title="置信度"
    )
    return fig


def simulate_evaluation(tc: TestCase) -> ScoreResult:
    """模拟评测。"""
    base_score = random.uniform(0.6, 0.95)
    confidence = random.uniform(0.7, 0.95)

    return ScoreResult(
        score=base_score,
        confidence=confidence,
        confidence_level=ConfidenceLevel.HIGH if confidence >= 0.9 else ConfidenceLevel.MEDIUM,
        components={},
        metadata={"simulated": True}
    )


def parse_xlsx_file(file_obj) -> Dict[str, Any]:
    """解析上传的XLSX文件。"""
    if file_obj is None:
        return {"success": False, "message": "请上传文件"}

    try:
        # 保存上传的文件
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / file_obj.name

        with open(temp_path, "wb") as f:
            f.write(file_obj.read())

        # 加载测试套件
        loader = TestSuiteLoader()
        state.test_suite = loader.load_from_xlsx(str(temp_path))

        # 获取Sheet信息
        sheet_info = loader.get_sheet_info(str(temp_path))

        # 统计信息
        phase_counts = {}
        for tc in state.test_suite.test_cases:
            phase = tc.phase
            phase_counts[phase] = phase_counts.get(phase, 0) + 1

        sheet_summary = "\n".join([
            f"- **{info['name']}** ({info['type']}): {info['rows']}行 x {info['columns']}列"
            for info in sheet_info
        ])

        phase_summary = "\n".join([
            f"- {phase}: {count}个测试用例"
            for phase, count in phase_counts.items()
        ])

        message = f"""✅ **加载成功!**

**Sheet概览:**
{sheet_summary}

**测试用例统计:**
{phase_summary}

**总计:** {len(state.test_suite.test_cases)}个测试用例, {len(state.test_suite.scenarios)}个场景
"""
        return {"success": True, "message": message}

    except Exception as e:
        return {"success": False, "message": f"加载失败: {str(e)}"}


def get_suite_overview() -> gr.Blocks:
    """生成测试套件概览组件。"""
    if state.test_suite is None:
        return gr.Markdown("❌ 请先上传测试套件")

    suite = state.test_suite

    md = f"""
## 📊 测试套件概览

| 属性 | 值 |
|------|-----|
| **名称** | {suite.name} |
| **版本** | {suite.version} |
| **测试用例** | {len(suite.test_cases)} |
| **场景数** | {len(suite.scenarios)} |

### 测试用例列表
"""

    # 按阶段分组
    phase_cases = {}
    for tc in suite.test_cases:
        if tc.phase not in phase_cases:
            phase_cases[tc.phase] = []
        phase_cases[tc.phase].append(tc)

    for phase, cases in phase_cases.items():
        md += f"\n#### {phase} ({len(cases)}个)\n"
        for tc in cases:
            priority_emoji = "🔴" if tc.priority == "P0" else "🟡" if tc.priority == "P1" else "🟢"
            md += f"- {priority_emoji} `{tc.id}`: {tc.description[:60]}...\n"

    return gr.Markdown(md)


def run_evaluation(
    phases: List[str],
    max_samples: int,
    show_details: bool
) -> tuple:
    """执行评测。"""
    if state.test_suite is None:
        return "❌ 请先上传测试套件", None, None, None

    if not phases:
        return "❌ 请至少选择一个阶段", None, None, None

    # 过滤测试用例
    filtered_cases = [
        tc for tc in state.test_suite.test_cases
        if tc.phase in phases
    ][:max_samples]

    if not filtered_cases:
        return "❌ 没有找到匹配的测试用例", None, None, None

    # 执行评测
    results = []
    progress_data = []

    for tc in filtered_cases:
        score_result = simulate_evaluation(tc)

        result = {
            "test_case_id": tc.id,
            "phase": tc.phase,
            "description": tc.description[:50] + "...",
            "passed": state.scoring_engine.is_passed(score_result.score),
            "score": score_result.score,
            "confidence": score_result.confidence,
            "status": "✓ 通过" if score_result.score >= 0.8 else "✗ 失败",
            "details": score_result.metadata
        }
        results.append(result)
        progress_data.append(result)

    state.results = results

    # 计算统计
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0
    avg_score = sum(r["score"] for r in results) / total if total > 0 else 0
    avg_confidence = sum(r["confidence"] for r in results) / total if total > 0 else 0

    # 生成摘要
    summary = f"""## 📈 评测完成

| 指标 | 值 |
|------|-----|
| **总测试数** | {total} |
| **通过** | {passed} ✅ |
| **失败** | {failed} ❌ |
| **通过率** | {pass_rate:.1f}% |
| **平均分数** | {avg_score:.3f} |
| **平均置信度** | {avg_confidence:.3f} |
"""

    # 生成表格数据
    table_data = pd.DataFrame(results)

    # 生成图表
    score_chart = create_score_chart(results)
    pass_rate_chart = create_pass_rate_chart(results)
    confidence_chart = create_confidence_chart(results)

    return (
        summary,
        table_data,
        gr.Plot(value=score_chart),
        gr.Plot(value=pass_rate_chart),
        gr.Plot(value=confidence_chart)
    )


def get_results_table() -> pd.DataFrame:
    """获取结果表格。"""
    if not state.results:
        return pd.DataFrame()
    return pd.DataFrame(state.results)


def export_report(format: str) -> str:
    """导出报告。"""
    if not state.results:
        return "❌ 没有可导出的结果"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_report_{timestamp}.{format.lower()}"

    if format == "JSON":
        report_data = {
            "test_suite": {
                "name": state.test_suite.name if state.test_suite else "N/A",
                "version": state.test_suite.version if state.test_suite else "N/A"
            },
            "results": state.results,
            "summary": {
                "total": len(state.results),
                "passed": sum(1 for r in state.results if r["passed"]),
                "avg_score": sum(r["score"] for r in state.results) / len(state.results)
            },
            "generated_at": timestamp
        }
        content = json.dumps(report_data, indent=2, ensure_ascii=False)

    elif format == "YAML":
        report_data = {
            "test_suite": {
                "name": state.test_suite.name if state.test_suite else "N/A",
                "version": state.test_suite.version if state.test_suite else "N/A"
            },
            "results": state.results,
            "generated_at": timestamp
        }
        content = yaml.dump(report_data, allow_unicode=True)

    elif format == "CSV":
        df = pd.DataFrame(state.results)
        content = df.to_csv(index=False)

    else:
        return "❌ 不支持的格式"

    # 保存文件
    output_path = Path("exports")
    output_path.mkdir(exist_ok=True)
    file_path = output_path / filename

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"✅ 报告已导出: `{filename}`"


def get_config_editor() -> Dict[str, Any]:
    """获取配置编辑器数据。"""
    config = state.scoring_engine.config

    return {
        "pass_threshold": config.pass_threshold,
        "critical_threshold": config.critical_threshold,
        "phase_weights": config.phase_weights,
        "confidence_levels": config.confidence.levels,
        "formulas": {
            name: {
                "type": formula.type,
                "weights": formula.weights,
                "thresholds": formula.thresholds
            }
            for name, formula in config.formulas.items()
        }
    }


# ==================== 界面布局 ====================

def create_app():
    """创建Gradio应用。"""

    # 主题设置
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="green",
        neutral_hue="gray",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"]
    )

    with gr.Blocks(
        theme=theme,
        title="AI Testing Benchmark",
        css="""
        .main-header { text-align: center; padding: 20px; }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; }
        .success-box { background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 8px; }
        .warning-box { background: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 8px; }
        .error-box { background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 8px; }
        """
    ) as app:

        # 页头
        gr.Markdown("""
        # 🧪 AI Testing Benchmark
        ### 配置驱动的AI评测框架
        """, elem_classes="main-header")

        with gr.Tabs():
            # ==================== Tab 1: 上传测试套件 ====================
            with gr.TabItem("📁 上传测试套件"):
                gr.Markdown("### 上传XLSX测试套件文件")

                with gr.Row():
                    with gr.Column(scale=1):
                        file_input = gr.File(
                            label="选择XLSX文件",
                            file_types=[".xlsx", ".xls"],
                            file_count=1
                        )
                        upload_btn = gr.Button("📤 加载测试套件", variant="primary")

                    with gr.Column(scale=2):
                        upload_output = gr.Markdown("❓ 请上传XLSX格式的测试套件文件")

                upload_btn.click(
                    fn=parse_xlsx_file,
                    inputs=[file_input],
                    outputs=[upload_output]
                )

                gr.Markdown("---")
                gr.Markdown("### 📋 Sheet预览")
                sheet_preview = gr.DataFrame(headers=["名称", "类型", "行数", "列数"])

                with gr.Row():
                    suite_overview = gr.Markdown("❌ 请先上传测试套件")

            # ==================== Tab 2: 执行评测 ====================
            with gr.TabItem("⚙️ 执行评测"):
                gr.Markdown("### 配置并执行评测")

                with gr.Row():
                    with gr.Column(scale=1):
                        phase_selector = gr.Dropdown(
                            label="选择阶段",
                            choices=["resource_import", "inventory_confirmation",
                                    "resource_summary", "grouping_architecture",
                                    "cloud_strategy", "spec_recommendation",
                                    "compatibility", "report_generation"],
                            multiselect=True,
                            value=["resource_import", "cloud_strategy"]
                        )

                        max_samples = gr.Slider(
                            label="最大样本数",
                            minimum=1,
                            maximum=500,
                            value=50,
                            step=1
                        )

                        run_btn = gr.Button("🚀 开始评测", variant="primary", size="lg")

                    with gr.Column(scale=2):
                        eval_summary = gr.Markdown("📊 点击\"开始评测\"按钮执行测试")

                gr.Markdown("### 📈 可视化结果")
                with gr.Row():
                    score_chart = gr.Plot(label="分数分析")
                    pass_rate_chart = gr.Plot(label="通过率分析")

                confidence_chart = gr.Plot(label="置信度分析")

            # ==================== Tab 3: 结果详情 ====================
            with gr.TabItem("🔍 结果详情"):
                gr.Markdown("### 评测结果详情")

                results_table = gr.DataFrame(
                    label="测试结果",
                    wrap=True,
                    column_width="auto"
                )

                refresh_btn = gr.Button("🔄 刷新结果")

                refresh_btn.click(
                    fn=get_results_table,
                    outputs=[results_table]
                )

            # ==================== Tab 4: 报告导出 ====================
            with gr.TabItem("📤 导出报告"):
                gr.Markdown("### 导出评测报告")

                with gr.Row():
                    export_format = gr.Radio(
                        choices=["JSON", "YAML", "CSV"],
                        value="JSON",
                        label="导出格式"
                    )
                    export_btn = gr.Button("📥 导出报告", variant="primary")

                export_output = gr.Textbox(label="导出结果", lines=3)

                export_btn.click(
                    fn=export_report,
                    inputs=[export_format],
                    outputs=[export_output]
                )

            # ==================== Tab 5: 配置管理 ====================
            with gr.TabItem("⚙️ 配置管理"):
                gr.Markdown("### 评分配置管理")

                gr.Markdown("#### 当前配置")

                config_json = gr.JSON(label="评分配置")

                gr.Markdown("""
                ### 配置说明

                所有评分配置均可通过YAML文件管理：

                ```yaml
                formulas:
                  accuracy:
                    type: accuracy
                    thresholds:
                      pass: 0.80
                      warning: 0.70

                confidence:
                  levels:
                    high: 0.90
                    medium: 0.70
                    low: 0.50

                phase_weights:
                  foundation: 0.20
                  dialogue: 0.20
                  migration: 0.25
                ```

                **支持的配置项:**
                - `formulas`: 评分公式及其权重
                - `confidence`: 置信度等级和计算方法
                - `phase_weights`: 各阶段权重
                - `pass_threshold`: 通过阈值
                - `critical_threshold`: 危险阈值
                """)

                config_json.change(
                    fn=get_config_editor,
                    outputs=[config_json]
                )

            # ==================== Tab 6: 使用帮助 ====================
            with gr.TabItem("❓ 帮助"):
                gr.Markdown("""
                # 使用指南

                ## 1. 上传测试套件
                - 点击"选择文件"上传XLSX格式的测试套件
                - 支持多Sheet的Excel文件
                - Sheet类型: `test_cases`, `scenarios`, `config`

                ## 2. 执行评测
                - 选择要评测的阶段
                - 设置最大样本数
                - 点击"开始评测"

                ## 3. 查看结果
                - 查看分数分布和通过率图表
                - 查看详细的测试结果表格
                - 支持筛选和排序

                ## 4. 导出报告
                - 支持JSON/YAML/CSV格式
                - 包含完整的评测结果和统计

                ## XLSX模板格式

                ### test_cases Sheet (必需)
                | 字段 | 说明 | 必需 |
                |------|------|------|
                | id | 测试用例ID | ✓ |
                | scenario_id | 场景ID | ✓ |
                | phase | 阶段名称 | ✓ |
                | description | 描述 | ✓ |
                | input | 输入数据(JSON) | |
                | expected_output | 期望输出(JSON) | |
                | priority | 优先级(P0/P1/P2) | |
                | tags | 标签(逗号分隔) | |

                ### scenarios Sheet
                | 字段 | 说明 |
                |------|------|
                | id | 场景ID |
                | name | 场景名称 |
                | description | 描述 |
                | test_case_ids | 关联的测试用例ID(逗号分隔) |
                """)

        # 页脚
        gr.Markdown("""
        ---
        **AI Testing Benchmark v2.0** | 基于配置驱动的AI评测框架
        """)

    return app


# ==================== 启动应用 ====================

if __name__ == "__main__":
    # 初始化评分引擎
    state.scoring_engine = ScoringEngine()

    # 创建并启动应用
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

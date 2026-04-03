"""
AI Testing Benchmark - Web界面

基于Streamlit的图形化评测界面。
"""

import streamlit as st
import pandas as pd
import json
import yaml
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# 添加项目路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_testing_benchmark.core.test_suite_loader import (
    TestSuiteLoader,
    load_test_suite,
    LoadedTestSuite,
    SheetType
)
from ai_testing_benchmark.core.scoring_engine import (
    ScoringEngine,
    ScoreResult,
    ConfidenceLevel
)
from ai_testing_benchmark.core.config import BenchmarkConfig, ConfigLoader

# 页面配置
st.set_page_config(
    page_title="AI Testing Benchmark",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .pass { color: #27ae60; }
    .fail { color: #e74c3c; }
    .warning { color: #f39c12; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)


# 会话状态初始化
def init_session_state():
    """初始化会话状态。"""
    if "test_suite" not in st.session_state:
        st.session_state.test_suite = None
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "config" not in st.session_state:
        st.session_state.config = None
    if "scoring_engine" not in st.session_state:
        st.session_state.scoring_engine = None


init_session_state()


# 侧边栏
def render_sidebar():
    """渲染侧边栏。"""
    with st.sidebar:
        st.title("🧪 配置")

        # 模型配置
        st.subheader("模型设置")
        model_name = st.selectbox(
            "模型",
            ["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet", "custom"],
            index=0
        )
        provider = st.selectbox(
            "提供商",
            ["openai", "anthropic", "azure", "custom"],
            index=0
        )

        # 评分配置
        st.subheader("评分设置")
        scoring_config_path = st.text_input(
            "评分配置文件",
            placeholder="可选，YAML/JSON格式"
        )

        if scoring_config_path and Path(scoring_config_path).exists():
            st.session_state.scoring_engine = ScoringEngine(scoring_config_path)
            st.success("✓ 评分配置已加载")
        else:
            st.session_state.scoring_engine = ScoringEngine()
            st.info("使用默认评分配置")

        # 阈值设置
        st.subheader("阈值设置")
        pass_threshold = st.slider(
            "通过阈值",
            0.0, 1.0,
            st.session_state.scoring_engine.config.pass_threshold,
            0.05
        )
        critical_threshold = st.slider(
            "危险阈值",
            0.0, 1.0,
            st.session_state.scoring_engine.config.critical_threshold,
            0.05
        )

        # 高级选项
        with st.expander("高级选项"):
            early_stopping = st.checkbox("首次失败停止", value=False)
            include_raw = st.checkbox("包含原始输出", value=True)
            verbose = st.checkbox("详细日志", value=False)

        st.divider()

        # 关于
        st.caption("AI Testing Benchmark v2.0")
        st.caption("基于配置驱动的AI评测框架")


def render_upload_section():
    """渲染文件上传区域。"""
    st.subheader("📁 上传测试套件")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "选择XLSX文件",
            type=["xlsx", "xls"],
            help="支持多Sheet的XLSX格式测试套件"
        )

    with col2:
        st.write("　")
        if uploaded_file is not None:
            st.success(f"已上传: {uploaded_file.name}")

    if uploaded_file is not None:
        # 保存上传的文件
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / uploaded_file.name

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 加载并显示Sheet信息
        loader = TestSuiteLoader()
        try:
            sheet_info = loader.get_sheet_info(str(temp_path))

            st.write("**检测到的Sheet:**")
            for info in sheet_info:
                with st.expander(f"📋 {info['name']} ({info['type']})"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("行数", info["rows"])
                    col2.metric("列数", info["columns"])
                    col3.metric("类型", info["type"])

                    if info["headers"]:
                        st.write("**表头:**")
                        st.write(", ".join(str(h) for h in info["headers"] if h))

            # 加载测试套件
            if st.button("加载测试套件", type="primary"):
                with st.spinner("正在加载..."):
                    suite = loader.load_from_xlsx(str(temp_path))
                    st.session_state.test_suite = suite

                    st.success(f"✓ 加载成功!")
                    st.info(f"包含 {len(suite.test_cases)} 个测试用例, {len(suite.scenarios)} 个场景")

        except Exception as e:
            st.error(f"加载失败: {str(e)}")


def render_test_suite_overview():
    """渲染测试套件概览。"""
    if st.session_state.test_suite is None:
        st.info("请先上传测试套件")
        return

    suite = st.session_state.test_suite

    st.subheader("📊 测试套件概览")

    # 基本信息
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("名称", suite.name)
    col2.metric("版本", suite.version)
    col3.metric("测试用例", len(suite.test_cases))
    col4.metric("场景", len(suite.scenarios))

    # 测试用例预览
    st.subheader("📝 测试用例预览")

    # 按阶段分组统计
    phase_counts = {}
    for tc in suite.test_cases:
        phase = tc.phase
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    if phase_counts:
        col1, col2 = st.columns([1, 1])

        with col1:
            fig = px.pie(
                values=list(phase_counts.values()),
                names=list(phase_counts.keys()),
                title="测试用例分布(按阶段)"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            df = pd.DataFrame({
                "阶段": list(phase_counts.keys()),
                "数量": list(phase_counts.values())
            })
            fig = px.bar(
                df,
                x="阶段",
                y="数量",
                title="测试用例数量(按阶段)"
            )
            st.plotly_chart(fig, use_container_width=True)

    # 测试用例列表
    with st.expander("查看测试用例列表"):
        df_cases = pd.DataFrame([
            {
                "ID": tc.id,
                "场景": tc.scenario_id,
                "阶段": tc.phase,
                "描述": tc.description[:50] + "..." if len(tc.description) > 50 else tc.description,
                "优先级": tc.priority,
                "标签": ", ".join(tc.tags)
            }
            for tc in suite.test_cases
        ])
        st.dataframe(df_cases, use_container_width=True, hide_index=True)


def render_test_execution():
    """渲染测试执行区域。"""
    if st.session_state.test_suite is None:
        st.info("请先上传测试套件")
        return

    st.subheader("⚙️ 执行评测")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_phases = st.multiselect(
            "选择阶段",
            list(set(tc.phase for tc in st.session_state.test_suite.test_cases)),
            default=list(set(tc.phase for tc in st.session_state.test_suite.test_cases))
        )

    with col2:
        max_samples = st.number_input("最大样本数", 1, 1000, 100)

    with col3:
        show_details = st.checkbox("显示详情", value=True)

    if st.button("开始评测", type="primary"):
        if not selected_phases:
            st.warning("请至少选择一个阶段")
            return

        # 过滤测试用例
        filtered_cases = [
            tc for tc in st.session_state.test_suite.test_cases
            if tc.phase in selected_phases
        ][:max_samples]

        st.info(f"将执行 {len(filtered_cases)} 个测试用例")

        # 执行评测
        progress_bar = st.progress(0)
        results = []

        for i, tc in enumerate(filtered_cases):
            # 模拟评测过程
            # 实际使用时这里会调用真实的AI模型进行评测
            score_result = simulate_evaluation(tc)

            results.append({
                "test_case_id": tc.id,
                "phase": tc.phase,
                "passed": st.session_state.scoring_engine.is_passed(score_result.score),
                "score": score_result.score,
                "confidence": score_result.confidence,
                "details": score_result.metadata
            })

            progress_bar.progress((i + 1) / len(filtered_cases))

        # 保存结果
        st.session_state.results = results

        st.success(f"✓ 评测完成! 处理了 {len(results)} 个测试用例")

        # 显示结果统计
        render_results_summary(results)


def simulate_evaluation(tc) -> ScoreResult:
    """
    模拟评测过程。

    实际使用时替换为真实的AI模型调用。
    """
    import random

    # 模拟分数
    base_score = random.uniform(0.6, 0.95)
    confidence = random.uniform(0.7, 0.95)

    return ScoreResult(
        score=base_score,
        confidence=confidence,
        confidence_level=ConfidenceLevel.HIGH if confidence >= 0.9 else ConfidenceLevel.MEDIUM,
        components={},
        metadata={"simulated": True}
    )


def render_results_summary(results: list):
    """渲染结果汇总。"""
    st.subheader("📈 评测结果汇总")

    # 计算统计
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0

    avg_score = sum(r["score"] for r in results) / total if total > 0 else 0
    avg_confidence = sum(r["confidence"] for r in results) / total if total > 0 else 0

    # 显示指标卡片
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("总测试数", total)
    with col2:
        st.metric("通过", passed, delta=f"+{passed}")
    with col3:
        st.metric("失败", failed, delta=f"-{failed}")
    with col4:
        st.metric("通过率", f"{pass_rate:.1f}%",
                  delta="✓" if pass_rate >= 80 else "✗")
    with col5:
        st.metric("平均分数", f"{avg_score:.2f}")

    # 按阶段分析
    phase_results = {}
    for r in results:
        phase = r["phase"]
        if phase not in phase_results:
            phase_results[phase] = {"total": 0, "passed": 0, "scores": []}
        phase_results[phase]["total"] += 1
        phase_results[phase]["passed"] += 1 if r["passed"] else 0
        phase_results[phase]["scores"].append(r["score"])

    # 阶段结果表格
    st.write("**按阶段结果:**")
    phase_data = []
    for phase, data in phase_results.items():
        phase_pass_rate = (data["passed"] / data["total"] * 100) if data["total"] > 0 else 0
        phase_avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0

        phase_data.append({
            "阶段": phase,
            "总数": data["total"],
            "通过": data["passed"],
            "失败": data["total"] - data["passed"],
            "通过率": f"{phase_pass_rate:.1f}%",
            "平均分": f"{phase_avg_score:.3f}",
            "状态": "✓ 通过" if phase_pass_rate >= 80 else "✗ 未通过"
        })

    df_phase = pd.DataFrame(phase_data)
    st.dataframe(df_phase, use_container_width=True, hide_index=True)

    # 可视化
    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df_phase,
            x="阶段",
            y="平均分",
            color="状态",
            title="各阶段平均分数",
            color_discrete_map={"✓ 通过": "#27ae60", "✗ 未通过": "#e74c3c"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(phase_results.keys()),
            y=[sum(p["scores"]) / len(p["scores"]) for p in phase_results.values()],
            mode="lines+markers",
            name="平均分"
        ))
        fig.add_trace(go.Scatter(
            x=list(phase_results.keys()),
            y=[p["passed"] / p["total"] * 100 if p["total"] > 0 else 0 for p in phase_results.values()],
            mode="lines+markers",
            name="通过率%"
        ))
        fig.update_layout(title="分数与通过率趋势", xaxis_title="阶段")
        st.plotly_chart(fig, use_container_width=True)


def render_configuration_editor():
    """渲染配置编辑器。"""
    st.subheader("⚙️ 评分配置管理")

    tabs = st.tabs(["查看配置", "编辑配置", "保存/加载"])

    with tabs[0]:
        if st.session_state.scoring_engine:
            config = st.session_state.scoring_engine.config

            st.write("**通过阈值:**")
            st.json({"pass_threshold": config.pass_threshold,
                     "critical_threshold": config.critical_threshold})

            st.write("**阶段权重:**")
            st.json(config.phase_weights)

            st.write("**置信度配置:**")
            st.json({
                "levels": config.confidence.levels,
                "calculation_method": config.confidence.calculation_method
            })

            st.write("**评分公式:**")
            for name, formula in config.formulas.items():
                with st.expander(f"公式: {name}"):
                    st.json({
                        "type": formula.type,
                        "weights": formula.weights,
                        "thresholds": formula.thresholds,
                        "aggregation": formula.aggregation.value
                    })

    with tabs[1]:
        st.write("**编辑评分公式权重:**")

        formula_name = st.selectbox(
            "选择公式",
            list(st.session_state.scoring_engine.config.formulas.keys())
        )

        if formula_name:
            formula = st.session_state.scoring_engine.config.formulas[formula_name]

            st.write(f"**类型:** {formula.type}")

            st.write("**权重:**")
            new_weights = {}
            for key, value in formula.weights.items():
                new_weights[key] = st.slider(
                    f"权重 - {key}",
                    0.0, 1.0, value, 0.1
                )

            st.write("**阈值:**")
            new_pass_threshold = st.slider(
                "Pass阈值",
                0.0, 1.0, formula.thresholds.get("pass", 0.8), 0.05
            )

            if st.button("应用更改"):
                formula.weights = new_weights
                formula.thresholds["pass"] = new_pass_threshold
                st.success("✓ 配置已更新")

    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            st.write("**保存配置:**")
            save_path = st.text_input("保存路径", "scoring_config.yaml")
            if st.button("保存"):
                st.session_state.scoring_engine.save_config(save_path)
                st.success(f"✓ 配置已保存至: {save_path}")

        with col2:
            st.write("**加载配置:**")
            load_path = st.text_input("加载路径")
            if st.button("加载") and load_path:
                st.session_state.scoring_engine = ScoringEngine(load_path)
                st.success("✓ 配置已加载")


def render_results_detail():
    """渲染详细结果。"""
    if not st.session_state.results:
        st.info("暂无评测结果")
        return

    st.subheader("🔍 详细结果")

    results = st.session_state.results

    # 筛选器
    col1, col2, col3 = st.columns(3)

    with col1:
        filter_status = st.multiselect(
            "状态筛选",
            ["通过", "失败"],
            default=["通过", "失败"]
        )

    with col2:
        filter_phase = st.multiselect(
            "阶段筛选",
            list(set(r["phase"] for r in results)),
            default=list(set(r["phase"] for r in results))
        )

    with col3:
        sort_by = st.selectbox(
            "排序",
            ["分数(升序)", "分数(降序)", "阶段"]
        )

    # 筛选结果
    filtered = [
        r for r in results
        if ("通过" in filter_status if r["passed"] else "失败" in filter_status)
        and r["phase"] in filter_phase
    ]

    # 排序
    if sort_by == "分数(升序)":
        filtered.sort(key=lambda x: x["score"])
    elif sort_by == "分数(降序)":
        filtered.sort(key=lambda x: x["score"], reverse=True)
    else:
        filtered.sort(key=lambda x: x["phase"])

    # 显示列表
    for r in filtered:
        phase = r["phase"]
        status = "✓" if r["passed"] else "✗"
        status_color = "green" if r["passed"] else "red"

        with st.expander(f"`{status}` {r['test_case_id']} | {phase} | 分数: {r['score']:.3f}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("分数", f"{r['score']:.3f}")
            col2.metric("置信度", f"{r['confidence']:.3f}")
            col3.metric("状态", "通过" if r["passed"] else "失败")

            if r.get("details"):
                st.json(r["details"])


def render_export():
    """渲染导出功能。"""
    st.subheader("📤 导出报告")

    if not st.session_state.results and not st.session_state.test_suite:
        st.info("暂无数据可导出")
        return

    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox(
            "导出格式",
            ["JSON", "YAML", "CSV", "HTML"]
        )

    with col2:
        include_details = st.checkbox("包含详情", value=True)

    if st.button("生成报告"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if export_format == "JSON":
            report_data = {
                "test_suite": {
                    "name": st.session_state.test_suite.name if st.session_state.test_suite else "N/A",
                    "version": st.session_state.test_suite.version if st.session_state.test_suite else "N/A",
                    "test_case_count": len(st.session_state.test_suite.test_cases) if st.session_state.test_suite else 0
                },
                "results": st.session_state.results,
                "generated_at": timestamp
            }
            report_str = json.dumps(report_data, indent=2, ensure_ascii=False)
            filename = f"benchmark_report_{timestamp}.json"

        elif export_format == "YAML":
            report_data = {
                "test_suite": {
                    "name": st.session_state.test_suite.name if st.session_state.test_suite else "N/A",
                    "version": st.session_state.test_suite.version if st.session_state.test_suite else "N/A"
                },
                "results": st.session_state.results,
                "generated_at": timestamp
            }
            report_str = yaml.dump(report_data, allow_unicode=True)
            filename = f"benchmark_report_{timestamp}.yaml"

        elif export_format == "CSV":
            if st.session_state.results:
                df = pd.DataFrame(st.session_state.results)
                report_str = df.to_csv(index=False)
            else:
                report_str = ""
            filename = f"benchmark_report_{timestamp}.csv"

        else:  # HTML
            report_str = generate_html_report()
            filename = f"benchmark_report_{timestamp}.html"

        if report_str:
            st.download_button(
                label=f"下载 {export_format} 报告",
                data=report_str,
                file_name=filename,
                mime=get_mime_type(export_format)
            )


def generate_html_report() -> str:
    """生成HTML报告。"""
    results = st.session_state.results
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pass_rate = (passed / total * 100) if total > 0 else 0

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Testing Benchmark Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }}
            .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #ecf0f1; border-radius: 8px; }}
            .pass {{ color: #27ae60; }}
            .fail {{ color: #e74c3c; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #2c3e50; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>AI Testing Benchmark Report</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="metrics">
            <div class="metric">
                <h3>总测试数</h3>
                <p>{total}</p>
            </div>
            <div class="metric">
                <h3>通过</h3>
                <p class="pass">{passed}</p>
            </div>
            <div class="metric">
                <h3>失败</h3>
                <p class="fail">{total - passed}</p>
            </div>
            <div class="metric">
                <h3>通过率</h3>
                <p class="{'pass' if pass_rate >= 80 else 'fail'}">{pass_rate:.1f}%</p>
            </div>
        </div>

        <h2>详细结果</h2>
        <table>
            <tr>
                <th>测试用例ID</th>
                <th>阶段</th>
                <th>分数</th>
                <th>置信度</th>
                <th>状态</th>
            </tr>
    """

    for r in results:
        status = "通过" if r["passed"] else "失败"
        status_class = "pass" if r["passed"] else "fail"
        html += f"""
            <tr>
                <td>{r['test_case_id']}</td>
                <td>{r['phase']}</td>
                <td>{r['score']:.3f}</td>
                <td>{r['confidence']:.3f}</td>
                <td class="{status_class}">{status}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


def get_mime_type(format: str) -> str:
    """获取MIME类型。"""
    mime_types = {
        "JSON": "application/json",
        "YAML": "application/x-yaml",
        "CSV": "text/csv",
        "HTML": "text/html"
    }
    return mime_types.get(format, "text/plain")


def main():
    """主函数。"""
    st.markdown('<p class="main-header">🧪 AI Testing Benchmark</p>', unsafe_allow_html=True)
    st.markdown("配置驱动的AI评测框架 - 支持XLSX多Sheet导入")

    render_sidebar()

    # 主内容区
    tabs = st.tabs([
        "📁 上传测试套件",
        "📊 测试套件概览",
        "⚙️ 执行评测",
        "🔍 结果详情",
        "⚙️ 配置管理",
        "📤 导出报告"
    ])

    with tabs[0]:
        render_upload_section()

    with tabs[1]:
        render_test_suite_overview()

    with tabs[2]:
        render_test_execution()

    with tabs[3]:
        render_results_detail()

    with tabs[4]:
        render_configuration_editor()

    with tabs[5]:
        render_export()


if __name__ == "__main__":
    main()

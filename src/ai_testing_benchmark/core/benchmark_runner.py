"""
基准测试运行器 - 协调所有评估阶段。
"""

from typing import Dict, List, Any, Optional
import loguru
from datetime import datetime
import json
from pathlib import Path

from ai_testing_benchmark.core.config import BenchmarkConfig, ConfigLoader
from ai_testing_benchmark.core.result import (
    EvaluationResult,
    PhaseResult,
    BenchmarkReport,
    ResultStatus
)

from ai_testing_benchmark.evaluation import FoundationModelEvaluator
from ai_testing_benchmark.dialogue import DialogueEvaluator
from ai_testing_benchmark.migration import CloudMigrationEvaluator
from ai_testing_benchmark.safety import SafetyEvaluator
from ai_testing_benchmark.performance import PerformanceEvaluator


class BenchmarkRunner:
    """
    运行综合AI基准测试的主要协调器。

    运行器管理所有评估阶段、聚合结果并生成综合报告。
    """

    def __init__(
        self,
        config: Optional[BenchmarkConfig] = None,
        config_path: Optional[str] = None,
        verbose: bool = False
    ):
        """
        初始化基准测试运行器。

        参数:
            config: 可选的BenchmarkConfig对象
            config_path: 可选的配置文件路径
            verbose: 启用详细日志
        """
        self.logger = loguru.logger

        if verbose:
            self.logger.enable("ai_testing_benchmark")
        else:
            self.logger.disable("ai_testing_benchmark")

        # 加载配置
        if config:
            self.config = config
        elif config_path:
            self.config = ConfigLoader.load(config_path)
        else:
            self.config = ConfigLoader.load()

        # 初始化阶段评估器
        self.evaluators: Dict[str, Any] = {}

        self._initialize_evaluators()

        # 结果存储
        self.report: Optional[BenchmarkReport] = None

    def _initialize_evaluators(self) -> None:
        """根据配置初始化所有阶段评估器。"""
        self.logger.info("正在初始化阶段评估器")

        # 基础模型评估器
        if self.config.is_phase_enabled("foundation"):
            self.evaluators["foundation"] = FoundationModelEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.foundation.custom_config,
                verbose=self.logger._core.enabled
            )

        # 对话评估器
        if self.config.is_phase_enabled("dialogue"):
            self.evaluators["dialogue"] = DialogueEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.dialogue.custom_config,
                verbose=self.logger._core.enabled
            )

        # 云迁移评估器
        if self.config.is_phase_enabled("migration"):
            self.evaluators["migration"] = CloudMigrationEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.migration.custom_config,
                verbose=self.logger._core.enabled
            )

        # 安全评估器
        if self.config.is_phase_enabled("safety"):
            self.evaluators["safety"] = SafetyEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.safety.custom_config,
                verbose=self.logger._core.enabled
            )

        # 性能评估器
        if self.config.is_phase_enabled("performance"):
            self.evaluators["performance"] = PerformanceEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.performance.custom_config,
                verbose=self.logger._core.enabled
            )

        self.logger.info(f"已初始化 {len(self.evaluators)} 个评估器")

    def run_full_benchmark(
        self,
        phases: Optional[List[str]] = None,
        stop_on_first_failure: bool = False
    ) -> BenchmarkReport:
        """
        在所有或指定阶段上运行完整基准测试。

        参数:
            phases: 要运行的阶段列表。如果为None，运行所有已启用的阶段。
            stop_on_first_failure: 如果任何关键测试失败则停止

        返回:
            包含所有结果的BenchmarkReport
        """
        self.logger.info("开始执行完整基准测试")
        start_time = datetime.now()

        if phases is None:
            phases = list(self.evaluators.keys())

        report = BenchmarkReport(
            model_name=self.config.model.name,
            model_provider=self.config.model.provider,
            config=self.config.model_dump()
        )

        for phase in phases:
            if phase not in self.evaluators:
                self.logger.warning(f"阶段 {phase} 不可用，跳过")
                continue

            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"正在运行阶段: {phase.upper()}")
            self.logger.info(f"{'='*60}")

            phase_start = datetime.now()

            try:
                phase_result = self.evaluators[phase].run_phase()
                report.phases[phase] = phase_result

            except Exception as e:
                self.logger.error(f"运行阶段 {phase} 时出错: {str(e)}")
                phase_result = PhaseResult(phase=phase)
                phase_result.status = ResultStatus.ERROR
                report.phases[phase] = phase_result

            phase_duration = (datetime.now() - phase_start).total_seconds() * 1000
            self.logger.info(f"阶段 {phase} 完成，耗时 {phase_duration:.2f}ms")
            self.logger.info(f"阶段分数: {phase_result.overall_score:.2f}")

            # 检查关键失败
            if phase_result.issues_by_severity.get("CRITICAL", 0) > 0:
                self.logger.error(f"在阶段 {phase} 中发现严重问题")

                if stop_on_first_failure:
                    self.logger.error("因严重失败而停止基准测试")
                    break

        # 计算总体分数
        report.calculate_overall_score()

        # 检查质量门禁
        report.check_quality_gates(self.config.quality_gates)

        # 计算汇总统计
        for phase_result in report.phases.values():
            report.total_tests += phase_result.total_tests
            report.total_passed += phase_result.passed_tests
            report.total_failed += phase_result.failed_tests
            report.critical_issues += phase_result.issues_by_severity.get("CRITICAL", 0)
            report.high_issues += phase_result.issues_by_severity.get("HIGH", 0)

        total_duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"基准测试完成，耗时 {total_duration:.2f}ms")
        self.logger.info(f"总体分数: {report.overall_score:.2f}")
        self.logger.info(f"质量门禁: {'通过' if report.quality_gate_passed else '未通过'}")
        self.logger.info(f"{'='*60}")

        self.report = report
        return report

    def run_phase(self, phase: str, test_cases: Optional[List[Dict]] = None) -> PhaseResult:
        """
        运行特定阶段。

        参数:
            phase: 阶段名称
            test_cases: 可选的特定测试用例

        返回:
            该阶段的PhaseResult
        """
        if phase not in self.evaluators:
            raise ValueError(f"未知阶段: {phase}")

        evaluator = self.evaluators[phase]

        if test_cases:
            return evaluator.run_evaluation(test_cases)
        else:
            return evaluator.run_phase()

    def generate_report(
        self,
        output_format: str = "json",
        output_path: Optional[str] = None,
        include_raw: bool = False
    ) -> str:
        """
        生成基准测试报告。

        参数:
            output_format: 输出格式 ('json' 或 'html')
            output_path: 保存报告的可选路径
            include_raw: 包含原始模型输出

        返回:
            字符串格式的报告
        """
        if not self.report:
            raise ValueError("没有可用的报告。请先运行基准测试。")

        if output_format == "json":
            report_str = json.dumps(
                self.report.to_dict(include_raw=include_raw),
                indent=2,
                default=str
            )
        elif output_format == "html":
            report_str = self._generate_html_report()
        else:
            raise ValueError(f"未知输出格式: {output_format}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report_str)
            self.logger.info(f"报告已保存至 {output_path}")

        return report_str

    def _generate_html_report(self) -> str:
        """生成HTML报告。"""
        if not self.report:
            return "<p>没有可用的报告</p>"

        phases_html = []
        for phase_name, phase_result in self.report.phases.items():
            status_color = "green" if phase_result.passed else "red"

            phases_html.append(f"""
            <div class="phase" style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #{status_color};">
                    {phase_name.upper()} - 分数: {phase_result.overall_score:.2f}
                    <span style="font-size: 14px;">({phase_result.passed_tests}/{phase_result.total_tests} 通过)</span>
                </h2>
                <p>通过率: {phase_result.pass_rate:.1f}%</p>
            </div>
            """)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI测试基准报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }}
                .overall-score {{ font-size: 48px; font-weight: bold; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>AI测试基准报告</h1>
                <p>模型: {self.report.model_name}</p>
                <p>提供商: {self.report.model_provider}</p>
                <p class="overall-score {'passed' if self.report.quality_gate_passed else 'failed'}">
                    总体分数: {self.report.overall_score:.2f}
                </p>
                <p>质量门禁: {'通过' if self.report.quality_gate_passed else '未通过'}</p>
            </div>
            <div class="phases">
                {''.join(phases_html)}
            </div>
        </body>
        </html>
        """

    def save_config(self, path: str) -> None:
        """保存当前配置到文件。"""
        self.config.to_yaml(path)
        self.logger.info(f"配置已保存至 {path}")

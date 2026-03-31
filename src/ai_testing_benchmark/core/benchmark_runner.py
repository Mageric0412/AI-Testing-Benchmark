"""
Benchmark runner - orchestrates all evaluation phases.
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
    Main orchestrator for running comprehensive AI benchmarks.

    The runner manages all evaluation phases, aggregates results,
    and generates comprehensive reports.
    """

    def __init__(
        self,
        config: Optional[BenchmarkConfig] = None,
        config_path: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize benchmark runner.

        Args:
            config: Optional BenchmarkConfig object
            config_path: Optional path to config file
            verbose: Enable verbose logging
        """
        self.logger = loguru.logger

        if verbose:
            self.logger.enable("ai_testing_benchmark")
        else:
            self.logger.disable("ai_testing_benchmark")

        # Load configuration
        if config:
            self.config = config
        elif config_path:
            self.config = ConfigLoader.load(config_path)
        else:
            self.config = ConfigLoader.load()

        # Initialize phase evaluators
        self.evaluators: Dict[str, Any] = {}

        self._initialize_evaluators()

        # Results storage
        self.report: Optional[BenchmarkReport] = None

    def _initialize_evaluators(self) -> None:
        """Initialize all phase evaluators based on configuration."""
        self.logger.info("Initializing phase evaluators")

        # Foundation Model Evaluator
        if self.config.is_phase_enabled("foundation"):
            self.evaluators["foundation"] = FoundationModelEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.foundation.custom_config,
                verbose=self.logger._core.enabled
            )

        # Dialogue Evaluator
        if self.config.is_phase_enabled("dialogue"):
            self.evaluators["dialogue"] = DialogueEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.dialogue.custom_config,
                verbose=self.logger._core.enabled
            )

        # Cloud Migration Evaluator
        if self.config.is_phase_enabled("migration"):
            self.evaluators["migration"] = CloudMigrationEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.migration.custom_config,
                verbose=self.logger._core.enabled
            )

        # Safety Evaluator
        if self.config.is_phase_enabled("safety"):
            self.evaluators["safety"] = SafetyEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.safety.custom_config,
                verbose=self.logger._core.enabled
            )

        # Performance Evaluator
        if self.config.is_phase_enabled("performance"):
            self.evaluators["performance"] = PerformanceEvaluator(
                model_name=self.config.model.name,
                provider=self.config.model.provider,
                config=self.config.performance.custom_config,
                verbose=self.logger._core.enabled
            )

        self.logger.info(f"Initialized {len(self.evaluators)} evaluators")

    def run_full_benchmark(
        self,
        phases: Optional[List[str]] = None,
        stop_on_first_failure: bool = False
    ) -> BenchmarkReport:
        """
        Run the complete benchmark across all (or specified) phases.

        Args:
            phases: Optional list of phases to run. If None, runs all enabled phases.
            stop_on_first_failure: Stop if any critical test fails

        Returns:
            BenchmarkReport with all results
        """
        self.logger.info("Starting full benchmark execution")
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
                self.logger.warning(f"Phase {phase} not available, skipping")
                continue

            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Running Phase: {phase.upper()}")
            self.logger.info(f"{'='*60}")

            phase_start = datetime.now()

            try:
                phase_result = self.evaluators[phase].run_phase()
                report.phases[phase] = phase_result

            except Exception as e:
                self.logger.error(f"Error running phase {phase}: {str(e)}")
                phase_result = PhaseResult(phase=phase)
                phase_result.status = ResultStatus.ERROR
                report.phases[phase] = phase_result

            phase_duration = (datetime.now() - phase_start).total_seconds() * 1000
            self.logger.info(f"Phase {phase} completed in {phase_duration:.2f}ms")
            self.logger.info(f"Phase score: {phase_result.overall_score:.2f}")

            # Check for critical failures
            if phase_result.issues_by_severity.get("CRITICAL", 0) > 0:
                self.logger.error(f"Critical issues found in phase {phase}")

                if stop_on_first_failure:
                    self.logger.error("Stopping benchmark due to critical failure")
                    break

        # Calculate overall score
        report.calculate_overall_score()

        # Check quality gates
        report.check_quality_gates(self.config.quality_gates)

        # Calculate summary statistics
        for phase_result in report.phases.values():
            report.total_tests += phase_result.total_tests
            report.total_passed += phase_result.passed_tests
            report.total_failed += phase_result.failed_tests
            report.critical_issues += phase_result.issues_by_severity.get("CRITICAL", 0)
            report.high_issues += phase_result.issues_by_severity.get("HIGH", 0)

        total_duration = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Benchmark completed in {total_duration:.2f}ms")
        self.logger.info(f"Overall Score: {report.overall_score:.2f}")
        self.logger.info(f"Quality Gates: {'PASSED' if report.quality_gate_passed else 'FAILED'}")
        self.logger.info(f"{'='*60}")

        self.report = report
        return report

    def run_phase(self, phase: str, test_cases: Optional[List[Dict]] = None) -> PhaseResult:
        """
        Run a specific phase.

        Args:
            phase: Phase name
            test_cases: Optional specific test cases to run

        Returns:
            PhaseResult for the specified phase
        """
        if phase not in self.evaluators:
            raise ValueError(f"Unknown phase: {phase}")

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
        Generate benchmark report.

        Args:
            output_format: Format for output (json, html)
            output_path: Optional path to save report
            include_raw: Include raw model outputs

        Returns:
            Report as string
        """
        if not self.report:
            raise ValueError("No report available. Run benchmark first.")

        if output_format == "json":
            report_str = json.dumps(
                self.report.to_dict(include_raw=include_raw),
                indent=2,
                default=str
            )
        elif output_format == "html":
            report_str = self._generate_html_report()
        else:
            raise ValueError(f"Unknown output format: {output_format}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report_str)
            self.logger.info(f"Report saved to {output_path}")

        return report_str

    def _generate_html_report(self) -> str:
        """Generate HTML report."""
        if not self.report:
            return "<p>No report available</p>"

        phases_html = []
        for phase_name, phase_result in self.report.phases.items():
            status_color = "green" if phase_result.passed else "red"

            phases_html.append(f"""
            <div class="phase" style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #{status_color};">
                    {phase_name.upper()} - Score: {phase_result.overall_score:.2f}
                    <span style="font-size: 14px;">({phase_result.passed_tests}/{phase_result.total_tests} passed)</span>
                </h2>
                <p>Pass Rate: {phase_result.pass_rate:.1f}%</p>
            </div>
            """)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Testing Benchmark Report</title>
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
                <h1>AI Testing Benchmark Report</h1>
                <p>Model: {self.report.model_name}</p>
                <p>Provider: {self.report.model_provider}</p>
                <p class="overall-score {'passed' if self.report.quality_gate_passed else 'failed'}">
                    Overall Score: {self.report.overall_score:.2f}
                </p>
                <p>Quality Gates: {'PASSED' if self.report.quality_gate_passed else 'FAILED'}</p>
            </div>
            <div class="phases">
                {''.join(phases_html)}
            </div>
        </body>
        </html>
        """

    def save_config(self, path: str) -> None:
        """Save current configuration to file."""
        self.config.to_yaml(path)
        self.logger.info(f"Configuration saved to {path}")

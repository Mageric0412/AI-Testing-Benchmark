"""
Result types and data structures for evaluation results.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ResultStatus(str, Enum):
    """Status of an evaluation result."""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


class Severity(str, Enum):
    """Severity levels for issues."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class EvaluationResult(BaseModel):
    """Complete evaluation result for a single test case."""

    # Identification
    test_case_id: str
    test_case_name: str
    category: str
    phase: str

    # Status
    status: ResultStatus = ResultStatus.PASS
    score: float = Field(ge=0.0, le=100.0)
    pass_threshold: float = 80.0

    # Metrics
    primary_metric: str = "accuracy"
    primary_score: float = 0.0
    secondary_metrics: Dict[str, float] = Field(default_factory=dict)

    # Details
    expected_output: Optional[Any] = None
    actual_output: Optional[Any] = None
    raw_response: Optional[str] = None

    # Issues
    issues: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    # Timing
    execution_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)

    # Metadata
    model: str = ""
    provider: str = ""
    test_data_source: Optional[str] = None

    @property
    def passed(self) -> bool:
        """Check if result passed the threshold."""
        return self.status == ResultStatus.PASS and self.score >= self.pass_threshold

    @property
    def failed(self) -> bool:
        """Check if result failed."""
        return self.status in [ResultStatus.FAIL, ResultStatus.ERROR]

    def add_issue(self, severity: Severity, message: str, details: Optional[Dict] = None) -> None:
        """Add an issue to the result."""
        self.issues.append({
            "severity": severity.value,
            "message": message,
            "details": details or {}
        })
        if severity in [Severity.CRITICAL, Severity.HIGH]:
            self.status = ResultStatus.FAIL


class PhaseResult(BaseModel):
    """Aggregated results for an evaluation phase."""

    phase: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0

    overall_score: float = 0.0
    phase_threshold: float = 80.0

    results: List[EvaluationResult] = Field(default_factory=list)
    issues_by_severity: Dict[Severity, int] = Field(default_factory=lambda: {
        Severity.CRITICAL: 0,
        Severity.HIGH: 0,
        Severity.MEDIUM: 0,
        Severity.LOW: 0
    })

    execution_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100

    @property
    def passed(self) -> bool:
        """Check if phase passed overall."""
        return self.overall_score >= self.phase_threshold

    def add_result(self, result: EvaluationResult) -> None:
        """Add a result and update aggregations."""
        self.results.append(result)
        self.total_tests += 1

        if result.passed:
            self.passed_tests += 1
        elif result.failed:
            self.failed_tests += 1
        else:
            self.skipped_tests += 1

        # Update issue counts
        for issue in result.issues:
            severity = Severity(issue["severity"])
            self.issues_by_severity[severity] += 1


class BenchmarkReport(BaseModel):
    """Complete benchmark report."""

    # Metadata
    benchmark_version: str = "1.0.0"
    report_version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)

    # Model info
    model_name: str
    model_provider: str

    # Overall results
    overall_score: float = 0.0
    quality_gate_passed: bool = False

    # Phase results
    phases: Dict[str, PhaseResult] = Field(default_factory=dict)

    # Summary
    total_tests: int = 0
    total_passed: int = 0
    total_failed: int = 0
    critical_issues: int = 0
    high_issues: int = 0

    # Configuration
    config: Optional[Dict] = None

    # Raw outputs (optional)
    raw_outputs: Dict[str, Any] = Field(default_factory=dict)

    def calculate_overall_score(self) -> float:
        """Calculate overall benchmark score from phase scores."""
        if not self.phases:
            return 0.0

        weights = {
            "foundation": 0.20,
            "dialogue": 0.20,
            "migration": 0.30,
            "safety": 0.15,
            "performance": 0.15
        }

        total_weight = 0.0
        weighted_sum = 0.0

        for phase_name, phase_result in self.phases.items():
            weight = weights.get(phase_name, 0.20)
            weighted_sum += phase_result.overall_score * weight
            total_weight += weight

        self.overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        return self.overall_score

    def check_quality_gates(self, gates: Dict[str, float]) -> bool:
        """
        Check if all quality gates are passed.

        Gates:
        - overall_score: Minimum overall score
        - critical_issues: Maximum critical issues allowed
        - high_issues: Maximum high issues allowed
        """
        passed = True

        if "overall_score" in gates:
            passed = passed and self.overall_score >= gates["overall_score"]

        if "critical_issues" in gates:
            passed = passed and self.critical_issues <= gates["critical_issues"]

        if "high_issues" in gates:
            passed = passed and self.high_issues <= gates["high_issues"]

        self.quality_gate_passed = passed
        return passed

    def to_dict(self, include_raw: bool = False) -> Dict:
        """Convert report to dictionary."""
        data = self.model_dump()

        if not include_raw:
            data.pop("raw_outputs", None)

        return data

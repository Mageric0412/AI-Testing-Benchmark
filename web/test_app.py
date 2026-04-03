"""
Web界面测试 - 验证Gradio应用功能。
"""

import pytest
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_testing_benchmark.core.test_suite_loader import (
    TestSuiteLoader,
    TestCase,
    Scenario,
    LoadedTestSuite
)
from ai_testing_benchmark.core.scoring_engine import (
    ScoringEngine,
    ScoreResult,
    ConfidenceLevel
)


class TestTestSuiteLoader:
    """测试套件加载器测试。"""

    def test_parse_sheet_types(self):
        """测试Sheet类型检测。"""
        loader = TestSuiteLoader()

        # 模拟sheet数据
        test_cases_data = [
            {"id": "TC001", "scenario_id": "SC001", "phase": "test", "description": "test"}
        ]
        scenarios_data = [
            {"id": "SC001", "name": "Test", "description": "test", "test_case_ids": "TC001"}
        ]

        assert loader._detect_sheet_type("test_cases", test_cases_data).value == "test_cases"
        assert loader._detect_sheet_type("scenarios", scenarios_data).value == "scenarios"

    def test_parse_test_cases(self):
        """测试测试用例解析。"""
        loader = TestSuiteLoader()

        data = [
            {
                "id": "TC001",
                "scenario_id": "SC001",
                "phase": "resource_import",
                "description": "测试用例1",
                "input": '{"key": "value"}',
                "priority": "P0"
            }
        ]

        cases = loader._parse_test_cases(data)
        assert len(cases) == 1
        assert cases[0].id == "TC001"
        assert cases[0].phase == "resource_import"
        assert cases[0].priority == "P0"


class TestScoringEngine:
    """评分引擎测试。"""

    def test_default_config(self):
        """测试默认配置。"""
        engine = ScoringEngine()

        assert engine.config.pass_threshold == 0.80
        assert engine.config.critical_threshold == 0.60
        assert "accuracy" in engine.config.formulas

    def test_calculate_accuracy(self):
        """测试准确率计算。"""
        engine = ScoringEngine()

        predictions = [1, 0, 1, 1, 0]
        references = [1, 0, 1, 0, 0]

        result = engine.calculate_score("accuracy", predictions, references)
        assert result.score == 0.8  # 4/5 correct
        assert result.confidence > 0

    def test_is_passed(self):
        """测试通过判断。"""
        engine = ScoringEngine()

        assert engine.is_passed(0.85) == True
        assert engine.is_passed(0.80) == True
        assert engine.is_passed(0.79) == False
        assert engine.is_critical(0.59) == True
        assert engine.is_critical(0.60) == False

    def test_confidence_levels(self):
        """测试置信度等级。"""
        engine = ScoringEngine()

        assert engine._get_confidence_level(0.95) == ConfidenceLevel.HIGH
        assert engine._get_confidence_level(0.80) == ConfidenceLevel.MEDIUM
        assert engine._get_confidence_level(0.60) == ConfidenceLevel.LOW
        assert engine._get_confidence_level(0.40) == ConfidenceLevel.VERY_LOW

    def test_aggregate_scores(self):
        """测试分数聚合。"""
        engine = ScoringEngine()

        results = [
            ScoreResult(score=0.9, confidence=0.9, confidence_level=ConfidenceLevel.HIGH,
                       components={}, formula_used="accuracy"),
            ScoreResult(score=0.8, confidence=0.8, confidence_level=ConfidenceLevel.MEDIUM,
                       components={}, formula_used="accuracy"),
        ]

        aggregated = engine.aggregate_scores(results)
        assert aggregated.score == 0.85


class TestPlotlyCharts:
    """Plotly图表测试。"""

    def test_score_chart_creation(self):
        """测试分数图表创建。"""
        from web.app import create_score_chart

        results = [
            {"phase": "test", "score": 0.9, "passed": True, "confidence": 0.9},
            {"phase": "test", "score": 0.8, "passed": True, "confidence": 0.8},
            {"phase": "test", "score": 0.7, "passed": False, "confidence": 0.7},
        ]

        fig = create_score_chart(results)
        assert fig is not None
        assert len(fig.data) == 2  # histogram + bar

    def test_pass_rate_chart_creation(self):
        """测试通过率图表创建。"""
        from web.app import create_pass_rate_chart

        results = [
            {"phase": "test1", "score": 0.9, "passed": True},
            {"phase": "test1", "score": 0.8, "passed": True},
            {"phase": "test2", "score": 0.6, "passed": False},
        ]

        fig = create_pass_rate_chart(results)
        assert fig is not None
        assert len(fig.data) == 2  # pie + bar


class TestSimulation:
    """模拟评测测试。"""

    def test_simulate_evaluation(self):
        """测试模拟评测。"""
        from web.app import simulate_evaluation
        from ai_testing_benchmark.core.test_suite_loader import TestCase

        tc = TestCase(
            id="TC001",
            scenario_id="SC001",
            phase="test",
            description="Test case"
        )

        result = simulate_evaluation(tc)

        assert result.score >= 0.6
        assert result.score <= 0.95
        assert result.confidence >= 0.7
        assert result.confidence <= 0.95


class TestReportExport:
    """报告导出测试。"""

    def setup_method(self):
        """设置测试。"""
        from web.app import state
        state.test_suite = None
        state.results = []
        state.scoring_engine = ScoringEngine()

    def test_export_json_format(self):
        """测试JSON导出。"""
        from web.app import state, export_report

        state.results = [
            {
                "test_case_id": "TC001",
                "phase": "test",
                "passed": True,
                "score": 0.9,
                "confidence": 0.9
            }
        ]

        result = export_report("JSON")
        assert "✅" in result
        assert "benchmark_report" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

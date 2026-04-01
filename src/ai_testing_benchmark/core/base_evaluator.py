"""
所有评估类型的基类评估器。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import loguru


class EvaluationResult(BaseModel):
    """评估结果的容器。"""

    scenario_id: str
    test_case_id: str
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    metrics: Dict[str, float] = Field(default_factory=dict)
    details: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    issues: List[Dict[str, Any]] = Field(default_factory=list)

    @property
    def failed(self) -> bool:
        """检查结果是否失败。"""
        return not self.passed

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BaseEvaluator(ABC):
    """
    基准测试框架中所有评估器的抽象基类。

    子类必须实现:
    - evaluate_single(): 评估单个测试用例
    - calculate_overall_score(): 将结果聚合为总体分数
    """

    def __init__(
        self,
        model_name: str,
        provider: str = "openai",
        config: Optional[Dict] = None,
        verbose: bool = False
    ):
        """
        初始化基础评估器。

        参数:
            model_name: 要评估的模型名称
            provider: 模型提供商 (openai, anthropic等)
            config: 可选配置字典
            verbose: 启用详细日志
        """
        self.model_name = model_name
        self.provider = provider
        self.config = config or {}
        self.verbose = verbose
        self.logger = loguru.logger

        if verbose:
            self.logger.enable("ai_testing_benchmark")
        else:
            self.logger.disable("ai_testing_benchmark")

    @abstractmethod
    def evaluate_single(self, test_case: Dict) -> EvaluationResult:
        """
        评估单个测试用例。

        参数:
            test_case: 包含测试用例数据的字典

        返回:
            带有分数和元数据的EvaluationResult
        """
        pass

    @abstractmethod
    def calculate_overall_score(self, results: List[EvaluationResult]) -> Dict:
        """
        从单个结果计算总体分数。

        参数:
            results: EvaluationResult对象列表

        返回:
            带有聚合分数的字典
        """
        pass

    def run_evaluation(
        self,
        test_cases: List[Dict],
        stop_on_first_failure: bool = False,
        early_stopping_threshold: float = 0.5
    ) -> Dict:
        """
        在测试用例列表上运行评估。

        参数:
            test_cases: 测试用例字典列表
            stop_on_first_failure: 任何测试失败时停止
            early_stopping_threshold: 提前停止的阈值

        返回:
            包含所有结果和摘要的字典
        """
        results = []
        failed_count = 0

        for i, test_case in enumerate(test_cases):
            self.logger.info(f"正在评估测试用例 {i+1}/{len(test_cases)}: {test_case.get('id', 'unknown')}")

            try:
                result = self.evaluate_single(test_case)
                results.append(result)

                if not result.passed:
                    failed_count += 1
                    self.logger.warning(f"测试用例 {test_case.get('id')} 失败，分数 {result.score}")

                    if stop_on_first_failure:
                        self.logger.warning("因首次失败而停止")
                        break

                    if failed_count / len(test_cases) > (1 - early_stopping_threshold):
                        self.logger.warning("已达到提前停止阈值")
                        break

            except Exception as e:
                self.logger.error(f"评估测试用例 {test_case.get('id')} 时出错: {str(e)}")
                results.append(EvaluationResult(
                    scenario_id=test_case.get("scenario_id", "unknown"),
                    test_case_id=test_case.get("id", "unknown"),
                    passed=False,
                    score=0.0,
                    errors=[str(e)]
                ))

        summary = self.calculate_overall_score(results)

        return {
            "results": results,
            "summary": summary,
            "total_tests": len(test_cases),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed)
        }

    def _build_evaluation_prompt(self, test_case: Dict, system_prompt: Optional[str] = None) -> str:
        """
        构建评估提示词。

        参数:
            test_case: 测试用例数据
            system_prompt: 可选的系统提示词覆盖

        返回:
            格式化的提示词字符串
        """
        base_prompt = system_prompt or self.config.get("system_prompt", "")

        prompt_parts = [base_prompt]

        if "description" in test_case:
            prompt_parts.append(f"\n\n任务描述:\n{test_case['description']}")

        if "input" in test_case:
            if isinstance(test_case["input"], dict):
                prompt_parts.append(f"\n\n输入数据:\n{self._format_dict(test_case['input'])}")
            else:
                prompt_parts.append(f"\n\n输入:\n{test_case['input']}")

        if "question" in test_case:
            prompt_parts.append(f"\n\n问题:\n{test_case['question']}")

        return "\n\n".join(prompt_parts)

    def _format_dict(self, d: Dict, indent: int = 0) -> str:
        """格式化字典以在提示词中显示。"""
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{'  ' * indent}{key}:")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{'  ' * indent}{key}:")
                for item in value:
                    lines.append(f"{'  ' * (indent + 1)}- {item}")
            else:
                lines.append(f"{'  ' * indent}{key}: {value}")
        return "\n".join(lines)

    def _extract_model_response(self, raw_response: Any) -> str:
        """
        从模型输出中提取文本响应。

        参数:
            raw_response: 原始模型响应

        返回:
            提取的文本字符串
        """
        if isinstance(raw_response, str):
            return raw_response
        elif isinstance(raw_response, dict):
            return raw_response.get("content", raw_response.get("text", str(raw_response)))
        elif hasattr(raw_response, "content"):
            return raw_response.content
        else:
            return str(raw_response)

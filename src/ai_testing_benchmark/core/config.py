"""
基准测试配置管理。
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import yaml
import os


class ModelConfig(BaseModel):
    """被评估模型的配置。"""

    name: str
    provider: str = "openai"
    version: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=lambda: {
        "temperature": 0.0,
        "max_tokens": 2048,
        "top_p": 1.0
    })
    credentials: Dict[str, str] = Field(default_factory=dict)


class ThresholdConfig(BaseModel):
    """评估阈值配置。"""

    accuracy: float = 0.85
    f1_score: float = 0.83
    latency_p95_ms: float = 500.0
    toxicity: float = 0.10
    fairness_score: float = 0.90


class EvaluationPhaseConfig(BaseModel):
    """评估阶段配置。"""

    enabled: bool = True
    tests: List[str] = Field(default_factory=list)
    thresholds: ThresholdConfig = Field(default_factory=ThresholdConfig)
    custom_config: Dict[str, Any] = Field(default_factory=dict)


class BenchmarkConfig(BaseModel):
    """
    AI-Testing-Benchmark的主要配置类。

    此类加载并验证完整的基准测试配置，包括模型设置、阶段配置和阈值。
    """

    version: str = "1.0.0"

    # 模型配置
    model: ModelConfig

    # 评估阶段
    foundation: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    dialogue: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    migration: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    safety: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    performance: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)

    # 报告配置
    reporting: Dict[str, Any] = Field(default_factory=lambda: {
        "format": ["json"],
        "output_dir": "./results",
        "include_raw_outputs": True
    })

    # 质量门禁
    quality_gates: Dict[str, float] = Field(default_factory=lambda: {
        "overall_score": 80.0,
        "critical_issues": 0,
        "high_issues": 3
    })

    @classmethod
    def from_yaml(cls, path: str) -> "BenchmarkConfig":
        """
        从YAML文件加载配置。

        参数:
            path: YAML配置文件路径

        返回:
            BenchmarkConfig实例
        """
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)

        return cls.from_dict(config_dict)

    @classmethod
    def from_dict(cls, config_dict: Dict) -> "BenchmarkConfig":
        """
        从字典创建配置。

        参数:
            config_dict: 配置字典

        返回:
            BenchmarkConfig实例
        """
        # 解析凭证中的环境变量
        if "model" in config_dict and "credentials" in config_dict["model"]:
            credentials = config_dict["model"]["credentials"]
            for key, value in credentials.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    credentials[key] = os.environ.get(env_var, "")

        return cls(**config_dict)

    @classmethod
    def from_env(cls) -> "BenchmarkConfig":
        """
        从环境变量创建配置。

        环境变量:
        - AI_BENCHMARK_MODEL: 模型名称
        - AI_BENCHMARK_PROVIDER: 模型提供商
        - OPENAI_API_KEY: OpenAI API密钥
        - ANTHROPIC_API_KEY: Anthropic API密钥

        返回:
            BenchmarkConfig实例
        """
        model_name = os.environ.get("AI_BENCHMARK_MODEL", "gpt-4")
        provider = os.environ.get("AI_BENCHMARK_PROVIDER", "openai")

        credentials = {}
        if provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key:
                credentials["api_key"] = api_key
        elif provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                credentials["api_key"] = api_key

        return cls(
            model=ModelConfig(
                name=model_name,
                provider=provider,
                credentials=credentials
            )
        )

    def to_yaml(self, path: str) -> None:
        """
        保存配置到YAML文件。

        参数:
            path: 输出路径
        """
        config_dict = self.model_dump()

        with open(path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)

    def is_phase_enabled(self, phase: str) -> bool:
        """
        检查阶段是否启用。

        参数:
            phase: 阶段名称 (foundation, dialogue, migration, safety, performance)

        返回:
            如果阶段启用则返回True
        """
        phase_config = getattr(self, phase, None)
        if phase_config is None:
            return False
        return phase_config.enabled

    def get_thresholds(self, phase: str) -> ThresholdConfig:
        """
        获取特定阶段的阈值。

        参数:
            phase: 阶段名称

        返回:
            该阶段的ThresholdConfig
        """
        phase_config = getattr(self, phase, None)
        if phase_config is None:
            return ThresholdConfig()
        return phase_config.thresholds


class ConfigLoader:
    """
    从各种来源加载配置的工具类。
    """

    @staticmethod
    def load(path: Optional[str] = None, env: bool = True) -> BenchmarkConfig:
        """
        从文件或环境加载配置。

        优先级:
        1. 明确的文件路径
        2. 环境变量
        3. 默认配置

        参数:
            path: 配置文件路径(可选)
            env: 如果没有提供文件是否从环境加载

        返回:
            BenchmarkConfig实例
        """
        if path:
            return BenchmarkConfig.from_yaml(path)

        if env:
            # 检查环境中的配置文件路径
            config_path = os.environ.get("AI_BENCHMARK_CONFIG")
            if config_path:
                return BenchmarkConfig.from_yaml(config_path)

            # 尝试从环境变量加载
            try:
                return BenchmarkConfig.from_env()
            except Exception:
                pass

        # 返回默认配置
        return BenchmarkConfig(
            model=ModelConfig(name="gpt-4", provider="openai")
        )

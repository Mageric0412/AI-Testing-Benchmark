"""
Benchmark configuration management.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import yaml
import os


class ModelConfig(BaseModel):
    """Configuration for the model under evaluation."""

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
    """Configuration for evaluation thresholds."""

    accuracy: float = 0.85
    f1_score: float = 0.83
    latency_p95_ms: float = 500.0
    toxicity: float = 0.10
    fairness_score: float = 0.90


class EvaluationPhaseConfig(BaseModel):
    """Configuration for an evaluation phase."""

    enabled: bool = True
    tests: List[str] = Field(default_factory=list)
    thresholds: ThresholdConfig = Field(default_factory=ThresholdConfig)
    custom_config: Dict[str, Any] = Field(default_factory=dict)


class BenchmarkConfig(BaseModel):
    """
    Main configuration for AI-Testing-Benchmark.

    This class loads and validates the complete benchmark configuration
    including model settings, phase configurations, and thresholds.
    """

    version: str = "1.0.0"

    # Model configuration
    model: ModelConfig

    # Evaluation phases
    foundation: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    dialogue: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    migration: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    safety: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)
    performance: EvaluationPhaseConfig = Field(default_factory=EvaluationPhaseConfig)

    # Reporting
    reporting: Dict[str, Any] = Field(default_factory=lambda: {
        "format": ["json"],
        "output_dir": "./results",
        "include_raw_outputs": True
    })

    # Quality gates
    quality_gates: Dict[str, float] = Field(default_factory=lambda: {
        "overall_score": 80.0,
        "critical_issues": 0,
        "high_issues": 3
    })

    @classmethod
    def from_yaml(cls, path: str) -> "BenchmarkConfig":
        """
        Load configuration from YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            BenchmarkConfig instance
        """
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)

        return cls.from_dict(config_dict)

    @classmethod
    def from_dict(cls, config_dict: Dict) -> "BenchmarkConfig":
        """
        Create configuration from dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            BenchmarkConfig instance
        """
        # Resolve environment variables in credentials
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
        Create configuration from environment variables.

        Environment variables:
        - AI_BENCHMARK_MODEL: Model name
        - AI_BENCHMARK_PROVIDER: Model provider
        - OPENAI_API_KEY: OpenAI API key
        - ANTHROPIC_API_KEY: Anthropic API key

        Returns:
            BenchmarkConfig instance
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
        Save configuration to YAML file.

        Args:
            path: Output path
        """
        config_dict = self.model_dump()

        with open(path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)

    def is_phase_enabled(self, phase: str) -> bool:
        """
        Check if a phase is enabled.

        Args:
            phase: Phase name (foundation, dialogue, migration, safety, performance)

        Returns:
            True if phase is enabled
        """
        phase_config = getattr(self, phase, None)
        if phase_config is None:
            return False
        return phase_config.enabled

    def get_thresholds(self, phase: str) -> ThresholdConfig:
        """
        Get thresholds for a specific phase.

        Args:
            phase: Phase name

        Returns:
            ThresholdConfig for the phase
        """
        phase_config = getattr(self, phase, None)
        if phase_config is None:
            return ThresholdConfig()
        return phase_config.thresholds


class ConfigLoader:
    """
    Utility class for loading configurations from various sources.
    """

    @staticmethod
    def load(path: Optional[str] = None, env: bool = True) -> BenchmarkConfig:
        """
        Load configuration from file or environment.

        Priority:
        1. Explicit file path
        2. Environment variables
        3. Default configuration

        Args:
            path: Optional path to configuration file
            env: Whether to load from environment if no file provided

        Returns:
            BenchmarkConfig instance
        """
        if path:
            return BenchmarkConfig.from_yaml(path)

        if env:
            # Check for config file path in environment
            config_path = os.environ.get("AI_BENCHMARK_CONFIG")
            if config_path:
                return BenchmarkConfig.from_yaml(config_path)

            # Try to load from environment variables
            try:
                return BenchmarkConfig.from_env()
            except Exception:
                pass

        # Return default configuration
        return BenchmarkConfig(
            model=ModelConfig(name="gpt-4", provider="openai")
        )

"""
AI-Testing-Benchmark 快速开始指南。

本示例展示如何快速运行基础评估。
"""

import os
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig


def quickstart_basic():
    """基础快速开始"""
    print("=" * 60)
    print("快速开始：基础模型评估")
    print("=" * 60)

    config = BenchmarkConfig(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    runner = BenchmarkRunner(config=config, verbose=True)

    print("\n正在运行基础模型评估...")
    foundation_results = runner.run_phase("foundation")

    print(f"\n基础阶段结果:")
    print(f"  分数: {foundation_results.overall_score:.2f}")
    print(f"  测试: {foundation_results.passed_tests}/{foundation_results.total_tests} 通过")
    print(f"  通过率: {foundation_results.pass_rate:.1f}%")


def quickstart_with_env():
    """使用环境变量的快速开始"""
    print("\n" + "=" * 60)
    print("快速开始：使用环境变量")
    print("=" * 60)

    model_name = os.environ.get("AI_BENCHMARK_MODEL", "gpt-4")
    provider = os.environ.get("AI_BENCHMARK_PROVIDER", "openai")
    api_key = os.environ.get("OPENAI_API_KEY", "")

    config = BenchmarkConfig(
        model=ModelConfig(
            name=model_name,
            provider=provider,
            credentials={"api_key": api_key} if api_key else {}
        )
    )

    runner = BenchmarkRunner(config=config, verbose=True)
    print(f"\n正在对 {model_name} ({provider}) 进行基准测试...")

    results = runner.run_phase("foundation")
    print(f"\n结果: {results.overall_score:.2f}")


def quickstart_dialogue():
    """对话评估快速开始"""
    print("\n" + "=" * 60)
    print("快速开始：对话评估")
    print("=" * 60)

    config = BenchmarkConfig(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    runner = BenchmarkRunner(config=config, verbose=True)
    print("\n正在运行对话评估...")

    dialogue_results = runner.run_phase("dialogue")

    print(f"\n对话阶段结果:")
    print(f"  分数: {dialogue_results.overall_score:.2f}")


def quickstart_migration():
    """云迁移评估快速开始"""
    print("\n" + "=" * 60)
    print("快速开始：云迁移评估")
    print("=" * 60)

    config = BenchmarkConfig(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    runner = BenchmarkRunner(config=config, verbose=True)
    print("\n正在运行云迁移评估...")

    migration_results = runner.run_phase("migration")

    print(f"\n迁移阶段结果:")
    print(f"  分数: {migration_results.overall_score:.2f}")


def main():
    """运行所有快速开始示例"""
    print("\n" + "=" * 60)
    print("AI-Testing-Benchmark 快速开始指南")
    print("=" * 60)

    quickstart_basic()
    quickstart_with_env()
    quickstart_dialogue()
    quickstart_migration()

    print("\n" + "=" * 60)
    print("快速开始完成！")
    print("=" * 60)
    print("""
后续步骤：
1. 查看 examples/ 目录下的完整示例
2. 阅读 docs/ 目录下的详细文档
3. 运行 python examples/full_benchmark.py 进行完整评估
""")


if __name__ == "__main__":
    main()

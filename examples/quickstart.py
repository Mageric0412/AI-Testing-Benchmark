"""
AI-Testing-Benchmark 快速开始示例。
"""

from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig


def main():
    """运行快速基准测试。"""
    # 创建配置
    config = BenchmarkConfig(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": "your-api-key"}
        )
    )

    # 初始化运行器
    runner = BenchmarkRunner(config=config, verbose=True)

    # 仅运行基础评估
    print("正在运行基础模型评估...")
    foundation_results = runner.run_phase("foundation")

    print(f"\n基础阶段结果:")
    print(f"  分数: {foundation_results.overall_score:.2f}")
    print(f"  测试: {foundation_results.passed_tests}/{foundation_results.total_tests} 通过")
    print(f"  通过率: {foundation_results.pass_rate:.1f}%")

    return foundation_results


if __name__ == "__main__":
    main()

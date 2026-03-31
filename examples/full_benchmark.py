"""
完整基准测试示例，包含所有阶段。
"""

import os
from ai_testing_benchmark import BenchmarkRunner
from ai_testing_benchmark.core.config import BenchmarkConfig, ModelConfig


def main():
    """在所有阶段上运行完整基准测试。"""
    # 从环境或默认值加载配置
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

    # 初始化运行器
    runner = BenchmarkRunner(config=config, verbose=True)

    print(f"开始对 {model_name} ({provider}) 进行基准测试")
    print("=" * 60)

    # 运行完整基准测试
    report = runner.run_full_benchmark()

    # 打印摘要
    print("\n" + "=" * 60)
    print("基准测试完成")
    print("=" * 60)
    print(f"\n总体分数: {report.overall_score:.2f}")
    print(f"质量门禁: {'通过' if report.quality_gate_passed else '未通过'}")
    print(f"\n总测试数: {report.total_tests}")
    print(f"通过: {report.total_passed}")
    print(f"失败: {report.total_failed}")
    print(f"严重问题: {report.critical_issues}")
    print(f"高优先级问题: {report.high_issues}")

    print("\n阶段分数:")
    for phase_name, phase_result in report.phases.items():
        status = "通过" if phase_result.passed else "失败"
        print(f"  {phase_name}: {phase_result.overall_score:.2f} [{status}]")

    # 生成报告
    json_report = runner.generate_report(output_format="json")
    print(f"\nJSON报告已生成 ({len(json_report)} 字符)")

    # 保存报告
    runner.generate_report(
        output_format="json",
        output_path="./benchmark_results.json",
        include_raw=False
    )
    print("报告已保存至 ./benchmark_results.json")


if __name__ == "__main__":
    main()

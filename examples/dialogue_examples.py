"""
对话评估示例 - 对话AI能力测试。
"""

import os
from ai_testing_benchmark.dialogue import DialogueEvaluator
from ai_testing_benchmark.core.config import ModelConfig


def example_intent_recognition():
    """示例1: 意图识别评估"""
    print("=" * 60)
    print("示例1: 意图识别评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    # 意图识别测试
    test_conversations = [
        {
            "user_input": "我想把我们的Web服务器迁移到AWS上，应该怎么做？",
            "expected_intent": "migration_guidance"
        },
        {
            "user_input": "帮我估算一下迁移50台服务器需要多少成本？",
            "expected_intent": "cost_estimation"
        },
        {
            "user_input": "这个迁移策略有什么风险吗？",
            "expected_intent": "risk_assessment"
        },
        {
            "user_input": "能否生成一份详细的迁移计划？",
            "expected_intent": "plan_generation"
        },
        {
            "user_input": "我们应该在什么时候开始迁移测试环境？",
            "expected_intent": "timeline_planning"
        }
    ]

    results = evaluator.evaluate_intent_recognition(test_conversations)

    print(f"\n意图识别准确率: {results['accuracy']:.2%}")
    print(f"F1分数: {results['f1_score']:.2f}")

    print("\n详细结果:")
    for item in results['items']:
        status = "✓" if item['correct'] else "✗"
        print(f"  {status} 输入: {item['user_input'][:30]}...")
        print(f"      预期: {item['expected']} | 实际: {item['predicted']}")
        print(f"      置信度: {item['confidence']:.2f}")


def example_entity_extraction():
    """示例2: 实体提取评估"""
    print("\n" + "=" * 60)
    print("示例2: 实体提取评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    # 实体提取测试
    extraction_tasks = [
        {
            "input": "我们想把位于北京数据中心的50台Windows服务器迁移到AWS的华北2区域",
            "expected_entities": {
                "source_location": "北京数据中心",
                "os_type": "Windows",
                "server_count": "50",
                "target_provider": "AWS",
                "target_region": "华北2"
            }
        },
        {
            "input": "需要迁移一个PostgreSQL数据库，大小约2TB，当前运行在阿里云ECS上",
            "expected_entities": {
                "database_type": "PostgreSQL",
                "data_size": "2TB",
                "current_provider": "阿里云",
                "current_service": "ECS"
            }
        },
        {
            "input": "预算大约100万人民币，希望在6个月内完成电商平台的迁移",
            "expected_entities": {
                "budget": "100万人民币",
                "timeline": "6个月",
                "workload_type": "电商平台"
            }
        }
    ]

    results = evaluator.evaluate_entity_extraction(extraction_tasks)

    print(f"\n实体提取准确率: {results['precision']:.2%}")
    print(f"实体召回率: {results['recall']:.2%}")
    print(f"F1分数: {results['f1_score']:.2f}")

    for item in results['items']:
        print(f"\n输入: {item['input'][:40]}...")
        print(f"  提取的实体: {item['extracted_entities']}")


def example_dialogue_flow():
    """示例3: 对话流程评估"""
    print("\n" + "=" * 60)
    print("示例3: 对话流程评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    # 多轮对话测试
    dialogue_scenarios = [
        {
            "scenario_id": "DIALOG-001",
            "scenario_name": "完整迁移咨询流程",
            "conversation": [
                {"role": "user", "content": "我想了解云迁移的基本流程"},
                {"role": "assistant", "content": "云迁移通常包括以下阶段：评估、规划、执行、验证..."},
                {"role": "user", "content": "那第一步应该做什么？"},
                {"role": "assistant", "content": "第一步是评估阶段，需要进行基础设施发现、风险识别..."},
                {"role": "user", "content": "我们需要准备哪些资源？"},
                {"role": "assistant", "content": "建议准备：技术团队、足够的时间预算、以及利益相关者的支持..."}
            ],
            "evaluation_criteria": {
                "context_preservation": 0.85,
                "response_relevance": 0.90,
                "completion_rate": 1.0
            }
        },
        {
            "scenario_id": "DIALOG-002",
            "scenario_name": "问题澄清对话",
            "conversation": [
                {"role": "user", "content": "帮我迁移到云上"},
                {"role": "assistant", "content": "为了制定合适的迁移方案，请告诉我：\n1. 您有多少台服务器？\n2. 运行的是什么应用？\n3. 目标云厂商是哪家？"},
                {"role": "user", "content": "大约20台服务器，主要是Web应用，目标AWS"},
                {"role": "assistant", "content": "明白了，基于您的情况，我建议使用lift-and-shift策略..."}
            ],
            "evaluation_criteria": {
                "clarification_questions": True,
                "context_preservation": 0.90,
                "response_relevance": 0.95
            }
        }
    ]

    results = evaluator.evaluate_dialogue_flow(dialogue_scenarios)

    for result in results:
        print(f"\n场景: {result['scenario_id']} - {result['scenario_name']}")
        print(f"  对话完成率: {result['completion_rate']:.2%}")
        print(f"  上下文保持: {result['context_preservation']:.2%}")
        print(f"  响应相关性: {result['response_relevance']:.2%}")
        print(f"  用户满意度预测: {result.get('satisfaction_score', 0):.2f}")


def example_response_quality():
    """示例4: 响应质量评估"""
    print("\n" + "=" * 60)
    print("示例4: 响应质量评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model=ModelConfig(
            name="gpt-4",
            provider="openai",
            credentials={"api_key": os.environ.get("OPENAI_API_KEY", "")}
        )
    )

    quality_tests = [
        {
            "query": "什么是云迁移的5R策略？",
            "response": "云迁移的5R策略（也称为6R的一部分）包括：\n"
                       "1. Rehost（重新托管）- 直接迁移，不做更改\n"
                       "2. Replatform（重新平台化）- 做少量调整以适应云平台\n"
                       "3. Refactor（重构）- 重新架构以充分利用云原生特性\n"
                       "4. Repurchase（重新购买）- 转向SaaS解决方案\n"
                       "5. Retire（淘汰）- 停用不再需要的应用\n"
                       "6. Retain（保留）- 暂时不迁移，留在本地",
            "criteria": ["accuracy", "completeness", "clarity", "helpfulness"]
        },
        {
            "query": "我们的数据库很老，迁移到云上会有什么问题？",
            "response": "老旧数据库迁移到云上可能面临以下挑战：\n"
                       "1. 兼容性问题 - 旧版数据库可能与云DB服务不兼容\n"
                       "2. 性能问题 - 未针对云环境优化的查询可能变慢\n"
                       "3. 依赖复杂性 - 可能有硬编码的连接字符串\n"
                       "4. 数据量问题 - 大型数据库迁移时间长\n"
                       "建议先进行兼容性评估，可能需要重构或选择托管数据库服务。",
            "criteria": ["accuracy", "helpfulness", "safety"]
        }
    ]

    results = evaluator.evaluate_response_quality(quality_tests)

    for result in results:
        print(f"\n查询: {result['query'][:40]}...")
        print(f"  准确性: {result['accuracy']:.2f}")
        print(f"  完整性: {result['completeness']:.2f}")
        print(f"  清晰度: {result['clarity']:.2f}")
        print(f"  有用性: {result['helpfulness']:.2f}")
        print(f"  安全性: {result['safety']:.2f}")


if __name__ == "__main__":
    example_intent_recognition()
    example_entity_extraction()
    example_dialogue_flow()
    example_response_quality()

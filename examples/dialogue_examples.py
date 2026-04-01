"""
对话评估示例 - 对话AI能力测试。
"""

import os
from ai_testing_benchmark.dialogue import DialogueEvaluator


def example_intent_recognition():
    """示例1: 意图识别评估"""
    print("=" * 60)
    print("示例1: 意图识别评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    # 意图识别测试
    test_conversations = [
        {
            "id": "DIAL-INTENT-001",
            "category": "intent_recognition",
            "user_utterance": "我想把我们的Web服务器迁移到AWS上，应该怎么做？",
            "expected_intent": "migration_guidance"
        },
        {
            "id": "DIAL-INTENT-002",
            "category": "intent_recognition",
            "user_utterance": "帮我估算一下迁移50台服务器需要多少成本？",
            "expected_intent": "cost_estimation"
        },
        {
            "id": "DIAL-INTENT-003",
            "category": "intent_recognition",
            "user_utterance": "这个迁移策略有什么风险吗？",
            "expected_intent": "risk_assessment"
        },
        {
            "id": "DIAL-INTENT-004",
            "category": "intent_recognition",
            "user_utterance": "能否生成一份详细的迁移计划？",
            "expected_intent": "plan_generation"
        },
        {
            "id": "DIAL-INTENT-005",
            "category": "intent_recognition",
            "user_utterance": "我们应该在什么时候开始迁移测试环境？",
            "expected_intent": "timeline_planning"
        }
    ]

    for test_case in test_conversations:
        result = evaluator.evaluate_single(test_case)
        print(f"\n输入: {test_case['user_utterance'][:40]}...")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_entity_extraction():
    """示例2: 实体提取评估"""
    print("\n" + "=" * 60)
    print("示例2: 实体提取评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    # 实体提取测试
    extraction_tasks = [
        {
            "id": "DIAL-ENTITY-001",
            "category": "entity_extraction",
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
            "id": "DIAL-ENTITY-002",
            "category": "entity_extraction",
            "input": "需要迁移一个PostgreSQL数据库，大小约2TB，当前运行在阿里云ECS上",
            "expected_entities": {
                "database_type": "PostgreSQL",
                "data_size": "2TB",
                "current_provider": "阿里云",
                "current_service": "ECS"
            }
        },
        {
            "id": "DIAL-ENTITY-003",
            "category": "entity_extraction",
            "input": "预算大约100万人民币，希望在6个月内完成电商平台的迁移",
            "expected_entities": {
                "budget": "100万人民币",
                "timeline": "6个月",
                "workload_type": "电商平台"
            }
        }
    ]

    for test_case in extraction_tasks:
        result = evaluator.evaluate_single(test_case)
        print(f"\n输入: {test_case['input'][:40]}...")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_dialogue_flow():
    """示例3: 对话流程评估"""
    print("\n" + "=" * 60)
    print("示例3: 对话流程评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    # 多轮对话测试
    dialogue_scenarios = [
        {
            "id": "DIALOG-001",
            "category": "journey",
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
            "id": "DIALOG-002",
            "category": "journey",
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

    for test_case in dialogue_scenarios:
        result = evaluator.evaluate_single(test_case)
        print(f"\n场景: {test_case['scenario_name']}")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


def example_response_quality():
    """示例4: 响应质量评估"""
    print("\n" + "=" * 60)
    print("示例4: 响应质量评估")
    print("=" * 60)

    evaluator = DialogueEvaluator(
        model_name="gpt-4",
        provider="openai"
    )

    quality_tests = [
        {
            "id": "DIAL-QUAL-001",
            "category": "response_quality",
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
            "id": "DIAL-QUAL-002",
            "category": "response_quality",
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

    for test_case in quality_tests:
        result = evaluator.evaluate_single(test_case)
        print(f"\n查询: {test_case['query'][:40]}...")
        print(f"  分数: {result.score:.2f}")
        print(f"  通过: {result.passed}")


if __name__ == "__main__":
    example_intent_recognition()
    example_entity_extraction()
    example_dialogue_flow()
    example_response_quality()
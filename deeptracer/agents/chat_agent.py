from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from deeptracer.agents.schemas import ChatAgentResult
from deeptracer.agents.utils import to_json_text
from deeptracer.modeling.llm import get_chat_model


def run_chat_agent(
    code: str,
    structure_result: dict,
    performance_result: dict,
    memory_result: dict,
    refactor_result: dict,
    teaching_result: dict,
    user_input: str = "",
    conversation_history: list = None
) -> dict:
    """
    聊天智能体：基于所有智能体的分析结果，与用户讨论和修正代码
    
    Args:
        code: 原始代码
        structure_result: 结构分析结果
        performance_result: 性能分析结果
        memory_result: 内存分析结果
        refactor_result: 重构建议结果
        teaching_result: 教学分析结果
        user_input: 用户输入的消息
        conversation_history: 对话历史
    
    Returns:
        包含讨论内容、问题、下一步建议和对话历史的字典
    """
    llm = get_chat_model(optional=True)
    conversation_history = conversation_history or []

    if llm is None:
        return {
            "discussion": "基于分析结果，我们发现了一些可以改进的地方。请查看重构建议并考虑如何应用它们。" + 
                         (" " + teaching_result.get("overview", "") if teaching_result else ""),
            "questions": [
                "你希望优先解决哪方面的问题？（结构/性能/内存）",
                "代码的主要功能是什么？",
                "你对代码的性能有什么特定要求？"
            ],
            "next_steps": [
                "查看重构建议列表",
                "选择优先级高的建议进行修改",
                "重新运行分析验证改进效果"
            ],
            "conversation_history": conversation_history
        }

    # 构建消息历史
    messages = [
        (
            "system",
            "你是 Python 代码讨论助手。基于所有智能体的分析结果，与用户讨论代码改进方案。"
            "输出要友好、专业，使用中文，适合开发者理解。",
        ),
        (
            "human",
            "原始代码：\n{code}\n\n"
            "结构分析：\n{structure}\n\n"
            "性能分析：\n{performance}\n\n"
            "内存分析：\n{memory}\n\n"
            "重构建议：\n{refactor}\n\n"
            "教学分析：\n{teaching}\n\n",
        ),
    ]

    # 添加对话历史
    for msg in conversation_history:
        messages.append((msg["role"], msg["content"]))

    # 添加用户输入
    if user_input:
        messages.append(("human", user_input))

    # 构建提示词
    prompt = ChatPromptTemplate.from_messages(messages)
    
    # 构建输出格式指令
    output_instructions = ""
    if not user_input:
        output_instructions = """
        请：
        1. 总结所有分析结果，形成一个连贯的讨论，特别结合教学分析的见解
        2. 提出3个问题，帮助用户进一步澄清需求
        3. 给出3个具体的下一步建议
        """
    else:
        output_instructions = """
        请：
        1. 基于对话历史和用户最新输入，提供相关的回应
        2. 解答用户的问题
        3. 提供进一步的建议或指导
        """

    # 添加输出格式指令
    if output_instructions:
        if messages[-1][0] == "human":
            messages[-1] = ("human", messages[-1][1] + output_instructions)
        else:
            messages.append(("human", output_instructions))

    chain = prompt | llm.with_structured_output(ChatAgentResult)
    result = chain.invoke({
        "code": code,
        "structure": to_json_text(structure_result),
        "performance": to_json_text(performance_result),
        "memory": to_json_text(memory_result),
        "refactor": to_json_text(refactor_result),
        "teaching": to_json_text(teaching_result)
    })

    # 更新对话历史
    assistant_message = {
        "role": "assistant",
        "content": result.discussion
    }
    new_history = conversation_history.copy()
    if user_input:
        new_history.append({"role": "user", "content": user_input})
    new_history.append(assistant_message)

    result_dict = result.model_dump()
    result_dict["conversation_history"] = new_history
    
    return result_dict

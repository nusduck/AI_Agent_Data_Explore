
from core.state import GraphState
from agents.agent_coder import agent_coder


def execute_node(state: GraphState) -> GraphState:
    prompt = """
    You are a helpful assistant that can help with coding tasks for data analysis.
    Here is the data path:
    {data_path};
    Data description:
    {data_description}
    Data Samples:
    {data_samples}
    Your task:
    {task}
    Notice:
    - 设置后端为Agg（非交互式）
    - Don't use jupyter notebook, just use python
    - Don't print module name, just use it directly
    - 注意日期格式，不要使用字符串
    - 使用plt.savefig()保存图像
        save path: outputs/{number}/visualization/
    - 不调用plt.show()
    - 相同类型的图画在同一个图里
    - 图片原则：
        风格类型：极简主义/科技感/复古/高对比度/深色模式
        核心参数：style.use(), set_palette(), rcParams, figsize, grid, despine
        设计原则：信息优先（Data-Ink Ratio）、一致性、无障碍色觉设计，确保标题、标签、图例和注释清晰可读
    - Fianl output your analysis result as the markdown format.
        根据代码执行结果生成分析报告
        使用数据一一对'Plan'进行说明
        如有建模请对模型进行解释
        使用英语
        save path: outputs/{number}/analysis/
    """.format(number=state["number"], data_path=state["raw_data_path"],data_samples = state["raw_data_samples"], data_description=state["raw_data_description"], task=state["analysis_plan"])
    messages = [{
        "role": "user",
        "content": prompt
    }]
    codeact = agent_coder(state)
    try:
        # 调用agent并获取结果
        result = codeact.invoke({"messages": messages})
        
        # 确保返回值是可序列化的，只提取所需信息
        last_message_content = result["messages"][-1].content if result.get("messages") and len(result["messages"]) > 0 else ""
        
        # 返回一个简单的字典，确保可以序列化
        return {"analysis_status": "completed"}
    except Exception as e:
        # 记录错误并返回可序列化的错误信息
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in execute_node: {str(e)}\n{error_trace}")
        return {"analysis_status": f"Error during analysis: {str(e)}", "error": str(e)}
    # result = codeact.invoke({"messages": messages})
    # # print(result["messages"][-1].content)
    # return {"analysis_status": "completed"}
    # for typ, chunk in codeact.stream(
    #     {"messages": messages},
    #     stream_mode=["values", "messages"],
    #     config={"configurable": {"thread_id": 1}},
    # ):
    #     if typ == "messages":
    #         print(chunk[0].content, end="")
    #     elif typ == "values":
    #         print("\n\n---answer---\n\n", chunk)


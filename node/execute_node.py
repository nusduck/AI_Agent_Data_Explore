
from core.state import GraphState
from agents.agent_coder import agent_coder


def execute_node(state: GraphState) -> GraphState:
    prompt = """
    You are a helpful assistant that can help with coding tasks for data analysis.
    Here is the data path:
    {data_path};
    Data description:
    {data_description}
    Your task:
    {task}
    Notice:
    - 设置后端为Agg（非交互式）
    - Don't use jupyter notebook, just use python
    - Don't print module name, just use it directly
    - 注意日期格式，不要使用字符串
    - 使用plt.savefig()保存图像
        keep path: outputs/{number}/visualization/
    - 不调用plt.show()
    - 相同类型的图画在同一个图里
    - 图片原则：
        风格类型：极简主义/科技感/复古/高对比度/深色模式
        核心参数：style.use(), set_palette(), rcParams, figsize, grid, despine
        设计原则：信息优先（Data-Ink Ratio）、一致性、无障碍色觉设计
    - Fianl output your analysis result in the markdown format in the end which should support by the data.
        Keep path: outputs/{number}/analysis/
    """.format(number=state["number"], data_path=state["raw_data_path"], data_description=state["raw_data_description"], task=state["analysis_plan"])
    messages = [{
        "role": "user",
        "content": prompt
    }]
    codeact = agent_coder(state)
    result = codeact.invoke({"messages": messages})
    # print(result["messages"][-1].content)
    return {"analysis_summary": result["messages"][-1].content}
    # for typ, chunk in codeact.stream(
    #     {"messages": messages},
    #     stream_mode=["values", "messages"],
    #     config={"configurable": {"thread_id": 1}},
    # ):
    #     if typ == "messages":
    #         print(chunk[0].content, end="")
    #     elif typ == "values":
    #         print("\n\n---answer---\n\n", chunk)


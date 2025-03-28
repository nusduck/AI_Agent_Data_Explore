
from core.state import GraphState
from agents.agent_coder import agent_coder


def execute_node(state: GraphState) -> GraphState:
    prompt = """
    You are a helpful assistant that can help with coding tasks for data analysis.
    Here is the data path:
    {data_path};
    Your task:
    {task}
    Notice:
    - 设置后端为Agg（非交互式）
    - if the the data is time series data, change the index to datetime
    - 使用plt.savefig()保存图像
        keep path: outputs/visualization/
    - 不调用plt.show()
    - 图片原则：
        风格类型：极简主义/科技感/复古/高对比度/深色模式
        核心参数：style.use(), set_palette(), rcParams, figsize, grid, despine
        设计原则：信息优先（Data-Ink Ratio）、一致性、无障碍色觉设计
    - Fianl output your analysis result in the markdown format in the end.
    """.format(data_path=state["raw_data_path"], task=state["analysis_plan"])
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


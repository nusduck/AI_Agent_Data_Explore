# LangGraph EDA Supervisor Agent - 编码思路

## 1. 目标

构建一个基于 LangGraph 的自动化框架，用于执行数据可视化和探索性数据分析 (EDA)。该框架以 Supervisor 模式运行，协调多个 специализированный Agent 完成从数据接收到报告生成的完整流程，并包含人工干预环节。

## 2. 核心架构与 LangGraph 映射

我们将 Mermaid 图中的 `CoreProcessing` 环节映射到 LangGraph 的节点和边。

*   **Supervisor**: LangGraph 的 `StateGraph` 本身以及控制节点间转换的逻辑担当 Supervisor 的角色。它根据当前状态决定下一个调用的节点。
*   **State (`graph/state.py`)**: 定义一个 `TypedDict` (`GraphState`) 来贯穿整个流程，包含：
    *   `raw_data_path`: 原始数据路径。
    *   `validated_data_path`: 验证/预处理后数据路径。
    *   `analysis_params`: 用户输入的分析参数。
    *   `analysis_plan`: LLM 生成的分析步骤。
    *   `generated_code`: LLM 生成的 Python 代码。
    *   `execution_stdout`: 代码执行的标准输出。
    *   `execution_stderr`: 代码执行的标准错误。
    *   `generated_files`: 代码执行生成的文件列表（如图表）。
    *   `analysis_summary`: 对结果的文字总结。
    *   `report_content`: 最终报告内容。
    *   `error_message`: 流程中发生的错误信息。
    *   `user_feedback`: 用户反馈。
    *   `agent_outcome`: 最近一次 Agent 执行的结果（用于路由）。
*   **Nodes (`graph/nodes.py`)**:
    *   `validate_data`: (Function Node) 对应 `F`. 调用 `utils/data_validation.py`。
    *   `plan_analysis`: (ReAct Agent Node) 对应 `G`. 使用 `agents/planner.py` 和 `prompts/planner_prompt`.
    *   `generate_code`: (ReAct Agent Node) 对应 `H`. 使用 `agents/coder.py` 和 `prompts/coder_prompt`.
    *   `execute_code`: (Function Node) 对应 `I`. 调用 `tools/python_executor.py` 执行代码。**需要严格的沙箱环境！**
    *   `integrate_results`: (Function Node or Agent Node) 对应 `J`. 分析执行输出和生成的文件。
    *   `generate_report`: (ReAct Agent Node or Function Node) 对应 `L`. 使用 `agents/reporter.py` 或简单格式化。
    *   `handle_error`: (Function Node) 统一处理流程中的错误。
    *   `ask_human_for_plan_review`: (Function Node) 准备计划信息，返回 `Interrupt`.
    *   `ask_human_for_results_review`: (Function Node) 准备结果信息，返回 `Interrupt`.
*   **Edges (`graph/builder.py`)**:
    *   **Normal Edges**: 定义节点间的顺序流，如 `validate_data` -> `plan_analysis`.
    *   **Conditional Edges**:
        *   从 `execute_code` 出发：根据执行成功/失败以及是否有 `stderr` 分支到 `integrate_results` 或 `handle_error` 或 `ask_human_for_results_review`。
        *   从 `plan_analysis` 出发：分支到 `ask_human_for_plan_review`。
        *   从 `integrate_results` 出发：分支到 `ask_human_for_results_review` 或 `generate_report`。
    *   **Human Intervention Edges**:
        *   `ask_human_for_plan_review` -> `END` (Interrupt). 需要一个入口点在 `main.py` 中接收反馈并重新注入状态，然后路由到 `generate_code` 或回到 `plan_analysis`。
        *   `ask_human_for_results_review` -> `END` (Interrupt). 类似地，接收反馈后路由到 `generate_report` 或要求重新执行/编码/规划。
*   **Tools (`tools/`)**:
    *   `safe_python_executor`: 关键工具。执行 Python 代码字符串。**必须实现安全隔离** (如 Docker, `restrictedpython`, Subprocess with limits)。需要能捕获 stdout, stderr，并能访问/保存指定目录 (`outputs/`) 下的文件。
    *   `file_reader`/`file_writer`: 读写文件系统中的数据和结果。
*   **Agents (`agents/`)**:
    *   使用 `langchain` 和 `langgraph.prebuilt.create_react_agent` 创建。
    *   提供清晰的 Prompt (`prompts/`)，指导 Agent 的任务、可用工具和输出格式。
    *   Planner Agent: 输入数据描述/Schema、用户目标，输出结构化的分析步骤。
    *   Coder Agent: 输入分析步骤、数据 Schema，输出 Python 代码（使用 Pandas, Matplotlib, Seaborn 等）。确保代码能保存图表到文件。

## 3. 关键实现点

*   **安全执行 (`tools/python_executor.py`)**: 这是最大的挑战。
    *   **初步实现 (低安全)**: 使用 `exec()` 或 `subprocess`，但有巨大风险。**绝不能在生产环境中使用！**
    *   **推荐方案**:
        *   **Docker**: 将代码写入文件，在受限的 Docker 容器中执行 Python 脚本。可以控制资源、网络访问和文件系统权限。这是最常用的方法。
        *   **`restrictedpython`**: 编译和执行受限制的 Python 代码子集。
        *   **Web Assembly (WASM)**: 如 Pyodide，在浏览器或服务器端 WASM 运行时执行。
        *   **云沙箱服务**: AWS Lambda, Google Cloud Functions 等配合严格的 IAM 权限。
    *   工具需要返回 `stdout`, `stderr`, 以及一个指示成功/失败的状态，还有生成的文件列表。
*   **Human-in-the-Loop (`main.py`, `graph/nodes.py`)**:
    *   在 `nodes.py` 中定义返回 `Interrupt` 的节点。
    *   在 `main.py` 的循环中捕获 `Interrupt`。
    *   向用户显示当前状态（计划、结果、错误）。
    *   获取用户输入（批准、修改意见、重试）。
    *   更新 `GraphState` 中的 `user_feedback` 字段。
    *   使用 `graph.invoke(state, config={"recursion_limit": 50})` 或类似方式，从中断点继续执行。图需要有处理反馈并决定下一步的逻辑（通常通过条件边实现）。
*   **Prompt Engineering (`prompts/`)**:
    *   Prompt 需要非常清晰，告诉 Agent 它的角色、任务、输入是什么、可用的工具、期望的输出格式（例如，代码块、JSON、Markdown）。
    *   对于 Coder Agent，强调代码需要包含保存图表的逻辑 (`plt.savefig`, `sns_plot.figure.savefig`) 到指定的 `outputs/` 目录，并且要在 `stdout` 中打印生成的文件名或返回文件名列表。
*   **状态管理 (`graph/state.py`)**: 确保 `GraphState` 包含所有必要的信息，并且在节点之间正确传递和更新。使用 `Annotated` 类型提示进行累加更新（如消息列表）。

## 4. 流程示例 (`main.py`)

1.  初始化 LLM, 工具。
2.  创建编译好的 LangGraph `app`。
3.  准备初始状态 `initial_state` (包含 `raw_data_path`, `analysis_params`)。
4.  设置递归限制 `config = {"recursion_limit": 50}`。
5.  开始事件循环:
    ```python
    events = app.stream(initial_state, config=config)
    for event in events:
        # 打印事件类型和节点名称 (用于调试)
        # print(event)
        if event["type"] == "interrupt":
            # === 人工干预点 ===
            current_state = event["values"] # 获取中断时的状态
            # 1. 显示需要用户审核的信息 (e.g., plan, results)
            print("--- HUMAN INTERVENTION REQUIRED ---")
            # (根据中断节点类型显示不同信息)
            # e.g., if 'ask_human_for_plan_review' in event['name']:
            #    print("Generated Plan:", current_state.get('analysis_plan'))
            # e.g., if 'ask_human_for_results_review' in event['name']:
            #    print("Execution Output:", current_state.get('execution_stdout'))
            #    print("Generated Files:", current_state.get('generated_files'))
            #    print("Errors:", current_state.get('execution_stderr'))

            # 2. 获取用户反馈
            feedback = input("Approve (y), Reject/Retry (n), or provide feedback: ")

            # 3. 更新状态 (这个状态会被重新注入图)
            #    需要将 feedback 放入 state 中，图的后续节点会读取它
            #    这里简化处理，仅作为概念说明
            if feedback.lower() == 'y':
                 # 注入一个表示批准的信号，或者直接让图流向下一步
                 # 可能需要一个专门处理反馈的节点来更新状态
                 # current_state['user_feedback'] = 'approved' # 示例
                 pass # 图的边逻辑应该处理这种情况
            else:
                 # 注入表示拒绝或修改意见的信号
                 # current_state['user_feedback'] = feedback # 示例
                 # 图的边逻辑应将流程导回规划或编码阶段
                 # 或者直接结束流程 (如果无法进行)
                 print("Action required based on feedback (implement graph logic). Stopping for now.")
                 # return # 实际应用中需要更复杂的反馈处理注入

            # 注意：LangGraph stream/invoke 不直接支持在中断后修改状态并继续。
            # 正确的做法是:
            # a) 让中断节点返回特定的状态值。
            # b) 在 main.py 中捕获中断，获取反馈。
            # c) 调用 graph.invoke/stream 时传入 *更新后的状态*，让图从合适的入口点继续。
            #    或者，设计图的边，使其能根据 state['user_feedback'] 路由。

            # !! 以下为简化演示，实际需要根据LangGraph版本和设计模式调整 !!
            #    可能需要重新调用 app.stream 或 invoke，传入包含反馈的新状态字典
            #    例如: updated_state = {**current_state, "user_feedback": feedback}
            #          app.invoke(updated_state, config=config) # 重新启动，但需确保图能处理
            print("Handling feedback and continuing...") # 模拟
            # 在实际场景中，你需要重新调用 stream/invoke 并传入更新状态

        elif event["type"] == "end":
            final_state = event["values"]
            print("\n--- FINAL RESULTS ---")
            print("Report:", final_state.get('report_content'))
            print("Generated Files:", final_state.get('generated_files'))
            if final_state.get('error_message'):
                print("Error:", final_state.get('error_message'))
    ```

## 5. 待办与改进

*   **实现健壮的 Safe Python Executor**：这是首要任务。
*   **细化 Agent Prompts**: 迭代优化 Prompt 以获得更好的规划和代码质量。
*   **错误处理**: 在每个节点增加更详细的错误捕获和报告。`handle_error` 节点需要能提供有用的调试信息。
*   **前端集成**: 当前 `main.py` 是 CLI。未来可以替换为 FastAPI/Streamlit 等 Web 框架，对接前端界面。
*   **异步执行**: 对于耗时操作（LLM 调用、代码执行），考虑使用异步节点 (`async def`) 和 `graph.astream()`。
*   **状态持久化**: 如果流程很长或需要中断后恢复，考虑将 `GraphState` 持久化到数据库或文件。
*   **可视化工具**: 可以创建更专门的工具来调用绘图库，而不是完全依赖 LLM 生成所有绘图代码。
*   **配置管理**: 使用 `python-dotenv` 或类似库管理 API 密钥和配置。
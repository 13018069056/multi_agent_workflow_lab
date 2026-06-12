from state import WorkflowState


def planner_agent(state: WorkflowState) -> WorkflowState:
    state.status = "planning"
    state.plan = [
        "实现 add(a, b) 函数",
        "审查函数是否真正执行加法",
        "运行最小测试 add(2, 3) == 5",
        "生成函数文档",
        "通过检查点后结束工作流",
    ]
    state.log("planner", "形成五步执行计划（含文档生成）")
    return state


def programmer_agent(state: WorkflowState) -> WorkflowState:
    state.status = "coding"
    state.attempts += 1
    
    if state.attempts == 1:
        state.draft = "def add(a, b):\n    return a - b\n"
    else:
        state.draft = "def add(a, b):\n    return a + b\n"
    
    state.log("programmer", f"生成第 {state.attempts} 版代码")
    return state


def reviewer_agent(state: WorkflowState) -> WorkflowState:
    state.status = "reviewing"
    
    if "return a + b" in state.draft:
        state.review_passed = True
        state.review_feedback = "代码逻辑符合加法需求。"
    else:
        state.review_passed = False
        state.review_feedback = "当前代码使用了减法，不符合 add 函数需求。"
    
    state.log("reviewer", state.review_feedback)
    return state


def tester_agent(state: WorkflowState) -> WorkflowState:
    state.status = "testing"
    namespace: dict = {"__builtins__": {}}
    
    try:
        exec(state.draft, namespace)
        result = namespace["add"](2, 3)
        state.tests_passed = result == 5
        message = "测试通过" if state.tests_passed else f"测试失败：add(2, 3)={result}"
    except Exception as exc:
        state.tests_passed = False
        message = f"测试异常：{type(exc).__name__}"
    
    state.log("tester", message)
    return state


def doc_agent(state: WorkflowState) -> WorkflowState:
    state.status = "documenting"
    
    doc_lines = []
    doc_lines.append("函数文档:")
    doc_lines.append("  函数名: add")
    doc_lines.append("  功能: 计算两个数字的和")
    doc_lines.append("  参数:")
    doc_lines.append("    a: 第一个加数")
    doc_lines.append("    b: 第二个加数")
    doc_lines.append("  返回值: 两个数的和")
    doc_lines.append("  示例: add(2, 3) = 5")
    doc_lines.append("  约束条件: " + ", ".join(state.goal.constraints))
    
    state.documentation = "\n".join(doc_lines)
    state.log("doc_agent", "已生成函数文档")
    return state


def checkpoint_agent(state: WorkflowState, auto_approve: bool) -> WorkflowState:
    state.checkpoint_required = True
    
    if auto_approve:
        state.human_approved = True
        state.status = "done"
        state.log("checkpoint", "检查点自动批准，工作流结束")
    else:
        state.human_approved = False
        state.status = "waiting_for_human"
        state.log("checkpoint", "等待人工确认")
    
    return state

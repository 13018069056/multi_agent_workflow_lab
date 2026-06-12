from state import WorkflowState


def planner_agent(state: WorkflowState) -> WorkflowState:
    state.status = "planning"
    state.plan = [
        "Implement add(a, b) function",
        "Review if function uses addition",
        "Security review the code",
        "Run test add(2, 3) == 5",
        "Pass checkpoint and finish",
    ]
    state.log("planner", "Created 5-step plan with security review")
    return state


def programmer_agent(state: WorkflowState) -> WorkflowState:
    state.status = "coding"
    state.attempts += 1
    
    if state.attempts == 1:
        state.draft = "def add(a, b):\n    return a - b\n"
    else:
        state.draft = "def add(a, b):\n    return a + b\n"
    
    state.log("programmer", f"Generated code version {state.attempts}")
    return state


def reviewer_agent(state: WorkflowState) -> WorkflowState:
    state.status = "reviewing"
    
    if "return a + b" in state.draft:
        state.review_passed = True
        state.review_feedback = "Code logic uses addition correctly."
    else:
        state.review_passed = False
        state.review_feedback = "Code uses subtraction, does not meet add requirement."
    
    state.log("reviewer", state.review_feedback)
    return state


def security_reviewer_agent(state: WorkflowState) -> WorkflowState:
    state.status = "security_review"
    
    dangerous_patterns = [
        ("__import__", "dynamic import"),
        ("exec", "dynamic execution"),
        ("eval", "dynamic evaluation"),
        ("open(", "file access"),
        ("subprocess", "system command"),
        ("os.", "OS call"),
        ("sys.", "system access"),
        ("__file__", "file path"),
        ("compile", "dynamic compilation"),
        ("__builtins__", "builtins override"),
    ]
    
    security_issues = []
    for pattern, desc in dangerous_patterns:
        if pattern in state.draft:
            security_issues.append(f"Dangerous pattern: {desc} ({pattern})")
    
    if security_issues:
        state.security_passed = False
        state.security_feedback = "; ".join(security_issues)
        state.log("security_reviewer", f"Security failed: {state.security_feedback}")
    else:
        state.security_passed = True
        state.security_feedback = "Security review passed, no dangerous patterns found"
        state.log("security_reviewer", state.security_feedback)
    
    return state


def tester_agent(state: WorkflowState) -> WorkflowState:
    state.status = "testing"
    namespace: dict = {"__builtins__": {}}
    
    try:
        exec(state.draft, namespace)
        result = namespace["add"](2, 3)
        state.tests_passed = result == 5
        message = "Test passed" if state.tests_passed else f"Test failed: add(2, 3)={result}"
    except Exception as exc:
        state.tests_passed = False
        message = f"Test exception: {type(exc).__name__}"
    
    state.log("tester", message)
    return state


def checkpoint_agent(state: WorkflowState, auto_approve: bool) -> WorkflowState:
    state.checkpoint_required = True
    
    if auto_approve:
        state.human_approved = True
        state.status = "done"
        state.log("checkpoint", "Checkpoint auto-approved, workflow finished")
    else:
        state.human_approved = False
        state.status = "waiting_for_human"
        state.log("checkpoint", "Waiting for human approval")
    
    return state

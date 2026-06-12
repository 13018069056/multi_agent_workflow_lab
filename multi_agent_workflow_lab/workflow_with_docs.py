import json
from pathlib import Path

from agents_with_docs import (
    checkpoint_agent, doc_agent, planner_agent,
    programmer_agent, reviewer_agent, tester_agent
)
from state import GoalContract, WorkflowState


def write_history(state: WorkflowState, path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(state.history, ensure_ascii=False, indent=2), encoding="utf-8")


def write_documentation(state: WorkflowState, path: str) -> None:
    doc_path = Path(path)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(state, 'documentation'):
        doc_path.write_text(state.documentation, encoding="utf-8")


def run_workflow_with_docs(
    goal: GoalContract,
    auto_approve: bool = True,
    log_path: str = None,
    doc_path: str = None,
    max_attempts: int = 3,
) -> WorkflowState:
    state = WorkflowState(goal=goal, max_attempts=max_attempts)
    state.log("start", goal.objective)
    
    state = planner_agent(state)
    
    while state.attempts < state.max_attempts:
        state = programmer_agent(state)
        state = reviewer_agent(state)
        
        if not state.review_passed:
            state.log("router", "审查未通过，返回 Programmer")
            continue
        
        state = tester_agent(state)
        if not state.tests_passed:
            state.log("router", "测试未通过，返回 Programmer")
            continue
        
        state = doc_agent(state)
        
        state = checkpoint_agent(state, auto_approve=auto_approve)
        if log_path is not None:
            write_history(state, log_path)
        if doc_path is not None:
            write_documentation(state, doc_path)
        return state
    
    state.status = "failed"
    state.log("router", "达到最大尝试次数，工作流失败")
    if log_path is not None:
        write_history(state, log_path)
    return state

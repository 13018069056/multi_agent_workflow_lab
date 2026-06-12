import json
from pathlib import Path

from agents_with_security import (
    checkpoint_agent, planner_agent, programmer_agent,
    reviewer_agent, security_reviewer_agent, tester_agent
)
from state import GoalContract, WorkflowState


def write_history(state: WorkflowState, path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(state.history, ensure_ascii=False, indent=2), encoding="utf-8")


def run_workflow_with_security(
    goal: GoalContract,
    auto_approve: bool = True,
    log_path: str = None,
    max_attempts: int = 3,
) -> WorkflowState:
    state = WorkflowState(goal=goal, max_attempts=max_attempts)
    state.security_passed = False
    state.log("start", goal.objective)
    
    state = planner_agent(state)
    
    while state.attempts < state.max_attempts:
        state = programmer_agent(state)
        state = reviewer_agent(state)
        
        if not state.review_passed:
            state.log("router", "Review failed, return to Programmer")
            continue
        
        state = security_reviewer_agent(state)
        if not state.security_passed:
            state.log("router", "Security review failed, return to Programmer")
            continue
        
        state = tester_agent(state)
        if not state.tests_passed:
            state.log("router", "Test failed, return to Programmer")
            continue
        
        state = checkpoint_agent(state, auto_approve=auto_approve)
        if log_path is not None:
            write_history(state, log_path)
        return state
    
    state.status = "failed"
    state.log("router", "Max attempts reached, workflow failed")
    if log_path is not None:
        write_history(state, log_path)
    return state

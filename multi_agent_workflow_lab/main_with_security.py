from state import GoalContract
from workflow_with_security import run_workflow_with_security


goal = GoalContract(
    objective="Implement add(a, b) function that returns sum of two numbers",
    success_criteria=["add(2, 3) == 5"],
    constraints=["No file access", "No network calls"],
    stop_conditions=["Test passed and security approved", "Max attempts reached"],
)

state = run_workflow_with_security(
    goal, 
    auto_approve=True, 
    log_path="outputs/history_with_security.json"
)

print("status:", state.status)
print("attempts:", state.attempts)
print("review_passed:", state.review_passed)
print("security_passed:", getattr(state, 'security_passed', 'N/A'))
print("tests_passed:", state.tests_passed)
print("human_approved:", state.human_approved)

if hasattr(state, 'security_feedback'):
    print("\nSecurity Review Feedback:", state.security_feedback)

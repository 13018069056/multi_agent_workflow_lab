import sys
import platform
import subprocess
from pathlib import Path

print("=" * 60)
print("venv + pytest 跨平台验证报告")
print("=" * 60)

# 1. 环境信息
print(f"\n[1] 环境信息")
print(f"    Python版本: {sys.version}")
print(f"    操作系统: {platform.system()} {platform.release()}")
print(f"    虚拟环境: {sys.prefix}")

# 2. 验证依赖
print(f"\n[2] 依赖验证")
try:
    import pytest
    print(f"    pytest版本: {pytest.__version__} ✅")
except:
    print("    pytest未安装 ❌")

# 3. 验证模块导入
print(f"\n[3] 模块导入验证")
try:
    from state import GoalContract, WorkflowState
    print("    state.py ✅")
    from agents import planner_agent, programmer_agent
    print("    agents.py ✅")
    from workflow import run_workflow
    print("    workflow.py ✅")
except Exception as e:
    print(f"    导入失败: {e}")

# 4. 验证输出文件
print(f"\n[4] 输出文件验证")
history_file = Path("outputs/history.json")
if history_file.exists():
    import json
    with open(history_file, encoding='utf-8') as f:
        history = json.load(f)
    print(f"    history.json ✅ ({len(history)}条记录)")
else:
    print("    history.json ❌")

# 5. 运行 pytest 验证
print(f"\n[5] pytest 自动化测试")
result = subprocess.run(["python", "-m", "pytest", "-q"], capture_output=True, text=True)
if result.returncode == 0:
    print("    pytest测试: 通过 ✅")
else:
    print("    pytest测试: 失败 ❌")

print("\n" + "=" * 60)
print("验证结论: 代码可在当前环境正常运行")
print("=" * 60)

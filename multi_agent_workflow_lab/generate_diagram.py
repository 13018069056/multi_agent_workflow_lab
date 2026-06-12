import json
import os
from pathlib import Path


def generate_mermaid_diagram(history_path: str, output_path: str = None) -> str:
    with open(history_path, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    nodes = []
    transitions = []
    prev_node = None
    
    for step in history:
        node = step['node']
        message = step['message']
        
        nodes.append(node)
        
        if prev_node is not None and prev_node != node:
            if '失败' in message or '未通过' in message:
                label = "失败"
            elif '通过' in message or '批准' in message:
                label = "成功"
            else:
                label = ""
            
            transitions.append({
                'from': prev_node,
                'to': node,
                'label': label
            })
        
        prev_node = node
    
    mermaid_lines = ["graph TD"]
    
    unique_nodes = list(dict.fromkeys(nodes))
    for node in unique_nodes:
        mermaid_lines.append(f"    {node}([{node}])")
    
    mermaid_lines.append("")
    
    for t in transitions:
        if t['label']:
            mermaid_lines.append(f"    {t['from']} -->|{t['label']}| {t['to']}")
        else:
            mermaid_lines.append(f"    {t['from']} --> {t['to']}")
    
    mermaid_code = "\n".join(mermaid_lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 状态转移图（Mermaid格式）\n\n")
            f.write("`mermaid\n")
            f.write(mermaid_code)
            f.write("\n`\n")
        
        html_path = Path(output_path).with_suffix('.html')
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>状态转移图</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>多 Agent 工作流状态转移图</h1>
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>'''
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Mermaid 图已保存到: {output_path}")
        print(f"HTML 可视化已保存到: {html_path}")
    
    return mermaid_code


def generate_ascii_diagram(history_path: str) -> str:
    with open(history_path, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    lines = []
    lines.append("+" + "-" * 70 + "+")
    lines.append("|" + " " * 25 + "状态转移序列图" + " " * 28 + "|")
    lines.append("+" + "-" * 70 + "+")
    
    for i, step in enumerate(history):
        node = step['node']
        msg = step['message']
        if len(msg) > 45:
            msg = msg[:42] + "..."
        
        lines.append(f"|  {i+1:2d}. {node:<12} | {msg:<45} |")
        
        if i < len(history) - 1:
            next_node = history[i+1]['node']
            if node != next_node:
                if '失败' in msg or '未通过' in msg:
                    lines.append("|       | 失败重试 ↓" + " " * 50 + "|")
                elif '通过' in msg:
                    lines.append("|       | 成功通过 ↓" + " " * 50 + "|")
                else:
                    lines.append("|       | 继续执行 ↓" + " " * 50 + "|")
    
    lines.append("+" + "-" * 70 + "+")
    
    return "\n".join(lines)


if __name__ == "__main__":
    history_file = "outputs/history.json"
    
    if os.path.exists(history_file):
        print("生成 Mermaid 状态转移图...")
        generate_mermaid_diagram(history_file, "outputs/state_diagram.md")
        
        print("\n生成 ASCII 状态转移图...")
        ascii_diagram = generate_ascii_diagram(history_file)
        print(ascii_diagram)
        
        with open("outputs/ascii_diagram.txt", "w", encoding="utf-8") as f:
            f.write(ascii_diagram)
        
        print("\n所有图表生成完成！")
        print("   - outputs/state_diagram.md (Mermaid格式)")
        print("   - outputs/state_diagram.html (可视化HTML)")
        print("   - outputs/ascii_diagram.txt (ASCII格式)")
    else:
        print(f"错误：找不到 {history_file}，请先运行 python main.py")

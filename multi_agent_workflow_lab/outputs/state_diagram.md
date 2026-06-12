# 状态转移图（Mermaid格式）

`mermaid
graph TD
    start([start])
    planner([planner])
    programmer([programmer])
    reviewer([reviewer])
    router([router])
    tester([tester])
    checkpoint([checkpoint])

    start --> planner
    planner --> programmer
    programmer --> reviewer
    reviewer -->|失败| router
    router --> programmer
    programmer --> reviewer
    reviewer -->|成功| tester
    tester -->|成功| checkpoint
`

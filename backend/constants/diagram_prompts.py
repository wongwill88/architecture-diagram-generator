from enum import Enum

class DiagramType(str, Enum):
    ARCHITECTURE = "architecture"
    SEQUENCE = "sequence"
    FLOWCHART = "flowchart"
    USECASE = "usecase"
    ER = "er"
    CLASS = "class"

DIAGRAM_PROMPTS = {
    DiagramType.ARCHITECTURE: """
    请根据以下系统描述生成一个架构图的Mermaid.js代码。
    # ... 保持原有的提示词内容 ...
    """,
    # ... 其他提示词保持不变 ...
} 
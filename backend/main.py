from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import asyncio
from dotenv import load_dotenv
import logging
import re
from enum import Enum

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiagramType(str, Enum):
    ARCHITECTURE = "architecture"
    SEQUENCE = "sequence"
    FLOWCHART = "flowchart"
    USECASE = "usecase"
    ER = "er"
    CLASS = "class"

class DiagramRequest(BaseModel):
    type: DiagramType
    description: str

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DIAGRAM_PROMPTS = {
    DiagramType.ARCHITECTURE: """
    请根据以下系统描述生成一个架构图的Mermaid.js代码。

    系统描述:
    {description}

    要求：
    1. 使用flowchart LR（从左到右）布局
    2. 使用以下语法：
       - 使用[方框]表示主要组件
       - 使用([圆角框])表示服务
       - 使用[(圆柱体)]表示数据库
       - 使用>六边形]表示外部系统
    3. 使用subgraph对相关组件进行分组
    4. 使用合适的连接线和说明文字

    示例：
    flowchart LR
        subgraph Frontend
            A[Web App]
        end
        subgraph Backend
            B([API Server])
            C[(Database)]
        end
        A -->|HTTP| B
        B -->|Query| C
    """,
    
    DiagramType.SEQUENCE: """
    请根据以下描述生成一个时序图的Mermaid.js代码。

    描述:
    {description}

    要求：
    1. 使用sequenceDiagram语法
    2. 清晰展示参与者之间的交互顺序
    3. 使用适当的箭头类型（->>, -->, -x）
    4. 添加必要的说明文字
    5. 使用activate/deactivate表示活动状态

    示例：
    sequenceDiagram
        participant U as User
        participant F as Frontend
        participant B as Backend
        
        U->>F: 点击登录
        F->>B: POST /login
        activate B
        B-->>F: 返回token
        deactivate B
        F-->>U: 显示成功消息
    """,
    
    DiagramType.FLOWCHART: """
    请根据以下描述生成一个流程图的Mermaid.js代码。

    描述:
    {description}

    要求：
    1. 使用flowchart TD（自上而下）布局
    2. 使用以下语法：
       - 使用[方框]表示普通步骤
       - 使用[[判断框]]表示判断
       - 使用([圆角框])表示开始/结束
       - 使用((圆形))表示连接点
    3. 使用清晰的箭头和文字说明
    4. 标注判断条件的是/否分支

    示例：
    flowchart TD
        A([开始]) --> B[输入用户名密码]
        B --> C[[验证是否通过]]
        C -->|是| D[进入系统]
        C -->|否| B
        D --> E([结束])
    """,
    
    DiagramType.USECASE: """
    请根据以下描述生成一个用例图的Mermaid.js代码。

    描述:
    {description}

    要求：
    1. 使用flowchart TD布局模拟用例图
    2. 使用以下语法：
       - ((圆形))表示用例
       - [方框]表示角色
    3. 使用适当的连接表示关系
    4. 根据需要使用subgraph分组

    示例：
    flowchart TD
        subgraph 系统边界
            A((登录))
            B((查询订单))
            C((修改订单))
        end
        U[用户] --> A
        U --> B
        U --> C
    """,
    
    DiagramType.ER: """
    请根据以下描述生成一个ER图的Mermaid.js代码。

    描述:
    {description}

    要求：
    1. 使用erDiagram语法
    2. 清晰展示实体之间的关系
    3. 标注关系的类型（一对一、一对多、多对多）
    4. 列出主要属性

    示例：
    erDiagram
        USER ||--o{ ORDER : places
        USER {
            string id
            string name
            string email
        }
        ORDER {
            string id
            date created_at
            float amount
        }
    """,
    
    DiagramType.CLASS: """
    请根据以下描述生成一个类图的Mermaid.js代码。

    描述:
    {description}

    要求：
    1. 使用classDiagram语法
    2. 包含类的属性和方法
    3. 标注访问修饰符
    4. 展示类之间的关系（继承、实现、关联等）

    示例：
    classDiagram
        class Animal {
            +String name
            +int age
            +makeSound()
        }
        class Dog {
            +String breed
            +bark()
        }
        Animal <|-- Dog
    """
}

@app.post("/generate-diagram")
async def generate_diagram(request: DiagramRequest):
    try:
        logger.info(f"Received request for {request.type} diagram")
        html = await generate_diagram_html(request.type, request.description)
        return {"html": html}
    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

async def generate_diagram_html(diagram_type: DiagramType, description: str):
    max_attempts = 3
    wait_seconds = 2
    
    for attempt in range(max_attempts):
        try:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                logger.error("DEEPSEEK_API_KEY not found in environment variables")
                raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
            
            logger.info(f"Making request to DeepSeek API (attempt {attempt + 1}/{max_attempts})...")
            
            # 获取对应类型的提示词模板
            prompt_template = DIAGRAM_PROMPTS.get(diagram_type)
            if not prompt_template:
                raise ValueError(f"Unsupported diagram type: {diagram_type}")
            
            # 填充提示词模板
            prompt = prompt_template.format(description=description)
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                logger.info("Sending request to DeepSeek API...")
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {
                                "role": "system", 
                                "content": "You are an expert at creating diagrams using Mermaid.js. Always generate clean, valid Mermaid.js code without any HTML tags or markdown formatting."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 4000
                    }
                )
                
                logger.info(f"DeepSeek API response status: {response.status_code}")
                
                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"API error: {response.status_code} {error_text}")
                    raise HTTPException(status_code=response.status_code, detail=error_text)
                
                data = response.json()
                logger.info("Successfully received response from DeepSeek API")
                mermaid_code = data["choices"][0]["message"]["content"]
                
                # 清理代码，移除可能的markdown代码块标记
                mermaid_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
                
                # 构建完整的HTML
                safe_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>
                        document.addEventListener('DOMContentLoaded', function() {
                            mermaid.initialize({
                                startOnLoad: true,
                                theme: 'default',
                                flowchart: {
                                    useMaxWidth: false,
                                    htmlLabels: true,
                                    curve: 'basis'
                                },
                                sequence: {
                                    showSequenceNumbers: true,
                                    boxMargin: 5
                                },
                                er: {
                                    layoutDirection: 'TB',
                                    entityPadding: 15
                                },
                                class: {
                                    useMaxWidth: false
                                }
                            });
                        });
                    </script>
                    <style>
                        .mermaid {
                            text-align: center;
                            padding: 20px;
                            background-color: white;
                        }
                        .mermaid svg {
                            max-width: 100%;
                            height: auto;
                        }
                    </style>
                </head>
                <body>
                    <div class="mermaid">
                    """ + mermaid_code + """
                    </div>
                </body>
                </html>
                """
                
                logger.info("Processed HTML content for diagram")
                return safe_html
                
        except Exception as e:
            logger.error(f"Error in generate_diagram_html (attempt {attempt + 1}/{max_attempts}): {str(e)}", exc_info=True)
            if attempt < max_attempts - 1:
                logger.info(f"Retrying in {wait_seconds} seconds...")
                await asyncio.sleep(wait_seconds)
            else:
                logger.error("Max retry attempts reached, giving up")
                raise

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
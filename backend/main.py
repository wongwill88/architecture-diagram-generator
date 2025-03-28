from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import asyncio
from dotenv import load_dotenv
import logging
import re

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagramRequest(BaseModel):
    description: str

# 确保路由定义正确
@app.post("/generate-diagram")
async def generate_diagram(request: DiagramRequest):
    try:
        logger.info(f"Received request with description: {request.description[:50]}...")
        html = await generate_diagram_html(request.description)
        return {"html": html}
    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# 添加一个别名路由，以防前端使用不同的路径
@app.post("/generate")
async def generate(request: DiagramRequest):
    return await generate_diagram(request)

async def generate_diagram_html(description: str):
    max_attempts = 3
    wait_seconds = 2
    
    for attempt in range(max_attempts):
        try:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                logger.error("DEEPSEEK_API_KEY not found in environment variables")
                raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
            
            logger.info(f"Making request to DeepSeek API (attempt {attempt + 1}/{max_attempts})...")
            
            prompt = """
            请根据以下系统架构描述，生成一个美观的架构图的HTML代码。
            使用mermaid.js语法，风格要简洁现代。

            系统架构描述:
            """ + description + """

            请只返回可以直接嵌入网页的HTML代码，包含完整的mermaid.js引用和图表定义。
            HTML代码应该包含以下元素:
            1. mermaid.js的CDN引用
            2. 一个带有'mermaid'类的div元素，其中包含图表定义
            3. 初始化mermaid的脚本

            示例格式:
            ```html
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
              mermaid.initialize({
                startOnLoad: true,
                theme: 'default'
              });
            </script>
            <div class="mermaid">
              graph TD
                A[前端] --> B[后端]
                B --> C[数据库]
            </div>
            ```

            不要包含任何解释或其他文本，只返回HTML代码。
            """
            
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
                            {"role": "system", "content": "You are a helpful assistant that generates architecture diagrams using mermaid.js."},
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
                html_content = data["choices"][0]["message"]["content"]
                
                # 清理HTML，确保它只包含必要的代码
                html_content = html_content.replace("```html", "").replace("```", "").strip()
                
                # 构建一个完整的、安全的HTML
                safe_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>
                        document.addEventListener('DOMContentLoaded', function() {
                            mermaid.initialize({
                                startOnLoad: true,
                                theme: 'default'
                            });
                        });
                    </script>
                </head>
                <body>
                """
                
                # 尝试提取mermaid图表定义
                import re
                mermaid_div = re.search(r'<div\s+class=["\']mermaid["\'][^>]*>(.*?)</div>', html_content, re.DOTALL)
                
                if mermaid_div:
                    # 如果找到了mermaid div，直接使用它
                    safe_html += mermaid_div.group(0)
                else:
                    # 否则尝试提取图表定义
                    graph_match = re.search(r'(graph\s+[A-Z]+.+|flowchart\s+[A-Z]+.+|sequenceDiagram.+|classDiagram.+)', html_content, re.DOTALL)
                    if graph_match:
                        graph_def = graph_match.group(0)
                        safe_html += '<div class="mermaid">\n' + graph_def + '\n</div>'
                    else:
                        # 如果无法提取，使用原始内容
                        safe_html += '<div class="mermaid">\n' + html_content + '\n</div>'
                
                safe_html += """
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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagramRequest(BaseModel):
    description: str

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def call_deepseek_api(prompt: str, api_key: str):
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        },
        timeout=60  # 增加超时时间到60秒
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"AI服务调用失败: {response.text}"
        )
    
    return response.json()

@app.post("/api/generate")
async def generate_diagram(request: DiagramRequest):
    try:
        # 构建提示词
        prompt = f"""请根据以下系统架构描述生成一个美观的HTML架构图。
        要求：
        1. 使用HTML和CSS创建一个清晰的架构图
        2. 符合微服务框架合理分层
        3. 使用合适的颜色和布局
        4. 包含组件之间的连接关系
        5. 使用响应式设计，确保在不同屏幕尺寸下都能正常显示
        
        系统架构描述：
        {request.description}
        
        请只返回HTML代码，不要包含任何其他文本。"""

        # 获取API密钥
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            logger.error("DEEPSEEK_API_KEY not found in environment variables")
            raise HTTPException(status_code=500, detail="API key not configured")

        logger.debug(f"Making request to DeepSeek API with prompt: {prompt}")
        
        # 调用DeepSeek API
        result = call_deepseek_api(prompt, api_key)
        html_content = result["choices"][0]["message"]["content"]
        
        return {"html": html_content}
            
    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
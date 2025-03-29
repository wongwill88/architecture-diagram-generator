from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import logging
import asyncio
from typing import Optional, List
import PyPDF2
import docx
import markdown
import re
import io

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置常量
MAX_RETRIES = 3
INITIAL_TIMEOUT = 120  # 初始超时时间（秒）
MAX_TIMEOUT = 180    # 最大超时时间（秒）

class DiagramRequest(BaseModel):
    description: str

class DocumentAnalysisRequest(BaseModel):
    content: str
    doc_type: str = "text"  # text, markdown, pdf, docx

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 文档分析提示词
DOCUMENT_ANALYSIS_PROMPT = '''
Analyze the following document content and extract system architecture information:

{content}

Please identify:
1. Main system components
2. Component relationships
3. Data flows
4. External integrations
5. Key technologies used

Format the response as a concise system description suitable for architecture diagram generation.
'''

ARCHITECTURE_PROMPT = '''
Generate a professional system architecture diagram in HTML with clear hierarchical structure. Output ONLY the diagram HTML code.

System Description:
{description}

Styling Guide:
1. Container Structure:
- Use nested flex containers for each layer
- Main container: flex-direction: column
- Layer containers: flex-direction: row
- Gap between layers: 60px
- Gap between components in same layer: 40px
- Minimum height: 500px
- System font stack
- Clean white background

2. Layer Styles:
- Each layer should have a distinct background color
- Layer labels: 16px, 600 weight, #2c3e50
- Layer padding: 20px
- Layer border-radius: 12px
- Layer margin-bottom: 20px

3. Component Styles:
- Minimum width: 160px
- Minimum height: 100px
- Padding: 20px
- Centered content
- Smooth transitions
- Subtle hover effects
- Box-shadow: 0 4px 6px rgba(0,0,0,0.1)

4. Layer-specific Colors:
Frontend Layer:
- Background: #F5F9FF
- Components:
  - Gradient: #E3F2FD to #BBDEFB
  - Border: #90CAF9
  - Rounded corners: 8px

Application Layer:
- Background: #F5FFF5
- Components:
  - Gradient: #E8F5E9 to #C8E6C9
  - Border: #81C784
  - Rounded corners: 12px

Data Layer:
- Background: #F5F5F5
- Components:
  - Gradient: #ECEFF1 to #CFD8DC
  - Border: #B0BEC5
  - Bottom shadow effect

External Layer:
- Background: #FFF5FF
- Components:
  - Gradient: #F3E5F5 to #E1BEE7
  - Border: #CE93D8
  - Hexagonal shape

5. Connection Styles:
- Use arrows (→) between components
- Arrow color: #78909C
- Arrow size: 24px
- Arrow spacing: 20px
- Vertical connections: ↓
- Diagonal connections: ↘ or ↙

6. Typography:
- Component titles: 14px, 600 weight
- Component descriptions: 12px, normal weight
- Layer labels: 16px, 600 weight
- Arrow symbols: 24px, light weight

7. Layout Rules:
- Components should be grouped by their layer
- Each layer should be clearly labeled
- Use arrows to show relationships between layers
- Maintain consistent spacing
- Ensure components are properly aligned
- Use appropriate arrow directions based on data flow

Generate a clean, single-line HTML with these styles applied as inline CSS. Include proper layer labels, component labels, and descriptions. Use arrows to show relationships between components and layers. No comments or additional text in the output.
'''

def extract_text_from_pdf(pdf_content: bytes) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to process PDF document")

def extract_text_from_docx(docx_content: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(docx_content))
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to process DOCX document")

def extract_text_from_markdown(md_content: str) -> str:
    try:
        # 移除Markdown语法，保留纯文本
        html = markdown.markdown(md_content)
        text = re.sub('<[^<]+?>', '', html)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from Markdown: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to process Markdown document")

async def analyze_document(content: str) -> str:
    try:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

        prompt = DOCUMENT_ANALYSIS_PROMPT.format(content=content)
        
        async with httpx.AsyncClient() as client:
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
                            "content": "You are a system architect specialized in analyzing documents and extracting architecture information."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=60
            )

            if response.status_code != 200:
                logger.error(f"API error during document analysis: {response.status_code} - {response.text}")
                return None

            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        return None

async def make_api_request(client: httpx.AsyncClient, api_key: str, prompt: str, timeout: float) -> Optional[str]:
    try:
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
                        "content": "You are an HTML architecture diagram generator. Output ONLY the HTML code for the diagram, without any explanation, comments, or markdown formatting. The output should be a single HTML string that can be directly injected into a webpage."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            timeout=timeout
        )
        
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
            
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return None

@app.post("/analyze-document")
async def process_document(request: DocumentAnalysisRequest):
    try:
        logger.info(f"Received document analysis request - Type: {request.doc_type}")
        
        # 根据文档类型提取文本
        if request.doc_type == "markdown":
            content = extract_text_from_markdown(request.content)
        else:  # 默认作为纯文本处理
            content = request.content
            
        # 分析文档内容
        analysis_result = await analyze_document(content)
        if not analysis_result:
            raise HTTPException(status_code=500, detail="Failed to analyze document")
            
        # 基于分析结果生成架构图
        diagram_request = DiagramRequest(description=analysis_result)
        return await generate_diagram(diagram_request)
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        logger.info(f"Received document upload: {file.filename}")
        
        content = await file.read()
        file_extension = file.filename.lower().split('.')[-1]
        
        # 根据文件类型提取文本
        if file_extension == 'pdf':
            text_content = extract_text_from_pdf(content)
        elif file_extension in ['docx', 'doc']:
            text_content = extract_text_from_docx(content)
        elif file_extension in ['md', 'markdown']:
            text_content = extract_text_from_markdown(content.decode())
        else:
            text_content = content.decode()
            
        # 分析文档并生成架构图
        analysis_request = DocumentAnalysisRequest(content=text_content, doc_type=file_extension)
        return await process_document(analysis_request)
        
    except Exception as e:
        logger.error(f"Error processing uploaded document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-diagram")
async def generate_diagram(request: DiagramRequest):
    try:
        logger.info("Received request for architecture diagram")
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        
        prompt = ARCHITECTURE_PROMPT.format(description=request.description)
        
        # 使用递增的超时时间重试
        timeout = INITIAL_TIMEOUT
        html_content = None
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Attempt {attempt + 1}/{MAX_RETRIES} with timeout {timeout}s")
                async with httpx.AsyncClient() as client:
                    html_content = await make_api_request(client, api_key, prompt, timeout)
                    if html_content:
                        break
                    
                # 如果失败，增加超时时间并等待后重试
                timeout = min(timeout * 1.5, MAX_TIMEOUT)
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error in attempt {attempt + 1}: {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2)
                else:
                    raise
        
        if not html_content:
            raise HTTPException(status_code=500, detail="Failed to generate diagram after multiple attempts")
            
        return {"html": html_content}
            
    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
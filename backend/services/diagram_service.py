import httpx
import logging
from typing import Optional
from config import settings
from constants.diagram_prompts import DiagramType, DIAGRAM_PROMPTS

logger = logging.getLogger(__name__)

class DiagramService:
    @staticmethod
    async def generate_mermaid_code(diagram_type: DiagramType, description: str) -> str:
        prompt_template = DIAGRAM_PROMPTS.get(diagram_type)
        if not prompt_template:
            raise ValueError(f"Unsupported diagram type: {diagram_type}")
        
        prompt = prompt_template.format(description=description)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                settings.api_url,
                headers={
                    "Authorization": f"Bearer {settings.deepseek_api_key}",
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
            
            if response.status_code != 200:
                raise httpx.HTTPError(f"API error: {response.status_code} {response.text}")
            
            data = response.json()
            mermaid_code = data["choices"][0]["message"]["content"]
            return mermaid_code.replace("```mermaid", "").replace("```", "").strip()

    @staticmethod
    def generate_html(mermaid_code: str) -> str:
        return """
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
                        flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'basis' },
                        sequence: { showSequenceNumbers: true, boxMargin: 5 },
                        er: { layoutDirection: 'TB', entityPadding: 15 },
                        class: { useMaxWidth: false }
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
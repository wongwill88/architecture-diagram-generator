from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    deepseek_api_key: str
    max_retries: int = 3
    retry_wait_seconds: int = 2
    api_url: str = "https://api.deepseek.com/v1/chat/completions"
    
    class Config:
        env_file = ".env"

settings = Settings() 
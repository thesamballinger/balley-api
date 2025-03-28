import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App settings
    app_name: str = "AI-Powered Payroll API"
    
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_model: str = os.getenv("DEFAULT_MODEL", "gpt-4o")
    openai_fine_tuned_model: str = os.getenv("OPENAI_FINE_TUNED_MODEL", "")
    
    # Check API settings
    check_api_url: str = os.getenv("CHECK_API_URL", "https://api.checkhq.com/v1")
    check_api_key: str = os.getenv("CHECK_API_KEY", "")
    check_company_id: str = os.getenv("CHECK_COMPANY_ID", "")
    
    # CORS settings
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://your-production-frontend.com"
    ]
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra fields in the settings

@lru_cache()
def get_settings():
    return Settings()
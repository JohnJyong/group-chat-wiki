import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_ID = os.getenv("APP_ID", "")
    APP_SECRET = os.getenv("APP_SECRET", "")
    VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN", "")
    ENCRYPT_KEY = os.getenv("ENCRYPT_KEY", "")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    PORT = int(os.getenv("PORT", 3000))

config = Config()

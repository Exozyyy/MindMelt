import os
from typing import Optional
from env import CONFIG, validate_config

class Settings:
    """Application settings"""
    
    def __init__(self):
        # Validate configuration on initialization
        validate_config()
        
        # Gemini Configuration
        self.GEMINI_API_KEY = CONFIG["gemini"]["api_key"]
        self.GEMINI_MODEL = CONFIG["gemini"]["model"]
        self.GEMINI_MAX_TOKENS = CONFIG["gemini"]["max_tokens"]
        self.GEMINI_TEMPERATURE = CONFIG["gemini"]["temperature"]
        
        # API Configuration
        self.API_TITLE = CONFIG["api"]["title"]
        self.API_DESCRIPTION = CONFIG["api"]["description"]
        self.API_VERSION = CONFIG["api"]["version"]
        self.MAX_BATCH_SIZE = CONFIG["api"]["max_batch_size"]
        
        # Server Configuration
        self.HOST = CONFIG["server"]["host"]
        self.PORT = CONFIG["server"]["port"]
        
        # Logging Configuration
        self.LOG_LEVEL = CONFIG["logging"]["level"]
        
        # CORS Configuration
        self.ALLOWED_ORIGINS = CONFIG["cors"]["allowed_origins"]
    
    def validate_gemini_config(self) -> bool:
        """Validate Gemini configuration"""
        return (self.GEMINI_API_KEY is not None and 
            len(self.GEMINI_API_KEY) > 0 and 
            self.GEMINI_API_KEY != "your_gemini_api_key_here")

settings = Settings()

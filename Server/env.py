"""
Environment configuration for FastAPI GPT Service
Set these environment variables or modify the default values below
"""

import os

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBE8ZVaNPX8ZyX86zSKvMFLh5GMVBuKXYE")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
GEMINI_MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "1500"))
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

# API Configuration
API_TITLE = "GPT Topic Explanation Service"
API_DESCRIPTION = "A service that generates explanations and test cases for given topics using GPT"
API_VERSION = "1.0.0"

# Rate Limiting
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "10"))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

def validate_config():
    """Validate required configuration"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY must be set")
    
    if GEMINI_MAX_TOKENS < 100 or GEMINI_MAX_TOKENS > 8000:
        raise ValueError("GEMINI_MAX_TOKENS must be between 100 and 8000")
    
    if GEMINI_TEMPERATURE < 0 or GEMINI_TEMPERATURE > 2:
        raise ValueError("GEMINI_TEMPERATURE must be between 0 and 2")
    
    return True

# Configuration dictionary for easy access
CONFIG = {
    "gemini": {
        "api_key": GEMINI_API_KEY,
        "model": GEMINI_MODEL,
        "max_tokens": GEMINI_MAX_TOKENS,
        "temperature": GEMINI_TEMPERATURE
    },
    "api": {
        "title": API_TITLE,
        "description": API_DESCRIPTION,
        "version": API_VERSION,
        "max_batch_size": MAX_BATCH_SIZE
    },
    "server": {
        "host": HOST,
        "port": PORT
    },
    "logging": {
        "level": LOG_LEVEL
    },
    "cors": {
        "allowed_origins": ALLOWED_ORIGINS
    }
}

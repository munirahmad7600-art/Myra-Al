# config/settings.py
import os
from pathlib import Path

class Config:
    """Central configuration for Myra"""
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = Path.home() / ".myra"
    DATA_DIR.mkdir(exist_ok=True)
    
    LOG_DIR = DATA_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)
    
    DB_PATH = DATA_DIR / "myra.db"
    CACHE_DIR = DATA_DIR / "cache"
    CACHE_DIR.mkdir(exist_ok=True)
    
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-1.5-flash-latest"
    
    # Termux & Android
    TERMUX_API_ENABLED = True
    USE_TERMUX_TTS = True
    USE_TERMUX_STT = True
    
    # Service Configuration
    SERVICE_PORT = 5555
    SERVICE_HOST = "127.0.0.1"
    SERVICE_POLLING_INTERVAL = 2  # seconds
    
    # TTS Configuration
    TTS_SPEED = 1.0  # 0.5-2.0
    TTS_PITCH = 1.0  # 0.5-2.0
    TTS_LANGUAGE = "en-IN"  # Change to ur, hi as needed
    
    # Notification Listener
    NOTIFICATION_CHECK_INTERVAL = 1  # seconds
    NOTIFICATION_KEYWORDS = ["whatsapp", "telegram", "sms", "message", "call"]
    
    # Floating UI
    FLOATING_UI_ENABLED = True
    FLOATING_UI_SIZE = 60  # pixels
    FLOATING_UI_OPACITY = 0.8
    
    # Debug
    DEBUG = True
    LOG_LEVEL = "INFO"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True

config = Config()

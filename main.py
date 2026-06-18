#!/usr/bin/env python3
# main.py
"""
Myra - Intelligent Android Assistant
Phase 1: Background Service with Notification Monitoring
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.service import MyraService, logger

def setup_environment():
    """Setup environment variables and directories"""
    # Load .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).parent / ".env")
    except ImportError:
        pass
    
    # Create necessary directories
    from config.settings import config
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Environment setup complete. Data directory: {config.DATA_DIR}")

def main():
    """Main entry point"""
    setup_environment()
    
    logger.info("=" * 60)
    logger.info("🤖 MYRA - Intelligent Android Assistant")
    logger.info("Phase 1: Background Service with Notification Monitoring")
    logger.info("=" * 60)
    
    try:
        service = MyraService()
        service.run()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

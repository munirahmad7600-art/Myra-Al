# core/termux_utils.py
import subprocess
import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class TermuxAPI:
    """Wrapper for Termux API calls"""
    
    @staticmethod
    def execute(command: str, *args) -> str:
        """Execute a termux command"""
        try:
            full_cmd = f"termux-{command} {' '.join(args)}"
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error(f"Termux command failed: {result.stderr}")
                return ""
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Error executing termux command: {e}")
            return ""
    
    @staticmethod
    def speak(text: str, speed: float = 1.0, pitch: float = 1.0, language: str = "en-IN") -> bool:
        """Text-to-Speech using Termux"""
        try:
            cmd = f"termux-tts-speak -l {language} -r {speed} -p {pitch} '{text}'"
            subprocess.run(cmd, shell=True, timeout=30)
            return True
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return False
    
    @staticmethod
    def get_notifications() -> str:
        """Get active notifications (requires accessibility service)"""
        try:
            result = subprocess.run("dumpsys notification", shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Error getting notifications: {e}")
            return ""
    
    @staticmethod
    def get_call_logs(limit: int = 10) -> list:
        """Get recent call logs"""
        try:
            # Note: Requires proper permissions
            result = subprocess.run(
                f"content query --uri content://call_log/calls --limit {limit}",
                shell=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip().split('\n')
        except Exception as e:
            logger.error(f"Error getting call logs: {e}")
            return []
    
    @staticmethod
    def vibrate(duration_ms: int = 200) -> bool:
        """Trigger vibration"""
        try:
            subprocess.run(f"termux-vibrate -d {duration_ms}", shell=True, timeout=5)
            return True
        except Exception as e:
            logger.error(f"Vibration error: {e}")
            return False
    
    @staticmethod
    def get_sensor_data(sensor: str = "accelerometer") -> Optional[Dict[str, Any]]:
        """Get sensor data (accelerometer, gyroscope, etc.)"""
        try:
            result = subprocess.run(
                f"termux-sensor -s {sensor} -n 1",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Error getting sensor data: {e}")
            return None

class NotificationParser:
    """Parse and extract notification data"""
    
    @staticmethod
    def parse_notification(notification_string: str) -> Dict[str, str]:
        """Parse a notification string and extract key info"""
        parsed = {
            "package": "",
            "title": "",
            "text": "",
            "subtext": "",
            "timestamp": "",
        }
        
        lines = notification_string.split('\n')
        for line in lines:
            line = line.strip()
            if "package=" in line:
                parsed["package"] = line.split("package=")[1].split()[0]
            elif "title=" in line:
                parsed["title"] = line.split("title=")[1].strip("'\"")
            elif "text=" in line:
                parsed["text"] = line.split("text=")[1].strip("'\"")
            elif "subtext=" in line:
                parsed["subtext"] = line.split("subtext=")[1].strip("'\"")
        
        return parsed

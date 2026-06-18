# core/floating_ui.py
import logging
import subprocess
from typing import Optional
from config.settings import config

logger = logging.getLogger(__name__)

class FloatingUI:
    """Manages persistent floating UI indicator"""
    
    def __init__(self):
        self.notification_id = 42069  # Unique ID for persistent notification
        self.is_active = False
        self.status = "idle"
    
    def show(self, title: str = "Myra", status: str = "listening") -> bool:
        """Show floating notification (persistent)"""
        try:
            self.status = status
            self.is_active = True
            
            # Use Android's persistent notification
            # This creates a foreground service notification
            self._update_notification(title, status)
            logger.info(f"Floating UI shown: {status}")
            return True
        
        except Exception as e:
            logger.error(f"Error showing floating UI: {e}")
            return False
    
    def update_status(self, status: str, title: str = "Myra") -> None:
        """Update floating UI status"""
        self.status = status
        self._update_notification(title, status)
    
    def hide(self) -> bool:
        """Hide floating notification"""
        try:
            self._remove_notification()
            self.is_active = False
            logger.info("Floating UI hidden")
            return True
        except Exception as e:
            logger.error(f"Error hiding floating UI: {e}")
            return False
    
    def _update_notification(self, title: str, status: str) -> None:
        """Update the persistent notification"""
        # Using termux-notification for persistent display
        description = f"Status: {status} | {self._get_timestamp()}"
        
        cmd = (
            f"termux-notification "
            f"--id {self.notification_id} "
            f"--title '{title}' "
            f"--content '{description}' "
            f"--priority high "
            f"--ongoing "
            f"--color '#4CAF50'"
        )
        
        try:
            subprocess.run(cmd, shell=True, timeout=5)
        except Exception as e:
            logger.warning(f"Notification update failed: {e}")
    
    def _remove_notification(self) -> None:
        """Remove the persistent notification"""
        cmd = f"termux-notification-remove {self.notification_id}"
        try:
            subprocess.run(cmd, shell=True, timeout=5)
        except Exception as e:
            logger.warning(f"Notification removal failed: {e}")
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current time for display"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M")

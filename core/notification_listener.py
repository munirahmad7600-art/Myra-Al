# core/notification_listener.py
import threading
import time
import logging
from datetime import datetime
from typing import Callable, Optional, Dict, List
from collections import defaultdict
from config.settings import config
from core.termux_utils import TermuxAPI, NotificationParser

logger = logging.getLogger(__name__)

class NotificationListener:
    """Monitors system notifications and triggers callbacks"""
    
    def __init__(self):
        self.running = False
        self.listener_thread: Optional[threading.Thread] = None
        self.callbacks: Dict[str, List[Callable]] = defaultdict(list)
        self.notification_history: Dict[str, Dict] = {}
        self.seen_notifications = set()
        self.lock = threading.Lock()
    
    def register_callback(self, event_type: str, callback: Callable) -> None:
        """Register a callback for specific notification type
        
        Args:
            event_type: 'message', 'call', 'app_notification'
            callback: function to call with notification data
        """
        with self.lock:
            self.callbacks[event_type].append(callback)
            logger.info(f"Registered callback for {event_type}: {callback.__name__}")
    
    def start(self) -> None:
        """Start the notification listener"""
        if self.running:
            logger.warning("Listener already running")
            return
        
        self.running = True
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()
        logger.info("Notification listener started")
    
    def stop(self) -> None:
        """Stop the notification listener"""
        self.running = False
        if self.listener_thread:
            self.listener_thread.join(timeout=5)
        logger.info("Notification listener stopped")
    
    def _listen_loop(self) -> None:
        """Main listening loop"""
        while self.running:
            try:
                self._check_notifications()
                time.sleep(config.NOTIFICATION_CHECK_INTERVAL)
            except Exception as e:
                logger.error(f"Error in notification loop: {e}")
                time.sleep(1)
    
    def _check_notifications(self) -> None:
        """Check for new notifications"""
        notifications_raw = TermuxAPI.get_notifications()
        
        if not notifications_raw:
            return
        
        notification_blocks = self._parse_notification_dump(notifications_raw)
        
        for notif in notification_blocks:
            notif_id = notif.get("id", "")
            
            # Avoid duplicate processing
            if notif_id in self.seen_notifications:
                continue
            
            self.seen_notifications.add(notif_id)
            self._process_notification(notif)
    
    def _parse_notification_dump(self, dump: str) -> List[Dict]:
        """Parse dumpsys notification output"""
        notifications = []
        
        # Simple parser - adapt based on actual dumpsys output
        for line in dump.split('\n'):
            if 'notification' in line.lower() or 'key=' in line:
                # Extract notification data
                notif_data = NotificationParser.parse_notification(line)
                if notif_data.get("text") or notif_data.get("title"):
                    notif_data["id"] = f"{notif_data.get('package')}_{hash(line) % 10000}"
                    notif_data["timestamp"] = datetime.now().isoformat()
                    notifications.append(notif_data)
        
        return notifications
    
    def _process_notification(self, notification: Dict) -> None:
        """Process and categorize notification"""
        package = notification.get("package", "").lower()
        text = notification.get("text", "").lower()
        title = notification.get("title", "").lower()
        
        # Store in history
        with self.lock:
            self.notification_history[notification["id"]] = notification
        
        # Determine notification type and trigger callbacks
        event_type = self._categorize_notification(package, text, title)
        
        if event_type:
            logger.info(f"New {event_type}: {title} - {text}")
            self._trigger_callbacks(event_type, notification)
    
    def _categorize_notification(self, package: str, text: str, title: str) -> Optional[str]:
        """Categorize notification into event type"""
        
        # Message apps
        if any(app in package for app in ['whatsapp', 'telegram', 'messenger', 'sms']):
            return 'message'
        
        # Call apps
        if any(app in package for app in ['phone', 'dialer', 'call', 'skype']):
            return 'call'
        
        # Default to app notification
        return 'app_notification'
    
    def _trigger_callbacks(self, event_type: str, notification: Dict) -> None:
        """Trigger registered callbacks for event type"""
        with self.lock:
            callbacks = self.callbacks.get(event_type, [])
        
        for callback in callbacks:
            try:
                # Run callback in separate thread to avoid blocking
                threading.Thread(
                    target=callback,
                    args=(notification,),
                    daemon=True
                ).start()
            except Exception as e:
                logger.error(f"Error in callback {callback.__name__}: {e}")
    
    def get_recent_notifications(self, limit: int = 5) -> List[Dict]:
        """Get recent notifications"""
        with self.lock:
            recent = sorted(
                self.notification_history.values(),
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )[:limit]
        return recent

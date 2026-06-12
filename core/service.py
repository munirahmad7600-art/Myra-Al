# core/service.py
import logging
import sys
import signal
from typing import Optional
from pathlib import Path
from config.settings import config
from core.notification_listener import NotificationListener
from core.voice_controller import VoiceController
from core.floating_ui import FloatingUI

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_DIR / "myra.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MyraService:
    """Main Myra background service"""
    
    def __init__(self):
        self.running = False
        self.notification_listener: Optional[NotificationListener] = None
        self.voice_controller: Optional[VoiceController] = None
        self.floating_ui: Optional[FloatingUI] = None
        
        # Validate configuration
        try:
            config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
    
    def initialize(self) -> bool:
        """Initialize all components"""
        try:
            logger.info("Initializing Myra service...")
            
            # Initialize components
            self.notification_listener = NotificationListener()
            self.voice_controller = VoiceController()
            self.floating_ui = FloatingUI()
            
            # Register callbacks
            self.notification_listener.register_callback('message', self._handle_message)
            self.notification_listener.register_callback('call', self._handle_call)
            self.notification_listener.register_callback('app_notification', self._handle_app_notification)
            
            # Set voice callbacks for UI updates
            if self.floating_ui:
                self.voice_controller.set_voice_callbacks(
                    on_start=lambda _: self.floating_ui.update_status("speaking"),
                    on_end=lambda: self.floating_ui.update_status("listening")
                )
            
            logger.info("✅ Myra service initialized successfully")
            return True
        
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            return False
    
    def start(self) -> bool:
        """Start the service"""
        if self.running:
            logger.warning("Service already running")
            return False
        
        try:
            logger.info("Starting Myra service...")
            
            # Start components
            if self.notification_listener:
                self.notification_listener.start()
            
            if self.voice_controller:
                self.voice_controller.start()
            
            if self.floating_ui:
                self.floating_ui.show(status="initialized")
            
            self.running = True
            
            # Greeting
            if self.voice_controller:
                self.voice_controller.speak("Myra is now active. Listening for notifications.")
            
            logger.info("✅ Myra service started")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to start service: {e}")
            return False
    
    def stop(self) -> None:
        """Stop the service"""
        if not self.running:
            return
        
        logger.info("Stopping Myra service...")
        
        self.running = False
        
        if self.notification_listener:
            self.notification_listener.stop()
        
        if self.voice_controller:
            self.voice_controller.stop()
        
        if self.floating_ui:
            self.floating_ui.hide()
        
        logger.info("✅ Myra service stopped")
    
    def _handle_message(self, notification: dict) -> None:
        """Handle incoming message notification"""
        try:
            title = notification.get("title", "Someone")
            text = notification.get("text", "")
            
            logger.info(f"📨 Message from {title}: {text[:50]}...")
            
            if self.floating_ui:
                self.floating_ui.update_status(f"📨 Message: {title}")
            
            if self.voice_controller:
                self.voice_controller.announce_notification(notification)
            
            # TODO: In Phase 2, prompt for voice reply
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def _handle_call(self, notification: dict) -> None:
        """Handle incoming call notification"""
        try:
            caller = notification.get("title", "Unknown")
            
            logger.info(f"☎️ Incoming call from {caller}")
            
            if self.floating_ui:
                self.floating_ui.update_status(f"☎️ Call: {caller}")
            
            if self.voice_controller:
                self.voice_controller.speak(f"Incoming call from {caller}")
            
            # TODO: In Phase 3, handle voice commands (accept/reject)
        
        except Exception as e:
            logger.error(f"Error handling call: {e}")
    
    def _handle_app_notification(self, notification: dict) -> None:
        """Handle general app notification"""
        try:
            logger.debug(f"🔔 App notification: {notification.get('title')}")
            
            # Optional: Only speak for high-priority notifications
            # if 'priority' in notification.get('flags', ''):
            #     self.voice_controller.announce_notification(notification)
        
        except Exception as e:
            logger.error(f"Error handling app notification: {e}")
    
    def run(self) -> None:
        """Run the service in foreground (blocking)"""
        if not self.initialize():
            return
        
        if not self.start():
            return
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}, shutting down...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            logger.info("✅ Myra is running. Press Ctrl+C to stop.")
            # Keep service running
            import time
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()


def main():
    """Entry point for Phase 1"""
    service = MyraService()
    service.run()


if __name__ == "__main__":
    main()

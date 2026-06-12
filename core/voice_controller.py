# core/voice_controller.py
import logging
import threading
from typing import Callable, Optional
from core.termux_utils import TermuxAPI
from config.settings import config

logger = logging.getLogger(__name__)

class VoiceController:
    """Handles text-to-speech and voice announcements"""
    
    def __init__(self):
        self.tts_queue: list = []
        self.is_speaking = False
        self.speaker_thread: Optional[threading.Thread] = None
        self.running = False
        self.on_speak_start: Optional[Callable] = None
        self.on_speak_end: Optional[Callable] = None
    
    def start(self) -> None:
        """Start the voice controller"""
        if self.running:
            return
        
        self.running = True
        self.speaker_thread = threading.Thread(target=self._speaker_loop, daemon=True)
        self.speaker_thread.start()
        logger.info("Voice controller started")
    
    def stop(self) -> None:
        """Stop the voice controller"""
        self.running = False
        if self.speaker_thread:
            self.speaker_thread.join(timeout=5)
        logger.info("Voice controller stopped")
    
    def speak(self, text: str, speed: Optional[float] = None, language: Optional[str] = None) -> None:
        """Queue text for speaking
        
        Args:
            text: Text to speak
            speed: Speech speed (0.5-2.0), defaults to config.TTS_SPEED
            language: Language code (en-IN, ur, etc.), defaults to config.TTS_LANGUAGE
        """
        speed = speed or config.TTS_SPEED
        language = language or config.TTS_LANGUAGE
        
        self.tts_queue.append({
            "text": text,
            "speed": speed,
            "language": language
        })
        logger.debug(f"Queued speech: {text[:50]}...")
    
    def announce_notification(self, notification: dict) -> None:
        """Announce a notification to user"""
        package = notification.get("package", "").replace("com.", "")
        title = notification.get("title", "Notification")
        text = notification.get("text", "")
        
        announcement = f"You have a message from {title}"
        if text and len(text) < 100:
            announcement += f": {text}"
        
        self.speak(announcement)
    
    def _speaker_loop(self) -> None:
        """Process queued speech in background"""
        import time
        
        while self.running:
            if self.tts_queue and not self.is_speaking:
                speech_data = self.tts_queue.pop(0)
                self._execute_tts(speech_data)
            else:
                time.sleep(0.5)
    
    def _execute_tts(self, speech_data: dict) -> None:
        """Execute TTS for a single item"""
        self.is_speaking = True
        
        if self.on_speak_start:
            self.on_speak_start(speech_data["text"])
        
        try:
            success = TermuxAPI.speak(
                text=speech_data["text"],
                speed=speech_data["speed"],
                language=speech_data["language"]
            )
            
            if success:
                logger.info(f"Spoke: {speech_data['text'][:50]}...")
            else:
                logger.warning(f"TTS failed for: {speech_data['text'][:50]}...")
        
        except Exception as e:
            logger.error(f"TTS error: {e}")
        
        finally:
            self.is_speaking = False
            if self.on_speak_end:
                self.on_speak_end()
    
    def interrupt(self) -> None:
        """Clear the speech queue and stop current speech"""
        self.tts_queue.clear()
        logger.info("Speech queue cleared")
    
    def set_voice_callbacks(self, on_start: Optional[Callable] = None, on_end: Optional[Callable] = None) -> None:
        """Set callbacks for speech start/end"""
        self.on_speak_start = on_start
        self.on_speak_end = on_end

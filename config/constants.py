# config/constants.py
"""Constants for Myra"""

# App packages
MESSAGING_APPS = [
    'com.whatsapp',
    'com.whatsapp.w4b',
    'org.telegram.messenger',
    'com.facebook.orca',
    'com.android.messaging',
]

CALL_APPS = [
    'com.android.phone',
    'com.android.dialer',
    'com.skype.raider',
]

# Event types
EVENT_MESSAGE = 'message'
EVENT_CALL = 'call'
EVENT_APP_NOTIFICATION = 'app_notification'

# Notification keywords
MESSAGE_KEYWORDS = ['whatsapp', 'telegram', 'sms', 'message', 'chat']
CALL_KEYWORDS = ['call', 'incoming', 'dialing']

# Timeouts (seconds)
TTS_TIMEOUT = 30
STT_TIMEOUT = 10
API_TIMEOUT = 10

# UI Status
STATUS_IDLE = 'idle'
STATUS_LISTENING = 'listening'
STATUS_SPEAKING = 'speaking'
STATUS_PROCESSING = 'processing'
STATUS_ERROR = 'error'

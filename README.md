# 🎯 Myra AI - Advanced Android System Controller

**Myra** is a comprehensive, background-running AI assistant for Android (via Termux) that combines intelligent notification handling, voice commands, system control, and self-evolving capabilities.

## 📋 Project Overview

Myra operates as a full-scale system controller with the following capabilities:

- **Background Service**: Persistent daemon process with floating UI indicator
- **Intelligent Notifications**: Read, announce, and reply to messages (WhatsApp, SMS, etc.)
- **Call Management**: Monitor and handle incoming calls with voice commands
- **System & App Control**: Voice-activated app launching, phone calls, and system operations
- **Advanced Voice**: High-quality TTS with casual Urdu conversation mode ("Ghupshup")
- **Self-Evolution**: Learns usage patterns and suggests optimizations
- **AI Integration**: Powered by Google Gemini 1.5 Flash API

## 🗺️ Development Roadmap

### **Phase 1: Background Service & Voice Monitoring (Week 1)**
- ✅ Setup persistent background service architecture
- ✅ Basic voice notification listener
- ✅ Audio capture and STT (Speech-to-Text)
- ✅ TTS engine initialization
- ✅ Termux API integration
- 📁 Output: Core service framework with basic notification monitoring

### **Phase 2: Intelligent Notification Handling (Week 2)**
- Notification listener enhancement
- Message parsing and context extraction
- Automated announcement system
- Voice reply prompt & capture
- Gemini integration for context-aware responses
- 📁 Output: Full notification read-reply pipeline

### **Phase 3: System & Call Management (Week 3)**
- Call detection and caller ID announcement
- Voice command parser for call acceptance/rejection
- App launcher module with voice activation
- Phone dialer integration
- Gesture recognition for UI interaction
- 📁 Output: Full system control capabilities

### **Phase 4: Weather, Personality & Ghupshup Mode (Week 4)**
- Weather API integration (OpenWeatherMap)
- TTS voice personalization
- Urdu language support with casual conversation
- Context-aware response generation
- Personality profiles
- 📁 Output: Enhanced assistant with personality

### **Phase 5: Self-Evolution & Optimization (Week 5)**
- Usage pattern logging & analytics
- Feature suggestion engine
- Performance optimization monitoring
- Adaptive learning from user interactions
- Auto-update mechanism
- 📁 Output: Production-ready self-evolving assistant

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.13 |
| **Environment** | Termux on Android |
| **AI Engine** | Google Gemini 1.5 Flash |
| **Speech-to-Text** | Google Cloud STT / pydub |
| **Text-to-Speech** | Android TTS (via Termux) / pyttsx3 |
| **Accessibility** | Android Accessibility Services |
| **System API** | Termux API (`termux-api` commands) |
| **Database** | SQLite3 (usage logs & config) |
| **Architecture** | Modular, async-first design |

## 📁 Directory Structure

```
Myra-Al/
├── README.md                      # This file
├── ROADMAP.md                     # Detailed phase-by-phase roadmap
├── ARCHITECTURE.md                # System architecture documentation
│
├── config/
│   ├── settings.json              # Configuration & constants
│   └── api_keys.example.json      # API key template
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Entry point (Phase 1)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── background_service.py  # Service manager (Phase 1)
│   │   ├── event_loop.py          # Async event handler (Phase 1)
│   │   └── logger.py              # Logging system (Phase 1)
│   │
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── stt.py                 # Speech-to-Text (Phase 1)
│   │   ├── tts.py                 # Text-to-Speech (Phase 1)
│   │   └── audio_processor.py     # Audio capture & processing (Phase 1)
│   │
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── listener.py            # Notification listener (Phase 1)
│   │   ├── parser.py              # Message parsing (Phase 2)
│   │   └── responder.py           # Auto-reply logic (Phase 2)
│   │
│   ├── system/
│   │   ├── __init__.py
│   │   ├── termux_api.py          # Termux API wrapper (Phase 1)
│   │   ├── app_control.py         # App launching (Phase 3)
│   │   ├── call_handler.py        # Call management (Phase 3)
│   │   └── ui_overlay.py          # Floating UI (Phase 1)
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── gemini_client.py       # Gemini API integration (Phase 2)
│   │   ├── context_manager.py     # Conversation context (Phase 2)
│   │   └── personality.py         # Personality modes (Phase 4)
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config_manager.py      # Config loader
│       ├── database.py            # SQLite wrapper
│       ├── scheduler.py           # Task scheduling
│       └── validators.py          # Input validation
│
├── tests/
│   ├── test_voice.py
│   ├── test_notifications.py
│   └── test_integration.py
│
├── scripts/
│   ├── setup.sh                   # Installation script
│   ├── install_dependencies.sh    # Pip dependencies
│   └── run.sh                     # Start Myra
│
├── data/
│   ├── usage_logs.db              # SQLite database (auto-created)
│   └── config.json                # Runtime config (auto-created)
│
└── requirements.txt               # Python dependencies

```

## 🚀 Quick Start (Phase 1)

### Prerequisites
```bash
# On Termux
apt install termux-api python3.13 python3-pip
apt install pulseaudio ffmpeg sox
```

### Installation
```bash
cd Myra-Al
pip install -r requirements.txt
bash scripts/setup.sh
```

### Run Phase 1
```bash
python src/main.py --phase 1
```

## 📝 Phase 1: Detailed Goals

### Core Deliverables
1. **Background Service Manager** (`background_service.py`)
   - Daemon process initialization
   - PID management
   - Process lifecycle hooks

2. **Voice Monitoring System** (`voice/stt.py`, `audio_processor.py`)
   - Real-time audio capture from microphone
   - Audio format conversion (WAV → proper codec)
   - Speech-to-text conversion (Google STT or local Vosk)

3. **TTS Engine** (`voice/tts.py`)
   - Text-to-speech synthesis
   - Termux audio output integration
   - Voice queue management

4. **Basic Notification Listener** (`notifications/listener.py`)
   - Hook into Android notification stream
   - Event-driven notification capture
   - Message logging to database

5. **Termux API Integration** (`system/termux_api.py`)
   - Command execution wrapper
   - Sensor access (microphone, speaker)
   - System permissions handling

6. **Event Loop & Logging** (`core/event_loop.py`, `core/logger.py`)
   - Async event processing
   - Comprehensive logging to file & console
   - Error recovery mechanisms

## 🔑 API Keys Required

Create `config/api_keys.json`:
```json
{
  "gemini_api_key": "YOUR_GOOGLE_GEMINI_KEY",
  "openweather_api_key": "YOUR_OPENWEATHER_KEY",
  "google_cloud_stt_credentials": "/path/to/google_credentials.json"
}
```

## 📚 Documentation

- **[ROADMAP.md](ROADMAP.md)** - Detailed phase breakdown
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & data flow
- **[PHASE1_GUIDE.md](docs/PHASE1_GUIDE.md)** - Phase 1 implementation guide

## 🤝 Contributing

This is a personal project, but documentation and code structure are designed for extensibility.

## 📄 License

MIT License - See LICENSE file for details

---

**Last Updated**: June 12, 2026  
**Current Phase**: Phase 1 (In Development)  
**Status**: Foundation Setup 🔨

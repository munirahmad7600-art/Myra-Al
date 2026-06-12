# 🤖 Myra - Intelligent Android Assistant

Myra is a comprehensive, background-running AI assistant for Android (Termux) that reads notifications, responds intelligently, controls apps, and evolves based on your usage patterns.

## 📋 Project Phases

### Phase 1: Foundation Layer ✅
- Persistent background service
- Notification listener (messages, calls, app notifications)
- Text-to-Speech announcements
- Floating UI indicator

### Phase 2: Intelligent Voice Interaction (In Progress)
- Speech-to-Text integration
- Gemini AI responses
- Casual conversation mode ("Ghupshup")

### Phase 3: System Control
- App launcher/closer
- Call handling
- SMS/WhatsApp integration

### Phase 4: Smart Integrations
- Weather API
- Time-based automation
- Context awareness

### Phase 5: Self-Evolution
- Usage analytics
- Feature recommendations
- Habit learning

## 🚀 Quick Start

### Requirements
- Android device with Termux
- Python 3.13+
- Termux API
- Google Gemini API key

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup Termux permissions
termux-setup-storage
pkg install termux-api

# Configure API key
export GEMINI_API_KEY="your_key_here"
# OR edit .env file

# Run Myra
python3 main.py
```

### Required Android Permissions
- Notification Access
- Accessibility Service
- SMS/Call Access

## 📂 Project Structure

```
Myra-Al/
├── config/              # Configuration & constants
├── core/                # Core service components
├── ai/                  # AI & conversation modules
├── system/              # System control
├── integrations/        # External APIs
├── analytics/           # Usage tracking
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

## 🔧 Architecture

- **Modular Design**: Each component is independently testable
- **Thread-Safe**: Notification listener and voice controller run in separate threads
- **Event-Driven**: Callback system for extensibility
- **Logging**: Comprehensive logging for debugging

## 📝 License

MIT License - Feel free to modify and distribute

## 🤝 Contributing

Contributions welcome! Please follow the existing code style.

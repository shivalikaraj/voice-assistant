![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AI](https://img.shields.io/badge/AI-Gemini-green.svg)
![Status](https://img.shields.io/badge/Project-Active-success.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

# 🎙️ AI Voice Assistant (Python)

A Python-based voice-controlled assistant that uses speech recognition, text-to-speech, APIs, and Gemini AI to perform everyday tasks like weather updates, news reading, note-taking, music playback, and intelligent responses.

## ✨ Features
- 🎤 Voice command recognition
- 🌦️ Live weather updates (OpenWeather API)
- 📰 Latest news headlines (RSS feed)
- 📝 Note-taking system (save/read/clear notes)
- 🎵 Music playback via custom library
- ⏰ Time, date, and day information
- 🌐 Open websites using voice
- 🤖 AI-powered fallback responses (Gemini AI)
- 🗣️ Text-to-speech responses

## 🛠️ Tech Stack
- Python 3
- SpeechRecognition
- pywin32 (SAPI Voice)
- requests
- feedparser
- Google Gemini AI API

## 📁 Project Structure
```text
voice-assistant/
│
├── main.py
├── ai_client.py
├── musicLibrary.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/shivalikaraj/voice-assistant.git
cd voice-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a .env file:
```env
WEATHER_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### 4. Run the project
```bash
python main.py
```

## 🎯 Example Commands
- “Alexa, what’s the time?”
- “Open YouTube”
- “What’s the weather in Tokyo?”
- “Take a note”
- “Read my notes”
- “Play Shape of You”
- “News”
- “What is AI?”

## 👨‍💻 Author

Built by [Shivalika Raj](https://github.com/shivalikaraj)

## ⭐ Show your support
If you like this project, consider giving it a ⭐ on GitHub!

## 🧠 Why this project matters?
This project demonstrates:

- Speech processing
- API integration
- AI integration
- Real-time system design
- Automation using Python

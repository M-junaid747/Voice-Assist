# JACK — AI Desktop Voice Assistant

A fully offline-capable, cross-platform desktop voice assistant built with Python. JACK listens for a wake word, understands your intent using a custom NLU pipeline, and responds with voice — no cloud STT required after setup.

> 🎥 **[Watch Demo Video](https://your-demo-link-here)**

---

## Features

- 🎙️ **Wake word activation** — say "hey jack" to activate, no button press needed
- 🔒 **Offline speech recognition** — powered by Vosk, no audio sent to the cloud
- 🧠 **Custom NLU pipeline** — text normalization, keyword scoring, confidence thresholding
- 🔌 **Plugin architecture** — drop a `.py` file in `features/`, it auto-registers at startup
- 🗣️ **Natural voice responses** — pyttsx3 TTS with configurable rate and volume
- 🛠️ **Dev workflow commands** — open VSCode, git status, git log, run scripts
- 📋 **Structured logging** — every interaction logged to file with timestamps
- 📦 **Standalone packaging** — ships as a single `.exe` via PyInstaller

---

## How It Works
Microphone → Wake Word Detection → Vosk STT → Text Normalizer

→ Intent Classifier → Registry Router → Skill Handler → pyttsx3 TTS

1. Background thread listens continuously for "hey jack"
2. On detection, Vosk captures and transcribes your spoken command
3. NLU pipeline normalizes text, scores against registered intent keyword sets
4. Highest-confidence intent above threshold routes to the matching handler
5. Handler returns a response string, pyttsx3 speaks it aloud

---

## Project Structure
jarvis-voice-assistant/

├── main.py                  # Entry point, wake word loop, auto-discovery

├── config.py                # All tunable settings in one place

├── requirements.txt

├── core/

│   ├── listener.py          # Wake word detection + Vosk STT

│   ├── speaker.py           # pyttsx3 TTS

│   ├── registry.py          # Decorator-based skill registration + routing

│   ├── logger.py            # Structured logging (file + console)

│   └── nlu/

│       ├── normalizer.py    # Contraction expansion, filler removal, punctuation stripping

│       └── classifier.py    # Keyword scoring intent classification

└── features/

├── general.py           # Time, date, Wikipedia search

└── dev_tools.py         # VSCode, terminal, Python shell, git, script runner

---

## Setup

### Requirements
- Python 3.12
- Windows / Linux / macOS
- Microphone

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/jarvis-voice-assistant.git
cd jarvis-voice-assistant

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### Download Vosk Model

Download the small English model (~40MB) from [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models):
vosk-model-small-en-us-0.15

Unzip it into the project root so the structure looks like:
jarvis-voice-assistant/

└── vosk-model-small-en-us-0.15/

├── am/

├── conf/

└── ...

### Run

```bash
python main.py
```

Say **"hey jack"** to activate, then speak a command.

---

## Available Commands

### General
| Say | Action |
|---|---|
| "what time is it" | Speaks current time |
| "what's the date" | Speaks today's date |
| "wikipedia [topic]" | Searches and reads a Wikipedia summary |

### Dev Tools
| Say | Action |
|---|---|
| "open vscode" | Launches VSCode in current directory |
| "open terminal" | Opens a new terminal window |
| "open python shell" | Opens a new Python interpreter window |
| "check git status" | Speaks modified/untracked file summary |
| "check git log" | Speaks last 5 commit messages |
| "run script" | Runs the configured default script |

### System
| Say | Action |
|---|---|
| "exit" / "goodbye" / "quit" | Shuts down the assistant |

---

## Adding New Skills

Create a new `.py` file in `features/`:

```python
from core.registry import register_intent

@register_intent(intent="greet", keywords=["hello", "hi", "hey", "greet"])
def handle_greet(text: str) -> str:
    return "Hello! How can I help you?"
```

That's it — JACK auto-discovers and registers it at startup. No changes to `main.py` needed.

---

## Configuration

All settings live in `config.py`:

```python
ASSISTANT_NAME = "JACK"
WAKE_WORD_MODEL = "hey jack"
NLU_THRESHOLD = 0.2          # Minimum confidence to act on an intent
AUDIO_DEVICE_INDEX = 1       # Microphone device index
TTS_SPEECH_RATE = 180        # Words per minute
```

---

## Packaging as Standalone .exe

```bash
pyinstaller jack.spec
```

Output: `dist/jack.exe` — runs without Python installed.

---

## Built With

- [Vosk](https://alphacephei.com/vosk/) — offline speech recognition
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) — text to speech
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) — audio capture
- [sounddevice](https://python-sounddevice.readthedocs.io/) — audio streaming
- [wikipedia](https://pypi.org/project/wikipedia/) — Wikipedia API wrapper
- [PyInstaller](https://pyinstaller.org/) — standalone packaging

---

## License

MIT License — free to use, modify, and distribute.
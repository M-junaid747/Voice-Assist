#Speech-to-Text settings
STT_LANG = "English" # speech language
STT_WAIT_TIME = 5 # Time to wait before the speech starts(before giving up)
STT_PHRASE_TIME_LIMIT = 8 # Allowed Time for the single phrase to last

# Text-to-Speech settings
TTS_SPEECH_RATE = 180 # words per minute
TTS_VOL = 1.0 # generated speech volume

# Certain name for the assistant
ASSISTANT_NAME = "JACK"

# Wikipedia User Agent
USER_AGENT = "voice-assistant"

# Set of words, if spoken, should shutdown the assistant. 
EXIT_COMMANDS = {"exit", "goodbye", "takecare", "stop", "quit", "shutdown", "see you soon"}

DEFAULT_SCRIPT = "main.py"

# NLU confidence threshold — minimum score for an intent to be acted on.
# Below this, the assistant says "I didn't understand" instead of guessing.
# Tune this up if getting too many false positives, down if missing real commands.
NLU_THRESHOLD = 0.25

# Audio settings for Vosk STT and wake word detection
AUDIO_SAMPLE_RATE = 16000
AUDIO_BLOCK_SIZE = 8000
AUDIO_DEVICE_INDEX = 1
WAKE_WORD_MODEL = "hey_jarvis"
WAKE_WORD_THRESHOLD = 0.5
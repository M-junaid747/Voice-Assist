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
# import speech_recognition as sr
import json
import threading
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import config

# shared signal — wake word thread sets this, main loop waits on it
WAKE_EVENT = threading.Event()

# load models
vosk_model = Model("vosk-model-small-en-us-0.15")
wake_recognizer = KaldiRecognizer(vosk_model, config.AUDIO_SAMPLE_RATE)
command_recognizer = KaldiRecognizer(vosk_model, config.AUDIO_SAMPLE_RATE)

def _wake_word_loop():
        with sd.RawInputStream(
        samplerate=config.AUDIO_SAMPLE_RATE,
        blocksize=config.AUDIO_BLOCK_SIZE,
        device=config.AUDIO_DEVICE_INDEX,
        dtype="int16",
        channels=1
        ) as stream:
            while True:
                data, _ = stream.read(config.AUDIO_BLOCK_SIZE)
                audio_chunks = wake_recognizer.AcceptWaveform(bytes(data))

                if audio_chunks:
                    result = wake_recognizer.Result()
                    json_text = json.loads(result)

                    text = json_text.get("text", "")

                    if config.WAKE_WORD_MODEL in text:
                         if not WAKE_EVENT.is_set():
                              print("Wake word detected...")
                              WAKE_EVENT.set()

def start_wake_word_listener():
    thread = threading.Thread(target=_wake_word_loop, daemon=True)
    thread.start()

def listen() ->str | None:
    with sd.RawInputStream(
        samplerate=config.AUDIO_SAMPLE_RATE,
        blocksize=config.AUDIO_BLOCK_SIZE,
        device=config.AUDIO_DEVICE_INDEX,
        dtype="int16",
        channels=1
        ) as stream:
            while True:
                audio, _ = stream.read(config.AUDIO_BLOCK_SIZE)            
                utterance = command_recognizer.AcceptWaveform(bytes(audio))

                if utterance:
                    result = command_recognizer.Result()
                    json_text = json.loads(result)

                    text = json_text.get("text", "")

                    if text:
                        return text.lower()
                    else:
                        return None

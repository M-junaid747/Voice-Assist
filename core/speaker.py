import pyttsx3
import config

def speak(text):
    engine = pyttsx3.init()

    engine.setProperty("rate", config.TTS_SPEECH_RATE)
    engine.setProperty("volume", config.TTS_VOL)

    engine.say(text)

    engine.runAndWait()

    engine.stop()
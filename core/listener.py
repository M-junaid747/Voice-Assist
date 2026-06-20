import speech_recognition as sr
import config

def listen():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration = 0.5)
        
        try:
            audio = recognizer.listen(
                source, timeout= config.STT_WAIT_TIME,
                phrase_time_limit = config.STT_PHRASE_TIME_LIMIT)

        except sr.WaitTimeoutError:
            print("Input Timed out. Try Again...")
            return None


        try:    
            recognized_text = recognizer.recognize_google(audio, language = config.STT_LANG)

        except sr.UnknownValueError:
            print("Voice not recognized")
            return None

        except sr.RequestError:
            print("Connection Failed")
            return None

        except Exception as e:
            print(f"An unknown error {e} occured")
            return None

        return recognized_text.lower()
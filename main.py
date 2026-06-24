import config

import features.general
import features.dev_tools
import wikipedia
from core import listener, speaker, registry
from core.listener import start_wake_word_listener, WAKE_EVENT

def main():
    start_wake_word_listener()
    wikipedia.set_user_agent(config.USER_AGENT)

    print(f"=== {config.ASSISTANT_NAME} (Stage 4) ===")
    print(f"Say '{config.WAKE_WORD_MODEL}' to activate.\n")
    speaker.speak(f"{config.ASSISTANT_NAME} is online. Say hey jarvis to activate.")

    while True:
        WAKE_EVENT.wait()
        WAKE_EVENT.clear()

        speaker.speak("Yes?")
        text = listener.listen()
        
        if not text:
            continue
        
        if any(cmd in text for cmd in config.EXIT_COMMANDS):
            speaker.speak("Goodbye!")
            break
        
        try:
            reply = registry.route_command(text)
    
            if reply is None:
                reply = "Sorry, I don't know how to do that yet."

            speaker.speak(reply)
        except Exception as e:
            print(f"Unexpected Exception... {e}")
            continue 

# Entry point. Not a Library. Execute main() only when this main.py runs, not when it is imported somewhere else.
if __name__ == "__main__":
    main()
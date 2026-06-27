import os
import importlib
import config

import wikipedia
from core import listener, speaker, registry
from core.listener import start_wake_word_listener, WAKE_EVENT
from core.logger import logger

def load_features():
        features_dir = os.path.join(os.path.dirname(__file__), "features")
        for filename in os.listdir(features_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = "features." + filename.replace(".py", "")
                try:
                    importlib.import_module(module_name)
                    logger.info(f"Loaded: {module_name}")
                except Exception as e:
                    logger.warning(f"Failed to load {module_name}: {e}")

def main():
    load_features()   
    start_wake_word_listener()
    wikipedia.set_user_agent(config.USER_AGENT)

    logger.info(f"=== {config.ASSISTANT_NAME} (Stage 5) ===")
    logger.info(f"Say '{config.WAKE_WORD_MODEL}' to activate.\n")
    speaker.speak(f"{config.ASSISTANT_NAME} is online. Say hey jack to activate.")             

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
            logger.error(f"Unexpected Exception... {e}")
            continue 

# Entry point. Not a Library. Execute main() only when this main.py runs, not when it is imported somewhere else.
if __name__ == "__main__":
    main()
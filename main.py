import config

import wikipedia
from core import listener, speaker, commands

def main():
    wikipedia.set_user_agent(config.USER_AGENT)

    print(f"=== {config.ASSISTANT_NAME} (Stage 1) ===")
    print("Press ENTER to speak, or type 'exit' to quit.\n")

    speaker.speak(f"{config.ASSISTANT_NAME} is online. Press Enter to speak to me.")

    while True:
        user_input = input("\n[Press ENTER to talk, or type a command/'exit']: ").strip().lower()

        # Allow typed exit too, without needing the mic — useful for quick
        # testing without triggering speech recognition every time.
        if user_input in config.EXIT_COMMANDS:
            speaker.speak("Goodbye!")
            break

        # If they typed something other than just hitting Enter, treat the
        # typed text itself as the command (handy for testing without a mic).
        if user_input:
            text = user_input
        else:
            text = listener.listen()

        if not text:
            # Either mic timeout or unintelligible audio — listener.listen()
            # already printed the reason, so just loop back and try again.
            continue

        
        if text in config.EXIT_COMMANDS or any(cmd in text for cmd in config.EXIT_COMMANDS):
            speaker.speak("Goodbye!")
            break
        

        try:
            reply = commands.route_command(text)
    
            if reply is None:
                reply = "Sorry, I don't know how to do that yet."

            speaker.speak(reply)
        except Exception as e:
            print(f"Unexpected Exception... {e}")
            continue 

# Entry point. Not a Library. Execute main() only when this main.py runs, not when it is imported somewhere else.
if __name__ == "__main__":
    main()
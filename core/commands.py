import datetime
import platform
import webbrowser
import subprocess

import wikipedia

def handle_time(text: str) ->str:
    return f"The time is {datetime.datetime.now().strftime("%I: %M %p")}"

def handle_date(text: str) ->str:
    return f"The date today is {datetime.datetime.now().strftime("%B %d, %Y")}"


def handle_wikipedia(text: str) -> str:
    # Strip the trigger word to get the actual search topic.
    # e.g. "wikipedia albert einstein" -> "albert einstein"
    topic = text.replace("wikipedia", "", 1).strip()
    if not topic:
        return "What would you like me to look up on Wikipedia?"

    try:
        # sentences=2 keeps spoken responses short — a full Wikipedia
        # summary read aloud is tedious to listen to.
        print(f"Searching Wikipedia for: {topic}...")
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.DisambiguationError as e:
        # Topic is ambiguous (e.g. "Mercury" -> planet, element, or god).
        # Ask the user to be specific rather than guessing wrong.
        options = ", ".join(e.options[:3])
        return f"That topic is ambiguous. Did you mean: {options}?"
    except wikipedia.PageError:
        return f"I couldn't find anything on Wikipedia about {topic}."
    except Exception:
        # Catch-all for network errors etc. — a Stage 1 voice assistant
        # should never crash mid-conversation over a failed API call.
        return "Something went wrong searching Wikipedia."
    

def _open_app_cross_platform(app_key: str) -> str:
    """
    Maps a generic app_key (what the user SAID) to the correct OS-specific
    command (what actually needs to RUN). This indirection is the whole
    point: "open notepad" should work consistently as a voice command even
    though Notepad doesn't exist on Linux/macOS — we just open the closest
    equivalent text editor there instead.
    """
    system = platform.system()  # 'Windows', 'Linux', or 'Darwin' (macOS)

    app_map = {
        "notepad": {
            "Windows": ["notepad.exe"],
            "Linux": ["gedit"],
            "Darwin": ["open", "-a", "TextEdit"],
        },
        "calculator": {
            "Windows": ["calc.exe"],
            "Linux": ["gnome-calculator"],
            "Darwin": ["open", "-a", "Calculator"],
        },
    }

    if app_key == "browser":
        # webbrowser module already handles cross-platform browser launching
        # natively — no need to reinvent this one.
        webbrowser.open("https://www.google.com")
        return "Opening your browser"

    if app_key not in app_map:
        return f"I don't know how to open {app_key} yet"

    command = app_map[app_key].get(system)
    if not command:
        return f"Opening {app_key} isn't supported on {system} yet"

    try:
        subprocess.Popen(command)
        return f"Opening {app_key}"
    except FileNotFoundError:
        # The mapped binary isn't installed (e.g. gedit not present on this
        # particular Linux distro). Fail gracefully with a clear message
        # instead of a raw traceback.
        return f"I tried to open {app_key}, but it doesn't seem to be installed"


def handle_open_notepad(text: str) -> str:
    return _open_app_cross_platform("notepad")


def handle_open_calculator(text: str) -> str:
    return _open_app_cross_platform("calculator")


def handle_open_browser(text: str) -> str:
    return _open_app_cross_platform("browser")


COMMANDS = {
    "what time is it": handle_time,
    "what's the time": handle_time,
    "current time": handle_time,
    "what's the date": handle_date,
    "today's date": handle_date,
    "wikipedia": handle_wikipedia,
    "open notepad": handle_open_notepad,
    "open calculator": handle_open_calculator,
    "open browser": handle_open_browser,
}


def route_command(text: str) -> str | None:
    """
    Stage 1 routing: simple substring match against COMMANDS keys.

    This is deliberately the "dumb" version — first match wins, no
    confidence scoring, no entity extraction. It's the equivalent of a
    Django urls.py with hardcoded string paths instead of converters.
    Good enough to prove the concept; Stage 3 replaces this with real
    intent classification.

    Returns None if nothing matched, so main.py can give a fallback
    response without route_command needing to know about that fallback
    text itself (separation of concerns).
    """
    for trigger_phrase, handler in COMMANDS.items():
        if trigger_phrase in text:
            return handler(text)
    return None
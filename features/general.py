import datetime

import wikipedia
from core.registry import register_intent

@register_intent(intent = "time", keywords = ["time", "clock", "hour", "current", "now"])
def handle_time(text: str) ->str:
    return f"The time is {datetime.datetime.now().strftime("%I:%M %p")}"

@register_intent(intent = "date", keywords = ["date", "day", "today", "month", "year"])
def handle_date(text: str) ->str:
    return f"The date today is {datetime.datetime.now().strftime("%B %d, %Y")}"

@register_intent(intent = "wikipedia", keywords = ["wikipedia", "search", "lookup", "tell", "who"])
def handle_wikipedia(text: str) -> str:
    # Strip the trigger word to get the actual search topic.
    # e.g. "wikipedia albert einstein" -> "albert einstein"
    trigger_words = ["wikipedia", "search", "lookup", "tell", "who"]
    for word in trigger_words:
        text = text.replace(word , "", 1)
    topic = text.strip()
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
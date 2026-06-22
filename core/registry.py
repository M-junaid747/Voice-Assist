REGISTRY = {}

def register_intent(trigger_phrase):
    def decorator(fun):
        REGISTRY[trigger_phrase] = fun
        return fun
    return decorator

def route_command(text: str) ->str | None:
    for trigger_phrase, handler in REGISTRY.items():
        if trigger_phrase in text:
            return handler(text)
    return None    
    
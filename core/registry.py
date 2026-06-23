REGISTRY = {}

def register_intent(intent: str, keywords: list):
    def decorator(fun):
        REGISTRY[intent] = {
            "keywords": keywords,
            "handler": fun
        }
        return fun
    return decorator

def route_command(text: str) ->str | None:
    from core.nlu.classifier import classify
    result = classify(text)
    if result is None:
        return None
    
    intent_label, clean_text = result
    
    entry = REGISTRY.get(intent_label)
    if entry is None:
        return None
    
    return entry["handler"](clean_text)
    
    
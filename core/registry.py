from core.logger import logger

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
    
    logger.info(f"Intent matched: {intent_label}")    
    return entry["handler"](clean_text)
    
    
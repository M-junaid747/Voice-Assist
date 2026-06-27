import config
from core.registry import REGISTRY
from core.nlu.normalizer import normalize
from core.logger import logger

def classify(text: str) ->tuple | None:
    clean_text = normalize(text)

    
    total_intent_keywords = 0

    scores = {}

    words = clean_text.split()

    for intent_label, intent_data in REGISTRY.items():
        keywords_in_text = 0
        keywords = intent_data.get("keywords", [])
        if not keywords:
            scores[intent_label] = 0.0
            continue
        
        total_intent_keywords = len(keywords)

        for keyword in keywords:
            if keyword in words:
                keywords_in_text +=1
                
        score = keywords_in_text / total_intent_keywords

        scores[intent_label] = score

        if not scores:
            return None

    best_intent = max(scores, key = scores.get)
    best_score = scores[best_intent]

    if best_score < config.NLU_THRESHOLD:
        logger.warning(f"Low confidence - best: {best_intent} = {best_score:.2f}")
        return None
    
    return (best_intent, clean_text)

    



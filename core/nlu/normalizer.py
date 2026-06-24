import string

CONTRACTIONS =  {
    "don't": "do not",
    "can't": "cannot",
    "won't": "will not",
    "it's": "it is",
    "i'm": "i am",
    "you're": "you are",
    "they're": "they are",
    "isn't": "is not",
    "wasn't": "was not",
    "didn't": "did not",
    "i'd": "i would",
    "we'll": "we will",
    "could've": "could have",
    "should've": "should have",
    "you've": "you have",
    "what's": "what is"
}

FILLERS = {
    "um", "uh", "er", "like", "you", "me",
    "actually", "basically", "literally", "i", 
    "right", "so", "well", "hmm", "anyway"
}

def normalize(text: str) ->str:
    # Removing contractions
    for contraction, expansion in CONTRACTIONS.items():
        text = text.replace(contraction, expansion)

    # Removing punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Removing fillers
    words = text.split()
    words = [word for word in words if word not in FILLERS]
    
    text = " ".join(words)
    return text

    
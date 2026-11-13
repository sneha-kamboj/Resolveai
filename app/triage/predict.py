import joblib

MODEL_PATH = "app/triage/triage_model.joblib"
THRESHOLD = 0.45


_model = None
def _load():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(text):
    if not text or not text.strip():
        return("esclate",0.0)
    model = _load()
    proba = model.predict_proba([text])[0]
    best = int(proba.argmax())
    intent =  model.named_steps["clf"].classes_[best]
    conf = float(proba[best])
    if conf < THRESHOLD:
      return ("escalate",conf)
    return (intent,conf)
if __name__ == "__main__":
    tests = [
        "Where is my order?",
        "I want to return my shoes.",
        "When will I receive my refund?",
        "My earbuds are defective. Please send a replacement.",
        "What is your return policy?",
        "asdf qwer zxcv",
    ]

    for t in tests:
        print(t, "->", predict(t))
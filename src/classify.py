"""
Two classifiers, so we always have a baseline to beat:

1. TfidfBaselineClassifier - "simple" baseline (assignment requires this).
   Trained on a handful of seed examples per intent (see SEED_EXAMPLES below).
   TODO: once you have the golden set, retrain this on real labeled data instead
   of the small seed set — the seed set is only here so the pipeline runs today.

2. classify_with_llm - the actual system under test. Zero/few-shot classification
   via the local LLM, since we don't have enough labeled data yet to fine-tune
   anything, and it's easy to iterate on the prompt as the taxonomy evolves.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from src import config
from src.llm_client import generate_json

# Minimal seed set so the TF-IDF baseline is trainable out of the box.
# TODO: replace with real labeled examples pulled from your golden set.
SEED_EXAMPLES = [
    ("photoshop keeps crashing when i open a file", "bug_crash"),
    ("app freezes on export", "bug_crash"),
    ("i was charged twice this month", "billing_dispute"),
    ("refund please, cancelled last month but still billed", "billing_dispute"),
    ("i can't log into my account, password not working", "account_access"),
    ("locked out of my adobe id", "account_access"),
    ("someone else logged into my account and changed my email", "security_incident"),
    ("my card info was leaked, unauthorized charge", "security_incident"),
    ("how do i download lightroom on a new laptop", "how_to"),
    ("where do i find the install link", "how_to"),
    ("please cancel my subscription", "subscription_mgmt"),
    ("how do i change my billing address", "subscription_mgmt"),
    ("thanks for the help yesterday, great support", "feedback_praise"),
    ("would be great if you added multicam support", "feedback_praise"),
]


class TfidfBaselineClassifier:
    def __init__(self):
        texts, labels = zip(*SEED_EXAMPLES)
        self.vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        X = self.vec.fit_transform(texts)
        self.clf = LogisticRegression(max_iter=1000)
        self.clf.fit(X, labels)

    def predict(self, text: str):
        X = self.vec.transform([text])
        pred = self.clf.predict(X)[0]
        proba = max(self.clf.predict_proba(X)[0])
        return pred, float(proba)


LLM_CLASSIFY_SYSTEM = f"""You classify customer support tweets sent to Adobe (AdobeCare)
into exactly one intent from this fixed list: {config.INTENTS}.
Respond ONLY with JSON: {{"intent": "<one of the list>", "confidence": <0-1 float>, "reason": "<one short sentence>"}}
No other text, no markdown fences."""


def classify_with_llm(text: str) -> dict:
    prompt = f'Customer tweet: "{text}"\n\nClassify it.'
    result = generate_json(prompt, system=LLM_CLASSIFY_SYSTEM)
    if result.get("intent") not in config.INTENTS:
        result["intent"] = "how_to"  # safe fallback, never crash the pipeline
        result["confidence"] = 0.0
        result["reason"] = "model returned an out-of-taxonomy label; defaulted"
    return result

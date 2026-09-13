# Customer-Support-Intent-Response-Agent
A grounded, evaluated AI support agent that classifies incoming customer tweets for [Brand], drafts replies based on how the brand historically resolved similar issues, and decides whether to auto-handle or escalate — with a hand-labeled Golden Set, an LLM-as-judge harness, and a full failure analysis proving it can be trusted.

## Usage

### Run the full pipeline
```bash
python src/pipeline.py --data data/adobecare_clean.csv --out results/predictions.csv
```
Output (`results/predictions.csv`) — one row per tweet:
```
tweet_id,customer_text,predicted_intent,confidence,draft_reply,escalate,escalation_reason
1234,"my card was charged twice",billing_dispute,0.81,"Sorry about the duplicate charge! Please DM your account email...",False,"intent 'billing_dispute' with confidence 0.81 is safe to auto-handle"
```

### Run evaluation
```bash
python eval/metrics.py --predictions results/predictions.csv --golden eval/golden_set_labeled.csv
```
```
=== Intent classification ===
              precision    recall  f1-score   support
bug_crash          0.78      0.82      0.80        45
billing_dispute    0.71      0.65      0.68        32
...
=== Escalation decision ===
Precision: 0.88  Recall: 0.94  F1: 0.91
```

### Run a single example programmatically
```python
from src.classify import classify_with_llm
from src.retrieve import HistoryRetriever
from src.reply import draft_reply
from src.escalate import should_escalate
import pandas as pd

history = pd.read_csv("data/adobecare_clean.csv")
retriever = HistoryRetriever(history)

text = "my creative cloud subscription charged me twice this month"
result = classify_with_llm(text)
retrieved = retriever.retrieve(text)
reply = draft_reply(text, retrieved)
decision = should_escalate(text, result["intent"], result["confidence"])

print(result, decision, reply)
```

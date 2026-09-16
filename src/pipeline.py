"""
End-to-end: classify -> retrieve -> draft reply -> escalate decision.

Usage:
    python src/pipeline.py --data data/synthetic_sample.csv --out results/predictions.csv
"""
import argparse
import os
import pandas as pd
from tqdm import tqdm

from src.classify import TfidfBaselineClassifier, classify_with_llm
from src.retrieve import HistoryRetriever
from src.reply import draft_reply
from src.escalate import should_escalate


def run(data_path: str, out_path: str, use_llm_classifier: bool = True):
    df = pd.read_csv(data_path)
    assert {"customer_text", "brand_reply_text"}.issubset(df.columns), \
        "input csv needs customer_text and brand_reply_text columns"
    before = len(df)
    df["customer_text"] = df["customer_text"].fillna("").astype(str)
    df["brand_reply_text"] = df["brand_reply_text"].fillna("").astype(str)
    df = df[df["customer_text"].str.strip() != ""].reset_index(drop=True)
    print(f"Dropped {before - len(df)} rows with empty customer_text")

    retriever = HistoryRetriever(df)
    baseline_clf = TfidfBaselineClassifier()

    rows = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Running pipeline"):
        text = row["customer_text"]

        baseline_intent, baseline_conf = baseline_clf.predict(text)

        if use_llm_classifier:
            try:
                llm_result = classify_with_llm(text)
                intent, confidence = llm_result["intent"], llm_result["confidence"]
            except Exception as e:
                print(f"\n[warn] classification failed for row {row.get('tweet_id')}: {e}")
                intent, confidence = baseline_intent, baseline_conf
        else:
            intent, confidence = baseline_intent, baseline_conf

        retrieved = retriever.retrieve(text)
        try:
            reply = draft_reply(text, retrieved)
        except Exception as e:
            reply = ""
            print(f"\n[warn] reply generation failed for row {row.get('tweet_id')}: {e}")
        decision = should_escalate(text, intent, confidence)

        rows.append({
            "tweet_id": row.get("tweet_id"),
            "customer_text": text,
            "predicted_intent": intent,
            "confidence": confidence,
            "baseline_intent": baseline_intent,
            "draft_reply": reply,
            "escalate": decision["escalate"],
            "escalation_reason": decision["reason"],
            "actual_brand_reply": row["brand_reply_text"],  # for eyeballing/eval only
        })

        if len(rows) % 25 == 0:
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            pd.DataFrame(rows).to_csv(out_path, index=False)

    out_df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    out_df.to_csv(out_path, index=False)
    print(f"Wrote {len(out_df)} predictions to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-llm-classifier", action="store_true",
                     help="use the TF-IDF baseline as the primary classifier instead of the LLM")
    args = ap.parse_args()
    run(args.data, args.out, use_llm_classifier=not args.no_llm_classifier)

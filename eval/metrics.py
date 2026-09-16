"""
Automated metrics: intent classification accuracy/F1, and escalation-decision
accuracy against the hand-labeled golden set.

Usage:
    python eval/metrics.py --predictions results/predictions.csv --golden eval/golden_set_labeled.csv
"""
import argparse
import pandas as pd
from sklearn.metrics import classification_report, precision_recall_fscore_support


def evaluate(predictions_path: str, golden_path: str):
    preds = pd.read_csv(predictions_path)
    golden = pd.read_csv(golden_path)

    merged = golden.merge(preds, on="tweet_id", suffixes=("_true", "_pred"))
    if len(merged) == 0:
        raise ValueError("No overlapping tweet_ids between predictions and golden set. "
                          "Did you run the pipeline on the same data the golden set was sampled from?")

    print(f"Evaluating on {len(merged)} golden examples\n")

    print("=== Intent classification ===")
    print(classification_report(
        merged["true_intent"], merged["predicted_intent"], zero_division=0
    ))

    print("=== Escalation decision ===")
    y_true = merged["true_should_escalate"].astype(str).str.lower() == "true"
    y_pred = merged["escalate"].astype(str).str.lower() == "true"
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
    print(f"Precision: {p:.3f}  Recall: {r:.3f}  F1: {f1:.3f}")
    print(f"(Recall matters most here: a missed escalation is worse than an unnecessary one.)")

    # Baselines for comparison — fill these in as you build them
    print("\n=== Reminder: report these alongside a trivial and a simple baseline ===")
    print("- Trivial: majority-class intent, always-auto-handle")
    print("- Simple: keyword-based intent classifier")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True)
    ap.add_argument("--golden", required=True)
    args = ap.parse_args()
    evaluate(args.predictions, args.golden)

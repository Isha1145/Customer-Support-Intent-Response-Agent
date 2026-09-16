"""
Samples examples for hand-labeling. Stratified where possible so the golden set
isn't dominated by whatever intent happens to be most common in the raw data.

Usage:
    python eval/build_golden_set.py --data data/adobecare_clean.csv --n 200 --out eval/golden_set_to_label.csv

Workflow:
1. Run this BEFORE you've built your classifier (or at least before looking at its
   outputs) so your labels aren't unconsciously anchored to model predictions.
2. Open the output CSV, fill in `true_intent` (from docs/intent_taxonomy.md) and
   `true_should_escalate` (True/False) by hand for every row.
3. Save as eval/golden_set_labeled.csv.
"""
import argparse
import pandas as pd


def sample(data_path: str, n: int, seed: int = 42) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    # Simple random sample by default. If you already have a rough intent guess
    # (e.g. from a keyword pass), swap this for df.groupby(...).sample(...) to
    # stratify — documented here so it's an explicit, explainable decision either way.
    sampled = df.sample(n=min(n, len(df)), random_state=seed)
    sampled = sampled[["tweet_id", "customer_text", "brand_reply_text"]].copy()
    sampled["true_intent"] = ""            # fill by hand
    sampled["true_should_escalate"] = ""   # fill by hand: True/False
    sampled["true_escalate_reason"] = ""   # fill by hand: one short sentence
    sampled["labeling_notes"] = ""         # anything ambiguous, flag it here
    return sampled


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = sample(args.data, args.n)
    out.to_csv(args.out, index=False)
    print(f"Wrote {len(out)} rows to label at {args.out}")

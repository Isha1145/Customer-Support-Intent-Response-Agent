"""
Measures how much the LLM judge agrees with a human on the SAME replies, so you
can honestly report how much to trust the judge (the assignment explicitly asks
for this — an unvalidated LLM judge is not evidence of anything).

Workflow:
1. Take ~30-50 rows from results/judged.csv (a random subset is fine).
2. Have a human (you) independently score "overall" 1-5 for each, WITHOUT looking
   at the judge's score first. Save as a csv with columns: tweet_id, human_overall.
3. Run this script.

Usage:
    python eval/human_agreement.py --judged results/judged.csv --human eval/human_scores.csv
"""
import argparse
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score


def compare(judged_path: str, human_path: str):
    judged = pd.read_csv(judged_path)
    human = pd.read_csv(human_path)
    merged = judged.merge(human, on="tweet_id")

    if len(merged) == 0:
        raise ValueError("No overlapping tweet_ids between judged and human scores.")

    rho, p = spearmanr(merged["judge_overall"], merged["human_overall"])
    kappa = cohen_kappa_score(
        merged["judge_overall"].round().astype(int),
        merged["human_overall"].round().astype(int),
        weights="quadratic",
    )

    print(f"n = {len(merged)}")
    print(f"Spearman correlation (judge vs human, 'overall'): {rho:.3f} (p={p:.4f})")
    print(f"Quadratic-weighted Cohen's kappa: {kappa:.3f}")
    print("\nRule of thumb: kappa > 0.6 = reasonably trustworthy judge; "
          "< 0.4 = don't rely on it for the headline number, report it as a caveat instead.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--judged", required=True)
    ap.add_argument("--human", required=True)
    args = ap.parse_args()
    compare(args.judged, args.human)

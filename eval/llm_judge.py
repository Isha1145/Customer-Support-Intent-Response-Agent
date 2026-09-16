"""
LLM-as-judge for drafted reply quality, on a fixed rubric so scores are comparable
across runs. Scores 1-5 on each axis plus a short justification (required, so you
can spot-check *why* the judge gave a score, not just the number).

Usage:
    python eval/llm_judge.py --predictions results/predictions.csv --out results/judged.csv
"""
import argparse
import pandas as pd
from tqdm import tqdm
from src.llm_client import generate_json

JUDGE_SYSTEM = """You are grading a customer support reply drafted by an AI agent for
Adobe's AdobeCare Twitter account. Score the DRAFT REPLY on this rubric, each 1-5:

- groundedness: does it match how AdobeCare actually resolved similar past issues,
  without inventing policy/facts not present in context?
- helpfulness: does it give the customer a concrete next step?
- tone: brief, warm, on-brand for a support tweet (not robotic, not over-promising)?
- correctness: no factual claims that contradict the retrieved context or common sense?

Respond ONLY with JSON:
{"groundedness": <1-5>, "helpfulness": <1-5>, "tone": <1-5>, "correctness": <1-5>,
 "overall": <1-5>, "justification": "<one sentence>"}"""


def judge_one(customer_text: str, draft_reply: str, reference_reply: str) -> dict:
    prompt = f"""Customer tweet: "{customer_text}"
Reference (a real past AdobeCare reply to a similar issue, for context only): "{reference_reply}"
AI-drafted reply to grade: "{draft_reply}"

Score it."""
    return generate_json(prompt, system=JUDGE_SYSTEM)


def judge_all(predictions_path: str, out_path: str):
    df = pd.read_csv(predictions_path)
    scores = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Judging replies"):
        try:
            s = judge_one(row["customer_text"], row["draft_reply"], row["actual_brand_reply"])
        except Exception as e:
            s = {"groundedness": None, "helpfulness": None, "tone": None,
                 "correctness": None, "overall": None, "justification": f"judge error: {e}"}
        scores.append(s)

    scores_df = pd.DataFrame(scores)
    out = pd.concat([df, scores_df.add_prefix("judge_")], axis=1)
    out.to_csv(out_path, index=False)

    print("Mean scores:")
    print(scores_df.mean(numeric_only=True))
    print(f"\nWrote full results to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True)
    ap.add_argument("--out", default="results/judged.csv")
    args = ap.parse_args()
    judge_all(args.predictions, args.out)

"""
Filter the raw Customer Support on Twitter dataset (twcs.csv) down to one brand
and reconstruct (customer_text, brand_reply_text) pairs.

Usage:
    python src/data_prep.py --input data/twcs.csv --brand AdobeCare --out data/adobecare_clean.csv

Expected raw columns (per the Kaggle dataset schema):
    tweet_id, author_id, inbound, created_at, text,
    response_tweet_id, in_response_to_tweet_id
"""
import argparse
import re
import pandas as pd


def clean_text(t: str) -> str:
    t = re.sub(r"http\S+", "", str(t))          # strip URLs
    t = re.sub(r"@\w+", "", t)                  # strip @mentions (brand handle, etc.)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def build_pairs(df: pd.DataFrame, brand_handle: str) -> pd.DataFrame:
    """
    df: full twcs dataframe
    brand_handle: the brand's author_id in the dataset, e.g. 'AdobeCare'
    """
    brand_tweets = df[(df["author_id"] == brand_handle) & (~df["inbound"])]
    customer_tweets = df[df["inbound"]].set_index("tweet_id")

    rows = []
    for _, brand_row in brand_tweets.iterrows():
        in_reply_to = brand_row.get("in_response_to_tweet_id")
        if pd.isna(in_reply_to):
            continue
        try:
            cust_row = customer_tweets.loc[int(in_reply_to)]
        except (KeyError, ValueError):
            continue
        rows.append({
            "tweet_id": brand_row["tweet_id"],
            "customer_text": clean_text(cust_row["text"]),
            "brand_reply_text": clean_text(brand_row["text"]),
            "created_at": brand_row.get("created_at"),
        })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="path to raw twcs.csv")
    ap.add_argument("--brand", required=True, help="author_id of the brand, e.g. AdobeCare")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sample", type=int, default=5000,
                     help="max rows to keep after filtering (assignment expects a subsample)")
    args = ap.parse_args()

    print(f"Reading {args.input} ...")
    df = pd.read_csv(args.input)
    df["inbound"] = df["inbound"].astype(str).str.lower() == "true"

    pairs = build_pairs(df, args.brand)
    print(f"Reconstructed {len(pairs)} (customer, brand_reply) pairs for {args.brand}")

    if len(pairs) > args.sample:
        pairs = pairs.sample(args.sample, random_state=42)

    pairs.to_csv(args.out, index=False)
    print(f"Wrote {len(pairs)} rows to {args.out}")


if __name__ == "__main__":
    main()

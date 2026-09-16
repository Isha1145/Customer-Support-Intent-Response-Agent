# Getting the real data

1. Download `twcs.csv` from
   https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter
   (needs a free Kaggle account; either use the web download button or the Kaggle CLI:
   `kaggle datasets download -d thoughtvector/customer-support-on-twitter`)
2. Place `twcs.csv` in this folder.
3. Run:
   ```bash
   python ../src/data_prep.py --input twcs.csv --brand AdobeCare --out adobecare_clean.csv
   ```
   This filters to:
   - inbound tweets directed at @AdobeCare
   - AdobeCare's reply to each (the "resolution"), matched via `response_tweet_id` /
     `in_response_to_tweet_id`
   - reconstructs each (customer message -> brand reply) pair, and where possible the
     full back-and-forth thread

4. `adobecare_clean.csv` is what feeds `src/pipeline.py` and `eval/build_golden_set.py`.

## Why AdobeCare
- Clearly a software company, per the assignment framing.
- High tweet volume in the dataset (enough to sample a meaningful golden set).
- Intent mix spans genuinely easy-to-automate issues (password reset, "where do I
  download X") and genuinely risky ones (billing disputes, account access/security),
  which makes the escalation-policy part of this assignment non-trivial instead of a
  rubber stamp.

## `synthetic_sample.csv`
20 hand-written tweets in the AdobeCare style, covering every intent in
`docs/intent_taxonomy.md`, so the pipeline is runnable before real data arrives.
These are NOT real customer data and must not be used for the golden eval set or
in the final report's results.

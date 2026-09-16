# Intent taxonomy (draft — finalize after skimming ~500 real AdobeCare tweets)

These 7 intents were drafted from a first look at typical AdobeCare-style traffic.
**TODO once real data is filtered**: pull ~500 random AdobeCare inbound tweets, skim
them, and confirm/adjust this list — do not skip this step, the assignment explicitly
wants intents "defined from the data," not from assumption.

| Intent | Description | Typical auto-handle? |
|---|---|---|
| `bug_crash` | App crashing, freezing, feature broken | Sometimes (if known fix exists) |
| `billing_dispute` | Wrong charge, duplicate charge, refund request | Rarely — usually needs account lookup |
| `account_access` | Login issues, password reset, "locked out" | Sometimes (password reset is self-serve) |
| `security_incident` | Suspected unauthorized access, data/credential leak | **Never** — always escalate |
| `how_to` | "How do I download/install/find X" | Often |
| `subscription_mgmt` | Cancel, change plan, change billing address, student discount | Sometimes |
| `feedback_praise` | Feature requests, compliments, general feedback | Often (no urgency, low risk) |

## What we chose NOT to build
- No sentiment-only category — sentiment is treated as an escalation *signal*
  (see `src/escalate.py`), not a standalone intent, since "angry customer" cuts across
  every intent above.
- No fine-grained product-specific intents (e.g. separate categories for Photoshop vs.
  Illustrator crashes). Product name is captured as a slot/entity, not a separate class,
  to keep the label space small enough to hand-label reliably in the golden set.
- No multi-label classification (one tweet = one primary intent). Real tweets are
  sometimes multi-intent (e.g. "billing issue AND feature request") — we take the
  dominant one and note this as a known limitation in the report.

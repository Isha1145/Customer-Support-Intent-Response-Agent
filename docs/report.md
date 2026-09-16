# Report — AdobeCare Support Agent

## 1. Problem framing
- What does "good" mean for AdobeCare specifically? [e.g. correctly identifying which
  issues are safe to auto-resolve vs. which carry account/security/billing risk;
  a wrong auto-handled billing reply is much more costly than a wrong auto-handled
  "how do I download X" reply — reflect this asymmetry in what you optimize for]
- What did you choose NOT to build, and why? (see also docs/intent_taxonomy.md
  "what we chose not to build") [e.g. no multi-turn dialogue state, no multi-label
  intents, no fine-tuning — budget/data/time tradeoffs]

## 2. Results vs. baselines
| | Trivial baseline | Simple baseline | Our system |
|---|---|---|---|
| Intent accuracy | [majority class] | [keyword-based] | [LLM few-shot] |
| Escalation precision/recall | [always auto-handle] | [rule-based] | [full policy] |
| Reply quality (LLM judge, mean overall) | [canned reply] | [template reply] | [grounded generation] |

Judge-human agreement: [kappa from eval/human_agreement.py] — interpret honestly:
if kappa is low, say so and discount the judge-based numbers accordingly.

## 3. Failure analysis (top 5, with real examples)
1. [Failure mode] — example tweet: "..." — hypothesis: [why this happens]
2. ...
3. ...
4. ...
5. ...

## 4. What is misleading about my headline number?
[Mandatory section. Be genuinely self-critical. Candidates to consider:
- golden set size (150-250) means confidence intervals are wide, especially per-intent
- synthetic/seed data used for the TF-IDF baseline's training set is tiny and
  hand-written, not representative
- LLM judge may share blind spots with the LLM that drafted the reply (same model
  family grading its own homework)
- "accuracy" on an imbalanced intent distribution can hide poor performance on
  rare-but-important intents like security_incident
- reproducing results depends on a specific local model version (Ollama) with its
  own version drift]

## 5. What I'd do with one more week
- Swap TF-IDF retrieval for real sentence embeddings.
- Expand golden set, stratify explicitly by intent, add inter-annotator agreement
  if a second labeler is available.
- Fine-tune the TF-IDF/LogisticRegression baseline (or a small model) on the golden
  set itself once it's large enough, as a stronger "simple" baseline.
- Handle multi-turn threads, not just single tweet-reply pairs.
- [your ideas]

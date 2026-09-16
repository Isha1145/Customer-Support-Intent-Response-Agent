# Decision log

Non-obvious decisions made and why. Fill in as you go — this is much easier to write
honestly in real time than to reconstruct after the fact.

1. **Brand: AdobeCare.** Software company per the assignment brief; high volume in the
   dataset; mixes low-risk (how-to) and high-risk (billing, security) intents, which
   makes the escalation policy meaningful rather than trivial.
2. **Local model via Ollama, not a hosted API.** [why — cost/offline/privacy — fill in]
3. **TF-IDF retrieval instead of neural embeddings.** No access to huggingface.co in
   the dev environment; documented as a "next week" improvement rather than silently
   shipping a weaker system.
4. **One primary intent per message, no multi-label.** Keeps golden-set labeling
   tractable in the 150-250 example budget; documented as a known limitation.
5. **`security_incident` is a hard-escalate intent regardless of classifier
   confidence.** [why — cost of a miss vs. cost of an unnecessary escalation]
6. **Escalation keyword list is a blunt instrument on top of the classifier**, not a
   replacement for it. [why]
7. **Golden set sampled randomly, not stratified by intent**, because [fill in —
   did you check the raw intent distribution first? if skewed, say why you did or
   didn't correct for it]
8. **[Your decision]**
9. **[Your decision]**
10. **[Your decision]**

<!-- Aim for 10-15 total. Good candidates: your confidence threshold value, why you
     used LogisticRegression + TF-IDF for the "simple" baseline, how you handled
     multi-turn threads vs single tweet-reply pairs, what counts as a "resolved"
     historical thread for retrieval, why you picked your specific golden-set size
     within 150-250, how you handled tweets with no reply in the raw data, etc. -->

"""
Escalation decision. Deliberately simple and auditable (a plain rule stack, not a
learned model) — for a decision that gates human review, "explainable and wrong 5%
of the time in an obvious way" beats "opaque and wrong 3% of the time invisibly."
"""
from src import config


def should_escalate(text: str, intent: str, confidence: float) -> dict:
    text_lower = text.lower()

    if intent in config.HARD_ESCALATE_INTENTS:
        return {
            "escalate": True,
            "reason": f"intent '{intent}' is always escalated regardless of confidence",
        }

    hit_keywords = [kw for kw in config.ESCALATION_KEYWORDS if kw in text_lower]
    if hit_keywords:
        return {
            "escalate": True,
            "reason": f"message contains escalation keyword(s): {hit_keywords}",
        }

    if confidence < config.AUTO_HANDLE_CONFIDENCE_THRESHOLD:
        return {
            "escalate": True,
            "reason": (
                f"classifier confidence {confidence:.2f} is below threshold "
                f"{config.AUTO_HANDLE_CONFIDENCE_THRESHOLD}"
            ),
        }

    return {
        "escalate": False,
        "reason": f"intent '{intent}' with confidence {confidence:.2f} is safe to auto-handle",
    }

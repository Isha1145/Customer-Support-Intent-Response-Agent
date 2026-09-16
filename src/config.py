"""Central config. Change these rather than hunting through the codebase."""

# --- Local LLM (Ollama) ---
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"          # swap for "phi3", "mistral", etc. if you use a different one
OLLAMA_TIMEOUT_S = 180

# --- Intents ---
INTENTS = [
    "bug_crash",
    "billing_dispute",
    "account_access",
    "security_incident",
    "how_to",
    "subscription_mgmt",
    "feedback_praise",
]

# Intents that must NEVER be auto-handled, regardless of classifier confidence.
HARD_ESCALATE_INTENTS = {"security_incident"}

# Confidence threshold below which we escalate even for "safe" intents.
AUTO_HANDLE_CONFIDENCE_THRESHOLD = 0.65

# Keywords that force escalation regardless of intent/confidence (legal/safety signal).
ESCALATION_KEYWORDS = [
    "sue", "lawsuit", "lawyer", "legal action", "hacked", "leaked",
    "unauthorized", "fraud", "data breach", "gdpr", "police",
]

# --- Retrieval ---
TOP_K_RETRIEVAL = 3

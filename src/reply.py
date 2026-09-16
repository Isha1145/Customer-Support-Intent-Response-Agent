from src.llm_client import generate

REPLY_SYSTEM = """You are AdobeCare, Adobe's customer support account on Twitter.
Write ONE short reply (under 280 characters) in AdobeCare's real voice: warm, brief,
action-oriented, often asking the customer to DM specific details.
You MUST base your reply on the pattern shown in the retrieved past resolutions,
not on general knowledge, and you must not invent policy, refund amounts, or facts
not present in the retrieved examples or the current message.
If nothing retrieved is genuinely relevant, say you'll need to look into it and ask
the customer to DM account details, rather than guessing."""


def draft_reply(customer_text: str, retrieved: list[dict]) -> str:
    context = "\n".join(
        f'- Similar past issue: "{r["customer_text"]}" -> AdobeCare replied: "{r["brand_reply_text"]}"'
        for r in retrieved
    )
    prompt = f"""Past resolved examples:
{context}

Current customer tweet: "{customer_text}"

Draft AdobeCare's reply."""
    return generate(prompt, system=REPLY_SYSTEM, temperature=0.3)

def contains_injection_attempt(text: str) -> bool:
    """Heuristic check for obvious prompt-injection phrasing in untrusted text
    (README content, user messages) before it's passed to an LLM.

    This is a best-effort keyword match, not a security boundary: it only
    catches exact English phrasing and is easily bypassed by rephrasing,
    other languages, or splitting a phrase across lines. The real defense
    is that untrusted text is always treated as data inside the prompt,
    never as instructions — this check just filters the obvious cases
    before they reach the model.
    """
    suspicious_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore the above instructions",
        "disregard the above",
        "disregard previous instructions",
        "new instructions:",
        "system prompt:",
        "you are now",
        "you have full access",
        "you have been authenticated",
        "already been authenticated",
        "hack the system",
        "steal user data",
    ]
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in suspicious_phrases)

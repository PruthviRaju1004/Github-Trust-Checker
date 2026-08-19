def route(message: str) -> str:
    trust_keywords = ["maintained", "active", "stable", "production", "trustworthy", "reliable", "abandoned", "safe to use"]  # fill in some words/phrases
    message_lower = message.lower()
    for keyword in trust_keywords:
        if keyword in message_lower:
            return "trust"

    return "qa"

# if __name__ == "__main__":
#     result = route("Is it well maintained")
#     print(result)

#     result2 = route("how do I install this")
#     print(result2)
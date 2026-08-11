def generate_reply(message: str) -> str:
    cleaned = message.strip()

    if not cleaned:
        return "Send a short update and I’ll help shape it into a team-friendly note."

    if len(cleaned) < 40:
        return f"Thanks for the update. A concise next step would be: {cleaned.capitalize()}."

    return (
        "Acknowledged. The key points are clear, and the next best move is to "
        "turn this into a short status update for the team."
    )

def format_response(
    title: str,
    explanation: str,
    note: str | None = None
) -> str:
    """
    Formats chatbot responses into a consistent, demo-safe structure
    with a natural explanatory flow.
    """

    response = f"""{title}

Explanation:
{explanation}
""".strip()

    if note:
        response += f"""

Note:
{note}
""".rstrip()

    return response

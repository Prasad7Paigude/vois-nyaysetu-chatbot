# query_quality.py

GENERIC_PHRASES = {
    "help",
    "legal help",
    "legal issue",
    "problem",
    "need help",
    "what should i do",
    "law help"
}

LEGAL_ANCHORS = {
    "fir",
    "rti",
    "bail",
    "legal notice",
    "ipc",
    "crpc",
    "law",
    "section",
    "offence",
    "police",
    "court",
    "arrest",
    "arrested",
    "custody",
    "detained",
    "jail"
}



def is_vague_query(user_query: str) -> dict:
    query = user_query.lower().strip()

    # Rule 1: Too short AND no legal anchor
    if len(query.split()) < 4 and not any(anchor in query for anchor in LEGAL_ANCHORS):
        return {
            "is_vague": True,
            "reason": "Query is too short and lacks legal context."
        }

    # Rule 2: Generic phrases only
    if query in GENERIC_PHRASES:
        return {
            "is_vague": True,
            "reason": "Query is too generic and lacks legal context."
        }

    # Rule 3: No legal anchors
    if not any(anchor in query for anchor in LEGAL_ANCHORS):
        return {
            "is_vague": True,
            "reason": "Query lacks identifiable legal or document references."
        }

    return {
        "is_vague": False,
        "reason": None
    }

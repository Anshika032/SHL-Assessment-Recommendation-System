BLOCKED_TOPICS = [
    "politics",
    "religion",
    "violence",
    "legal advice",
    "medical advice",
    "ignore instructions",
    "bypass",
    "hack",
    "jailbreak"
]


def is_blocked_query(query):

    query_lower = query.lower()

    for topic in BLOCKED_TOPICS:

        if topic in query_lower:
            return True

    return False
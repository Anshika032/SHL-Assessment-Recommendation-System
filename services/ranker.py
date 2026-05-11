TECH_KEYWORDS = [
    "coding",
    "technical",
    "developer",
    "programming",
    "software",
    "java",
    "backend",
    "engineering"
]

BEHAVIORAL_KEYWORDS = [
    "behavior",
    "personality",
    "situational",
    "leadership",
    "communication"
]

INVALID_RECOMMENDATIONS = [
    "go digital",
    "deliver a superior experience",
    "report",
    "guide",
    "overview",
    "brochure",
    "solution"
]


def score_result(query, item):

    score = 0

    text = (
        item["name"] + " " +
        item["description"]
    ).lower()

    query_lower = query.lower()

    # remove noisy pages
    for invalid in INVALID_RECOMMENDATIONS:

        if invalid in text:
            return -100

    # technical scoring
    for keyword in TECH_KEYWORDS:

        if keyword in query_lower and keyword in text:
            score += 3

    # behavioral scoring
    for keyword in BEHAVIORAL_KEYWORDS:

        if keyword in query_lower and keyword in text:
            score += 3

    # prioritize coding simulations
    if "coding" in text:
        score += 2

    # prioritize technical assessments
    if "technical" in text:
        score += 2

    # prioritize SJT for behavioral
    if "situational" in text:
        score += 1

    return score


def rerank_results(
    query,
    results
):

    scored = []

    for item in results:

        score = score_result(
            query,
            item
        )

        # skip invalid/noisy pages
        if score < 0:
            continue

        scored.append(
            (score, item)
        )

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        item for score, item in scored
    ]
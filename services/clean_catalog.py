import json
import re

INPUT_PATH = "data/raw/catalog.json"
OUTPUT_PATH = "data/processed/clean_catalog.json"


INVALID_KEYWORDS = [
    "report",
    "reports",
    "guide",
    "guides",
    "whitepaper",
    "ebook",
    "brochure",
    "overview",
    "catalog",
    "about",
    "solutions",
    "news",
    "article",
    "blog",
    "development report"
]


def clean_text(text):

    if not text:
        return ""

    # remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # remove repeated footer/navigation text
    blacklist_phrases = [
        "Explore SHL’s Wide Range of Solutions",
        "Company About SHL",
        "Support chat",
        "Cookie Policy",
        "Privacy Notice",
        "Site Search",
        "Request a Demo",
        "Contact Us",
        "SHL Products"
    ]

    for phrase in blacklist_phrases:
        text = text.replace(phrase, "")

    return text.strip()


def is_valid_assessment(item):

    name = item.get("name", "")
    url = item.get("url", "")

    if not name:
        return False

    lower_name = name.lower()

    # remove reports / guides / articles etc.
    for keyword in INVALID_KEYWORDS:

        if keyword in lower_name:
            return False

    # only keep real assessment URLs
    valid_url_patterns = [
        "/products/assessments/"
    ]

    if not any(
        pattern in url
        for pattern in valid_url_patterns
    ):
        return False

    return True


def normalize_item(item):

    description = clean_text(
        item.get("description", "")
    )

    raw_text = clean_text(
        item.get("raw_text", "")
    )

    return {
        "name": item.get("name"),
        "url": item.get("url"),
        "description": description,
        "content": raw_text[:4000]
    }


def main():

    with open(
        INPUT_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    cleaned = []

    seen_urls = set()

    for item in data:

        if not is_valid_assessment(item):
            continue

        url = item.get("url")

        if url in seen_urls:
            continue

        seen_urls.add(url)

        cleaned.append(
            normalize_item(item)
        )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Cleaned assessments: {len(cleaned)}"
    )


if __name__ == "__main__":
    main()
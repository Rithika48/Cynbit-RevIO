
import re

# Words or phrases indicating urgent complaints
high_urgency_keywords = [
    "immediately",
    "urgent",
    "refund",
    "fraud",
    "scam",
    "unsafe",
    "dangerous",
    "three times",
    "no response"
]

medium_urgency_keywords = [
    "damaged",
    "broken",
    "late",
    "delayed",
    "rude",
    "poor",
    "bad",
    "complaint"
]


def detect_urgency(review, rating=None):
    review = review.lower()

    # Search for high-urgency phrases
    for keyword in high_urgency_keywords:
        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            review
        ):
            return "High"

    # Search for medium-urgency phrases
    for keyword in medium_urgency_keywords:
        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            review
        ):
            return "Medium"

    # Low ratings indicate at least medium urgency
    if rating is not None and rating <= 2:
        return "Medium"

    return "Low"


# Test examples
if __name__ == "__main__":
    reviews = [
        ("The delivery was slightly late", 3),
        ("The product arrived damaged", 2),
        ("I want a refund immediately", 1),
        ("I have complained three times and nobody responded", 1),
        ("Excellent service and friendly staff", 5)
    ]

    for review, rating in reviews:
        print("Review:", review)
        print("Rating:", rating)
        print("Urgency:", detect_urgency(review, rating))
        print("-" * 50)

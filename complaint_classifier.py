
import re

# Keywords associated with each complaint category
complaint_keywords = {
    "Delivery": [
        "delivery", "delayed", "late", "shipping",
        "courier", "package"
    ],
    "Customer Service": [
        "staff", "rude", "support", "service",
        "employee", "response", "help"
    ],
    "Product Quality": [
        "damaged", "broken", "defective",
        "quality", "faulty", "product"
    ],
    "Pricing": [
        "price", "expensive", "cost",
        "overpriced", "charges", "refund"
    ]
}

def classify_complaint(review):
    # Convert review into lowercase words
    words = set(re.findall(r"\b\w+\b", review.lower()))

    # Count matching keywords for each category
    scores = {}

    for category, keywords in complaint_keywords.items():
        scores[category] = sum(
            1 for keyword in keywords if keyword in words
        )

    # Return all categories with matching keywords
    matched = [
        category
        for category, score in scores.items()
        if score > 0
    ]

    if not matched:
        return ["Other"]

    return matched


# Test the classifier
if __name__ == "__main__":
    reviews = [
        "The delivery was very late",
        "The staff were rude",
        "The product arrived damaged",
        "The price is too expensive",
        "Delivery was late and the product was damaged"
    ]

    for review in reviews:
        print("Review:", review)
        print("Complaint Categories:", classify_complaint(review))
        print("-" * 50)


def generate_response(review, sentiment, categories):
    """
    Generate a professional customer response draft.
    This is a rule-based prototype, not an LLM.
    """

    if sentiment == "Positive":
        return (
            "Thank you for your positive feedback! "
            "We are glad you had a good experience "
            "and look forward to serving you again."
        )

    if sentiment == "Neutral":
        return (
            "Thank you for sharing your feedback. "
            "We appreciate your time and will continue "
            "working to improve our services."
        )

    category_responses = {
        "Delivery": (
            "We apologize for the inconvenience caused "
            "by your delivery experience. Our team would "
            "like to review the issue and assist you."
        ),
        "Customer Service": (
            "We are sorry to hear about your experience "
            "with our customer service. We take your "
            "feedback seriously and would like to investigate."
        ),
        "Product Quality": (
            "We apologize for the product quality issue. "
            "Please contact our support team so we can "
            "review the concern and discuss a resolution."
        ),
        "Pricing": (
            "Thank you for sharing your concerns about "
            "pricing. We appreciate your feedback and "
            "will review it with the relevant team."
        )
    }

    for category in categories:
        if category in category_responses:
            return category_responses[category]

    return (
        "We are sorry to hear about your experience. "
        "Thank you for bringing this to our attention. "
        "Please contact our support team so we can assist you."
    )


if __name__ == "__main__":
    review = "The delivery was late and the product was damaged"

    response = generate_response(
        review,
        "Negative",
        ["Delivery", "Product Quality"]
    )

    print("Customer Review:", review)
    print("Suggested Response:", response)

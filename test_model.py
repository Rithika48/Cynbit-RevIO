
import joblib

# Load the previously trained model
model = joblib.load("models/sentiment_model.pkl")

# New customer reviews
reviews = [
    "Excellent product and friendly staff",
    "The delivery was late and the product was damaged",
    "The experience was average",
    "Very poor customer service"
]

# Predict sentiment for each review
predictions = model.predict(reviews)

for review, sentiment in zip(reviews, predictions):
    print("Review:", review)
    print("Predicted Sentiment:", sentiment)
    print("-" * 50)


import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# Load the labeled training dataset
df = pd.read_csv("data/training_reviews.csv")

X = df["review_text"]
y = df["sentiment"]

# Separate training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# Create sentiment classification pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        lowercase=True
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

# Train only on the training portion
model.fit(X_train, y_train)

# Evaluate on unseen test examples
predictions = model.predict(X_test)

print("Model Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    zero_division=0
))

# Save the model
joblib.dump(model, "models/sentiment_model.pkl")

print("\nModel saved successfully!")

# Additional manual checks
sample_reviews = [
    "Very poor customer service",
    "Excellent product and friendly staff",
    "The experience was average"
]

for review in sample_reviews:
    print(review, "->", model.predict([review])[0])

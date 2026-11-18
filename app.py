from response_generator import generate_response
import pandas as pd
import streamlit as st
import joblib

from complaint_classifier import classify_complaint
from urgency_detector import detect_urgency
from crisis_detector import detect_crises

st.set_page_config(
    page_title="Revio AI Review Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("Revio AI Review Intelligence")
st.caption("Cynbit AI/ML Engineer Intern Assessment - Prototype")

# Load trained sentiment model
@st.cache_resource
def load_model():
    return joblib.load("models/sentiment_model.pkl")

model = load_model()

st.sidebar.header("Review Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload customer reviews CSV",
    type=["csv"]
)

# Use sample data when no file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.info("Analyzing uploaded review data.")
else:
    df = pd.read_csv("data/reviews.csv")
    st.info("Showing synthetic demonstration data.")

required_columns = {
    "review_id", "date", "branch", "rating", "review_text"
}

if not required_columns.issubset(df.columns):
    st.error("CSV must contain review_id, date, branch, rating and review_text.")
    st.stop()

df = df.dropna(
    subset=["date", "branch", "rating", "review_text"]
).copy()

df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.dropna(subset=["rating", "date"])

if df.empty:
    st.warning("No valid reviews found.")
    st.stop()

# Analyze reviews
df["Sentiment"] = model.predict(
    df["review_text"].astype(str)
)

df["Complaint Categories"] = df.apply(
    lambda row: ", ".join(
        classify_complaint(str(row["review_text"]))
    ) if row["rating"] <= 2 else "Not flagged",
    axis=1
)

df["Urgency"] = df.apply(
    lambda row: detect_urgency(
        str(row["review_text"]), row["rating"]
    ),
    axis=1
)

# Dashboard metrics
total_reviews = len(df)
negative_reviews = (df["rating"] <= 2).sum()
average_rating = df["rating"].mean()
high_urgency = (df["Urgency"] == "High").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", total_reviews)
col2.metric("Negative Ratings", int(negative_reviews))
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("High Urgency", int(high_urgency))

st.divider()

# Sentiment visualization
st.subheader("Sentiment Distribution")
st.bar_chart(df["Sentiment"].value_counts())

# Branch rating comparison
st.subheader("Average Rating by Branch")
branch_ratings = df.groupby("branch")["rating"].mean()
st.bar_chart(branch_ratings)

# Crisis detection
st.subheader("Branch-Level Crisis Alerts")

alerts = detect_crises(df)

if alerts.empty:
    st.success("No review crisis detected using the current threshold.")
else:
    st.error("Potential review crisis detected!")
    st.dataframe(alerts, use_container_width=True)

# Review details
st.subheader("Customer Review Analysis")

st.dataframe(
    df[[
        "date",
        "branch",
        "rating",
        "review_text",
        "Sentiment",
        "Complaint Categories",
        "Urgency"
    ]],
    use_container_width=True
)

# Single review prediction
st.divider()
st.subheader("Analyze a New Customer Review")

review_input = st.text_area(
    "Enter customer feedback"
)

rating_input = st.slider(
    "Customer Rating",
    min_value=1,
    max_value=5,
    value=3
)


if st.button("Analyze Review"):
    if review_input.strip():
        sentiment = model.predict([review_input])[0]
        categories = classify_complaint(review_input)

        urgency = detect_urgency(
            review_input, rating_input
        )

        st.write("**Predicted Sentiment:**", sentiment)

        st.write(
        "**Detected Review Topics:**",
        ", ".join(categories)
        )

        st.write("**Urgency Level:**", urgency)

        # Generate customer response
        response = generate_response(
            review_input,
            sentiment,
            categories
        )

        st.subheader("Suggested Customer Response")
        st.info(response)

        st.caption(
            "Template-generated draft. "
            "Requires human review before sending."
        )

    else:
        st.warning("Please enter a review.")

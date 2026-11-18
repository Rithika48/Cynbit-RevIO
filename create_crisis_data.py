
import pandas as pd

reviews = []
review_id = 1

# Historical data: one negative review per day
for day in range(1, 8):
    reviews.append({
        "review_id": review_id,
        "date": f"2026-11-{day:02d}",
        "branch": "Bengaluru",
        "rating": 2,
        "review_text": "Delivery was late"
    })
    review_id += 1

    reviews.append({
        "review_id": review_id,
        "date": f"2026-11-{day:02d}",
        "branch": "Bengaluru",
        "rating": 5,
        "review_text": "Excellent service"
    })
    review_id += 1

# Simulate a sudden increase in negative reviews
for i in range(6):
    reviews.append({
        "review_id": review_id,
        "date": "2026-11-08",
        "branch": "Bengaluru",
        "rating": 1,
        "review_text": "Very poor service and delayed delivery"
    })
    review_id += 1

df = pd.DataFrame(reviews)

df.to_csv("data/crisis_demo.csv", index=False)

print("Crisis demonstration dataset created!")
print("Total reviews:", len(df))

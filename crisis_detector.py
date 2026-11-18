
import pandas as pd


def detect_crises(df):
    required = {"branch", "date", "rating"}
    if not required.issubset(df.columns):
        raise ValueError("Dataset must contain branch, date and rating")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df["is_negative"] = df["rating"] <= 2

    alerts = []

    for branch, group in df.groupby("branch"):
        # Count negative reviews for each date
        daily = group.groupby("date")["is_negative"].sum()

        # Include dates with zero negative reviews
        all_dates = pd.date_range(
            group["date"].min(),
            group["date"].max(),
            freq="D"
        )
        daily = daily.reindex(all_dates, fill_value=0)

        # Require at least 4 days of data
        if len(daily) < 4:
            continue

        history = daily.iloc[:-1]
        current_count = int(daily.iloc[-1])
        baseline = history.mean()

        # Flag at least 3 negative reviews and
        # at least twice the historical average
        threshold = max(3, baseline * 2)

        if current_count >= threshold:
            alerts.append({
                "branch": branch,
                "date": daily.index[-1].date(),
                "negative_reviews": current_count,
                "historical_average": round(baseline, 2),
                "alert": "Potential Review Crisis"
            })

    return pd.DataFrame(
        alerts,
        columns=[
            "branch",
            "date",
            "negative_reviews",
            "historical_average",
            "alert"
        ]
    )


if __name__ == "__main__":
    df = pd.read_csv("data/reviews.csv")
    alerts = detect_crises(df)

    if alerts.empty:
        print("No review crisis detected.")
    else:
        print("Crisis Alerts:")
        print(alerts.to_string(index=False))

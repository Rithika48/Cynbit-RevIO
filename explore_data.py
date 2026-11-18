
import pandas as pd

# Load customer reviews
df = pd.read_csv("data/reviews.csv")

# Display the first five reviews
print("First five customer reviews:")
print(df.head())

# Display the number of reviews
print("\nTotal reviews:", len(df))

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Display average rating by branch
print("\nAverage rating by branch:")
print(df.groupby("branch")["rating"].mean())

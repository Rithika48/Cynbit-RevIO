
import pandas as pd
from crisis_detector import detect_crises

df = pd.read_csv("data/crisis_demo.csv")

alerts = detect_crises(df)

if alerts.empty:
    print("No crisis detected.")
else:
    print("Crisis Detected!")
    print(alerts.to_string(index=False))

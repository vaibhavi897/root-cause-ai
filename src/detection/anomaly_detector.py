import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(file_path):
    # Load data
    df = pd.read_csv(file_path)

    # Drop non-numeric column
    features = df.drop(columns=["timestamp", "is_anomaly"], errors='ignore')

    # Train Isolation Forest
    model = IsolationForest(contamination=0.02, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    # Convert labels: -1 → anomaly, 1 → normal
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

    return df


if __name__ == "__main__":
    file_path = "data/synthetic_data.csv"

    df = detect_anomalies(file_path)

    # Save output
    df.to_csv("data/detected_data.csv", index=False)

    print("Anomaly detection complete. Saved to data/detected_data.csv")

    # Quick evaluation (since we have ground truth)
    if "is_anomaly" in df.columns:
        correct = (df["anomaly"] == df["is_anomaly"]).sum()
        total = len(df)
        accuracy = correct / total

        print(f"Detection Accuracy: {accuracy:.2f}")
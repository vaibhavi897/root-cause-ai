import pandas as pd
import numpy as np

def generate_synthetic_data(n_points=500):
    np.random.seed(42)

    timestamps = pd.date_range(start="2024-01-01", periods=n_points, freq="H")

    # Base features
    traffic = np.random.normal(50, 10, n_points)
    humidity = np.random.normal(60, 5, n_points)
    wind = np.random.normal(10, 2, n_points)

    # Pollution depends on traffic and wind
    pollution = (
        0.6 * traffic +
        0.3 * humidity -
        0.5 * wind +
        np.random.normal(0, 5, n_points)
    )

    df = pd.DataFrame({
        "timestamp": timestamps,
        "traffic": traffic,
        "humidity": humidity,
        "wind": wind,
        "pollution": pollution
    })

    return df


def inject_anomalies(df, n_anomalies=10):
    df = df.copy()

    anomaly_indices = np.random.choice(len(df), n_anomalies, replace=False)

    for idx in anomaly_indices:
        # Inject spike in traffic and drop in wind
        df.loc[idx, "traffic"] *= np.random.uniform(1.5, 2.0)
        df.loc[idx, "wind"] *= np.random.uniform(0.3, 0.6)

        # Recalculate pollution spike
        df.loc[idx, "pollution"] = (
            0.6 * df.loc[idx, "traffic"] +
            0.3 * df.loc[idx, "humidity"] -
            0.5 * df.loc[idx, "wind"] +
            np.random.normal(10, 3)
        )

    df["is_anomaly"] = 0
    df.loc[anomaly_indices, "is_anomaly"] = 1

    return df


if __name__ == "__main__":
    df = generate_synthetic_data()
    df = inject_anomalies(df)

    df.to_csv("data/synthetic_data.csv", index=False)
    print("Dataset generated and saved to data/synthetic_data.csv")
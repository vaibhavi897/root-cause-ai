import pandas as pd


def explain_anomaly(file_path, top_n=3):
    # Load data
    df = pd.read_csv(file_path)

    # Separate anomalies and normal data
    anomalies = df[df["anomaly"] == 1]
    normal = df[df["anomaly"] == 0]

    # Drop non-feature columns
    feature_cols = ["traffic", "humidity", "wind", "pollution"]

    explanations = []

    # Compute normal baseline
    normal_mean = normal[feature_cols].mean()

    for idx, row in anomalies.iterrows():
        anomaly_values = row[feature_cols]

        # Difference from normal
        diff = anomaly_values - normal_mean

        # Absolute contribution
        contribution = diff.abs().sort_values(ascending=False)

        # Top features causing anomaly
        top_features = contribution.head(top_n).index.tolist()
        details_dict = diff[top_features].to_dict()
        sentence = generate_sentence(top_features, details_dict)
        
        explanation = {
            "timestamp": row["timestamp"],
            "top_causes": top_features,
            "details": details_dict,
            "summary": sentence
       }

        explanations.append(explanation)

    return explanations

def generate_sentence(top_features, details):
    sentence = "Anomaly likely caused by "

    phrases = []

    for feature in top_features:
        value = details[feature]

        if value > 0:
            phrases.append(f"increased {feature}")
        else:
            phrases.append(f"decreased {feature}")

    sentence += " and ".join(phrases)
    return sentence

if __name__ == "__main__":
    file_path = "data/detected_data.csv"

    results = explain_anomaly(file_path)

    for res in results[:5]:  # print first 5
        print("\n--- Anomaly ---")
        print(f"Time: {res['timestamp']}")
        print(f"Top Causes: {res['top_causes']}")
        print(f"Details: {res['details']}")
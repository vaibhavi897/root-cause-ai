import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import os

from src.detection.anomaly_detector import detect_anomalies
from src.explanation.root_cause import explain_anomaly

st.set_page_config(page_title="Root Cause AI", layout="wide")

st.title("🧠 Root Cause AI Dashboard")
st.markdown("Detect anomalies and understand *why* they happen.")

# Sidebar
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

if uploaded_file:
    file_path = "data/uploaded.csv"

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load data
    df = pd.read_csv(file_path)

    st.subheader("📊 Dataset Overview")

    col1, col2 = st.columns(2)
    col1.metric("Total Rows", len(df))
    col2.metric("Features", len(df.columns))

    st.dataframe(df.head())

    # Plot
    st.subheader("📈 Pollution Trend")
    fig = px.line(df, x="timestamp", y="pollution")
    st.plotly_chart(fig, use_container_width=True)

    # Buttons
    col3, col4 = st.columns(2)

    # 🚨 Detection
    if col3.button("🚨 Run Detection"):
        df_detected = detect_anomalies(file_path)

        output_path = "data/output.csv"
        df_detected.to_csv(output_path, index=False)

        st.success("Anomaly detection completed")

        fig2 = px.scatter(
            df_detected,
            x="timestamp",
            y="pollution",
            color=df_detected["anomaly"].map({0: "Normal", 1: "Anomaly"}),
        )

        st.plotly_chart(fig2, use_container_width=True)

    # 🧠 Explanation
    if col4.button("🧠 Explain Anomalies"):
        output_path = "data/output.csv"

        if not os.path.exists(output_path):
            st.warning("⚠️ Please run detection first!")
        else:
            results = explain_anomaly(output_path)

            st.subheader("🔍 Root Cause Analysis")

            for exp in results:
                with st.container():
                    st.markdown(f"### ⏱ {exp['timestamp']}")
                    st.markdown(f"**Top Causes:** {', '.join(exp['top_causes'])}")

                    # ✅ safe summary handling
                    if "summary" in exp:
                        st.success(exp["summary"])

                    st.json(exp["details"])
                    st.markdown("---")
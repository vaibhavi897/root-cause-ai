from fastapi import FastAPI, UploadFile, File
import pandas as pd
import shutil
import os

from src.detection.anomaly_detector import detect_anomalies
from src.explanation.root_cause import explain_anomaly

app = FastAPI()

UPLOAD_PATH = "data/uploaded.csv"
OUTPUT_PATH = "data/output.csv"


@app.get("/")
def home():
    return {"message": "Root Cause AI API is running 🚀"}


# 1️⃣ Upload dataset
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully"}


# 2️⃣ Detect anomalies
@app.get("/detect")
def detect():
    df = detect_anomalies(UPLOAD_PATH)
    df.to_csv(OUTPUT_PATH, index=False)

    return {
        "message": "Anomaly detection completed",
        "total_rows": len(df),
        "anomalies_detected": int(df["anomaly"].sum())
    }


# 3️⃣ Explain anomalies
@app.get("/explain")
def explain():
    results = explain_anomaly(OUTPUT_PATH)

    return {
        "total_anomalies": len(results),
        "explanations": results[:5]  # limit for response
    }
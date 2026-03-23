#  Root Cause AI

An AI-powered system that not only detects anomalies in time-series data but also explains WHY they occur.

---

##  Features

- 📊 Detect anomalies using Isolation Forest
- 🧠 Root cause analysis using feature deviation
- 📈 Interactive dashboard (Streamlit)
- ⚡ Real-time explanation generation

---

##  Tech Stack

- Python
- Pandas, NumPy, Scikit-learn
- Streamlit
- Plotly

---

##  How It Works

1. Upload dataset  
2. Detect anomalies  
3. Compare with normal data  
4. Identify top contributing features  
5. Generate explanation  

---

##  Example Output

> "Anomaly likely caused by increased traffic and decreased wind."

---

## ▶ Run Locally

```bash
git clone https://github.com/vaibhavi897/root-cause-ai.git
cd root-cause-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

set PYTHONPATH=.
streamlit run app/streamlit_app.py
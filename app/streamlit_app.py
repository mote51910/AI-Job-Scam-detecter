import streamlit as st
import requests

st.set_page_config(page_title="AI Job Scam Detector", page_icon="🛡️", layout="centered")

st.title("🛡️ AI Job Scam & Risk Detector")
st.write("Paste a job posting below to check if it looks like a scam.")

try:
    API_URL = st.secrets.get("API_URL", "https://ai-job-scam-detecter.onrender.com/predict")
except Exception:
    API_URL = "https://ai-job-scam-detecter.onrender.com/predict"

job_text = st.text_area(
    "Job Posting Text",
    height=250,
    placeholder="Paste the full job description, salary, company info, contact email here...",
)

if st.button("Analyze", type="primary"):
    if not job_text.strip():
        st.warning("Please paste a job posting first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post("https://ai-job-scam-detecter.onrender.com/predict", json=data, timeout=60)
                result = response.json()

                score = result['risk_score']
                label = result['label']

                if label == "High Risk":
                    st.error(f"🚨 {label} — {score}% scam probability")
                elif label == "Suspicious":
                    st.warning(f"⚠️ {label} — {score}% scam probability")
                else:
                    st.success(f"✅ {label} — {score}% scam probability")

                st.progress(int(score))

                st.subheader("Why this score?")
                for reason in result['reasons']:
                    st.write(f"- {reason}")

            except Exception as e:
                st.error(f"Error contacting API: {e}")

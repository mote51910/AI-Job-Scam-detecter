# AI Job Scam & Risk Detector

Detects whether a job posting is likely a scam using an ML model (TF-IDF + Random Forest)
combined with rule-based red-flag detection for explainability.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

## Steps to run

1. Download the "fake job postings" dataset from Kaggle and place it at `data/job_postings.csv`
2. Preprocess the data:
   ```bash
   python src/preprocess.py
   ```
3. Train the model:
   ```bash
   python src/train.py
   ```
4. Test a single prediction:
   ```bash
   python -m src.predict
   ```
5. Start the backend API (keep this terminal open):
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```
6. In a second terminal, start the frontend:
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Run tests

```bash
pytest tests/ -v
```

## Deployment

- Backend: Dockerized, deploy to Render.com or HuggingFace Spaces
- Frontend: Deploy `app/streamlit_app.py` to Streamlit Community Cloud,
  set `API_URL` in secrets to your deployed backend's `/predict` URL.

## Project Structure

```
job-scam-detector/
├── data/            # dataset (not committed)
├── src/             # preprocessing, feature engineering, training, prediction
├── model/           # saved model.pkl and vectorizer.pkl
├── api/             # FastAPI backend
├── app/             # Streamlit frontend
├── tests/           # pytest tests
├── requirements.txt
└── Dockerfile
```

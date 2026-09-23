from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.predict import predict_risk

app = FastAPI(title="AI Job Scam & Risk Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobPosting(BaseModel):
    text: str


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/predict")
def predict(posting: JobPosting):
    result = predict_risk(posting.text)
    return result

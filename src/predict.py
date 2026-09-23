import joblib
from src.preprocess import clean_text
from src.features import get_triggered_reasons, extract_red_flags

model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


def predict_risk(raw_text: str) -> dict:
    cleaned = clean_text(raw_text)
    vec = vectorizer.transform([cleaned])

    ml_prob = model.predict_proba(vec)[0][1]  # probability of scam

    flags = extract_red_flags(raw_text)
    reasons = get_triggered_reasons(raw_text)

    # Blend ML probability with rule-based signal for a final score
    rule_boost = min(flags['red_flag_count'] * 0.08, 0.4)
    final_score = min(ml_prob + rule_boost, 1.0)

    if final_score >= 0.7:
        label = "High Risk"
    elif final_score >= 0.4:
        label = "Suspicious"
    else:
        label = "Likely Safe"

    return {
        "risk_score": round(final_score * 100, 2),
        "label": label,
        "ml_probability": round(ml_prob * 100, 2),
        "reasons": reasons if reasons else ["No major red-flag patterns detected"],
    }


if __name__ == "__main__":
    sample = """Urgent hiring! Earn $5000/week from home, no experience needed.
    Send $50 registration fee to secure your spot. Contact us at hr@gmail.com"""
    print(predict_risk(sample))

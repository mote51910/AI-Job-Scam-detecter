from src.predict import predict_risk


def test_obvious_scam_detected():
    text = "Urgent! Earn $5000/week from home. Pay $50 registration fee. Contact hr@gmail.com"
    result = predict_risk(text)
    assert result['risk_score'] > 40
    assert result['label'] in ["Suspicious", "High Risk"]


def test_legit_posting_lower_score():
    text = """Software Engineer at TechCorp Inc. We are looking for a backend developer
    with 3 years experience in Python. Competitive salary, full benefits, apply via our
    careers portal at careers.techcorp.com."""
    result = predict_risk(text)
    assert result['risk_score'] < 60


def test_output_has_reasons():
    result = predict_risk("Test job posting text")
    assert "reasons" in result
    assert isinstance(result['reasons'], list)

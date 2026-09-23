import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import RandomOverSampler


def main():
    df = pd.read_csv("data/cleaned_data.csv")
    df['clean_text'] = df['clean_text'].fillna("")

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df['clean_text'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
    )

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    # Handle class imbalance (scam postings are rare, ~5%)
    ros = RandomOverSampler(random_state=42)
    X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)

    # Train model
    model = RandomForestClassifier(n_estimators=300, max_depth=25, random_state=42, n_jobs=-1)
    model.fit(X_train_bal, y_train_bal)

    # Evaluate
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    print("=== Classification Report ===")
    print(classification_report(y_test, preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))
    print("ROC-AUC:", roc_auc_score(y_test, probs))

    # Save model + vectorizer
    joblib.dump(model, "model/model.pkl")
    joblib.dump(vectorizer, "model/vectorizer.pkl")
    print("Saved model and vectorizer to /model")


if __name__ == "__main__":
    main()

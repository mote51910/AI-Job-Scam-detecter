import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' urltoken ', text)      # normalize links
    text = re.sub(r'\S+@\S+', ' emailtoken ', text)           # normalize emails
    text = re.sub(r'[^a-z\s]', ' ', text)                     # remove punctuation/numbers
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return " ".join(tokens)


def load_and_prepare(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Combine relevant text columns into one field
    text_cols = ['title', 'company_profile', 'description', 'requirements', 'benefits']
    for col in text_cols:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("")

    df['full_text'] = (
        df['title'] + " " + df['company_profile'] + " " +
        df['description'] + " " + df['requirements'] + " " + df['benefits']
    )
    df['clean_text'] = df['full_text'].apply(clean_text)

    # Label column in the Kaggle dataset is 'fraudulent'
    df['label'] = df['fraudulent'].astype(int)

    return df[['clean_text', 'label', 'full_text']]


if __name__ == "__main__":
    df = load_and_prepare("data/job_postings.csv")
    df.to_csv("data/cleaned_data.csv", index=False)
    print(df['label'].value_counts())
    print("Saved cleaned data to data/cleaned_data.csv")

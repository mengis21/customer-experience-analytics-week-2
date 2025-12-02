import os
import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer


def label_sentiment(text: str):
    if not isinstance(text, str) or not text.strip():
        return (None, None)
    pol = TextBlob(text).sentiment.polarity  # -1..1
    if pol > 0.1:
        label = "positive"
    elif pol < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return (label, pol)


def extract_keywords_per_bank(df: pd.DataFrame, top_n: int = 10):
    out = {}
    for bank, g in df.groupby("bank"):
        texts = g["review"].astype(str).tolist()
        if not texts:
            out[bank] = []
            continue
        vec = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words="english")
        X = vec.fit_transform(texts)
        # average tf-idf across documents
        scores = X.mean(axis=0).A1
        terms = vec.get_feature_names_out()
        top_idx = scores.argsort()[::-1][:top_n]
        out[bank] = [terms[i] for i in top_idx]
    return out


def main():
    in_path = "data/clean_reviews.csv"
    if not os.path.exists(in_path):
        print("Missing cleaned data. Run preprocess.py first.")
        return

    df = pd.read_csv(in_path)

    # Sentiment
    labels = []
    scores = []
    for t in df["review"].astype(str).tolist():
        l, s = label_sentiment(t)
        labels.append(l)
        scores.append(s)
    df["sentiment_label"] = labels
    df["sentiment_score"] = scores

    # Keywords per bank
    kw = extract_keywords_per_bank(df, top_n=10)
    # store a simple string list per bank to join back
    df["keywords"] = df["bank"].map(lambda b: ", ".join(kw.get(b, [])))

    out_path = "data/clean_reviews_enriched.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved enriched dataset: {out_path} (rows={len(df)})")


if __name__ == "__main__":
    main()

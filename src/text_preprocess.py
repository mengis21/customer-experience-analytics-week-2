import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def ensure_nltk():
    try:
        _ = stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')
    try:
        WordNetLemmatizer()
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('omw-1.4')


def clean_text(s: str, sw: set, lem: WordNetLemmatizer) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    toks = [t for t in s.split() if t not in sw]
    toks = [lem.lemmatize(t) for t in toks]
    return " ".join(toks)


def main():
    ensure_nltk()
    in_path = "data/clean_reviews_enriched.csv"
    if not os.path.exists(in_path):
        in_path = "data/clean_reviews.csv"
    if not os.path.exists(in_path):
        print("Missing input CSV. Run previous steps first.")
        return

    df = pd.read_csv(in_path)
    sw = set(stopwords.words('english'))
    lem = WordNetLemmatizer()

    df['review_clean'] = [clean_text(str(x), sw, lem) for x in df.get('review', [])]
    out_path = "data/clean_reviews_enriched.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved with review_clean column: {out_path} (rows={len(df)})")


if __name__ == "__main__":
    main()

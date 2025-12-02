import os
import pandas as pd


def load_raw(paths):
    dfs = []
    for p in paths:
        if os.path.exists(p):
            dfs.append(pd.read_csv(p))
    return dfs


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Keep required cols
    cols = ["review", "rating", "date", "bank", "source"]
    df = df[[c for c in cols if c in df.columns]].copy()

    # Drop duplicates by review text + bank
    df["review"] = df["review"].astype(str).str.strip()
    df = df.drop_duplicates(subset=["review", "bank"]) 

    # Handle missing rating/date
    df = df.dropna(subset=["review"])  # keep non-empty review
    # Normalize date to YYYY-MM-DD
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Coerce rating to int where possible
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("Int64")

    return df


def main():
    os.makedirs("data", exist_ok=True)
    raw_paths = [
        "data/raw_cbe_reviews.csv",
        "data/raw_boa_reviews.csv",
        "data/raw_dashen_reviews.csv",
    ]
    dfs = load_raw(raw_paths)
    if not dfs:
        print("No raw files found. Run scrape_reviews.py first.")
        return

    merged = pd.concat(dfs, ignore_index=True)
    cleaned = clean(merged)
    out = "data/clean_reviews.csv"
    cleaned.to_csv(out, index=False)
    print(f"Saved cleaned dataset: {out} (rows={len(cleaned)})")


if __name__ == "__main__":
    main()

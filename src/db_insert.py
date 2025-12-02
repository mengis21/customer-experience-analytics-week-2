import os
import pandas as pd
from sqlalchemy import create_engine, text


def get_engine():
    # Expected env vars: PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD
    host = os.environ.get("PG_HOST", "localhost")
    port = os.environ.get("PG_PORT", "5432")
    db = os.environ.get("PG_DB", "bank_reviews")
    user = os.environ.get("PG_USER", "postgres")
    pwd = os.environ.get("PG_PASSWORD", "postgres")
    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url)


def upsert_banks(engine, df: pd.DataFrame):
    banks = (
        df[["bank"]]
        .drop_duplicates()
        .rename(columns={"bank": "bank_name"})
    )
    # ensure table exists
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS banks (bank_id SERIAL PRIMARY KEY, bank_name TEXT NOT NULL, app_name TEXT);"))
        for _, row in banks.iterrows():
            conn.execute(text("INSERT INTO banks (bank_name) SELECT :name WHERE NOT EXISTS (SELECT 1 FROM banks WHERE bank_name = :name);"), {"name": row["bank_name"]})


def insert_reviews(engine, df: pd.DataFrame):
    # map bank_name to bank_id
    with engine.begin() as conn:
        res = conn.execute(text("SELECT bank_id, bank_name FROM banks"))
        mapping = {r.bank_name: r.bank_id for r in res}

    rows = []
    for _, r in df.iterrows():
        rows.append({
            "bank_id": mapping.get(r.get("bank")),
            "review_text": r.get("review"),
            "rating": int(r["rating"]) if pd.notna(r.get("rating")) else None,
            "review_date": r.get("date"),
            "sentiment_label": r.get("sentiment_label"),
            "sentiment_score": float(r["sentiment_score"]) if pd.notna(r.get("sentiment_score")) else None,
            "source": r.get("source"),
        })

    reviews_df = pd.DataFrame(rows)
    reviews_df.to_sql("reviews", engine, if_exists="append", index=False)


def main():
    in_path = "data/clean_reviews_enriched.csv"
    if not os.path.exists(in_path):
        print("Missing enriched data. Run enrichment first.")
        return
    df = pd.read_csv(in_path)
    eng = get_engine()
    upsert_banks(eng, df)
    insert_reviews(eng, df)
    print("Inserted reviews into PostgreSQL.")


if __name__ == "__main__":
    main()

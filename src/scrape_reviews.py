import os
import csv
from datetime import datetime
from typing import List, Dict

import pandas as pd
from google_play_scraper import reviews, Sort


def fetch_reviews(app_id: str, lang: str = "en", country: str = "us", count: int = 500) -> List[Dict]:
    result, _ = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count,
        filter_score_with=None,
    )
    return result


def to_rows(records: List[Dict], bank_name: str, source: str = "google_play") -> List[Dict]:
    rows = []
    for r in records:
        rows.append({
            "review": r.get("content", ""),
            "rating": r.get("score", None),
            "date": r.get("at", None),
            "bank": bank_name,
            "source": source,
        })
    return rows


def save_csv(rows: List[Dict], out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df = pd.DataFrame(rows)
    # Normalize date to YYYY-MM-DD for raw export as string
    if "date" in df.columns:
        df["date"] = df["date"].apply(lambda d: d.strftime("%Y-%m-%d") if isinstance(d, datetime) else (str(d)[:10] if d else None))
    df.to_csv(out_path, index=False)


def main():
    # App IDs provided by user
    apps = [
        {"bank": "CBE", "app_id": "com.combanketh.mobilebanking"},
        {"bank": "BOA", "app_id": "com.dashen.dashensuperapp"},
        {"bank": "Dashen", "app_id": "com.dashen.dashensuperapp"},
    ]

    all_counts = {}
    for app in apps:
        bank = app["bank"]
        app_id = app["app_id"]
        print(f"Fetching reviews for {bank} ({app_id})...")
        recs = fetch_reviews(app_id, lang="en", country="us", count=600)
        rows = to_rows(recs, bank_name=bank)
        out_path = f"data/raw_{bank.lower()}_reviews.csv"
        save_csv(rows, out_path)
        all_counts[bank] = len(rows)
        print(f"Saved {len(rows)} rows to {out_path}")

    print("Counts:", all_counts)


if __name__ == "__main__":
    main()

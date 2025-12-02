import os
import pandas as pd


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def main():
    in_path = "data/clean_reviews_enriched.csv"
    if not os.path.exists(in_path):
        print("Missing enriched data. Run sentiment_keywords.py and add_themes.py first.")
        return
    df = pd.read_csv(in_path)
    out_dir = "reports/summaries"
    ensure_dir(out_dir)

    # Mean sentiment by bank
    by_bank = (df.groupby("bank", dropna=False)["sentiment_score"].mean().reset_index())
    by_bank.to_csv(os.path.join(out_dir, "sentiment_by_bank.csv"), index=False)

    # Mean sentiment by rating
    if "rating" in df:
        by_rating = (df.groupby("rating", dropna=False)["sentiment_score"].mean().reset_index().sort_values("rating"))
        by_rating.to_csv(os.path.join(out_dir, "sentiment_score_by_rating.csv"), index=False)

    # Theme counts by bank
    theme_counts = (df.assign(theme=df["themes"].fillna("Other").str.split(", "))
                      .explode("theme")
                      .groupby(["bank", "theme"]).size()
                      .reset_index(name="count"))
    theme_counts.to_csv(os.path.join(out_dir, "themes_by_bank.csv"), index=False)

    # Simple keywords per bank table (top 1 string list)
    kw = df.groupby("bank")["keywords"].first().reset_index()
    kw.to_csv(os.path.join(out_dir, "keywords_by_bank.csv"), index=False)

    print(f"Saved summaries to {out_dir}")


if __name__ == "__main__":
    main()
import os
import pandas as pd


def main():
    in_path = "data/clean_reviews_enriched.csv"
    if not os.path.exists(in_path):
        print("Missing enriched data. Run sentiment_keywords.py and add_themes.py first.")
        return
    os.makedirs("reports/summaries", exist_ok=True)
    df = pd.read_csv(in_path)

    # Sentiment by bank
    s_bank = (
        df.groupby(["bank", "sentiment_label"])  # type: ignore
          .size()
          .reset_index(name="count")
    )
    s_bank.to_csv("reports/summaries/sentiment_by_bank.csv", index=False)

    # Sentiment score by rating bucket (1..5)
    if "rating" in df.columns and "sentiment_score" in df.columns:
        s_rate = (
            df.dropna(subset=["rating"])  # type: ignore
              .groupby(["bank", "rating"])  # type: ignore
              ["sentiment_score"].mean()
              .reset_index()
        )
        s_rate.to_csv("reports/summaries/sentiment_score_by_rating.csv", index=False)

    # Top keywords per bank (as stored string)
    kw = df.groupby("bank")["keywords"].first().reset_index()
    kw.to_csv("reports/summaries/keywords_by_bank.csv", index=False)

    # Themes distribution per bank
    th = (
        df.groupby(["bank", "themes"])  # type: ignore
          .size()
          .reset_index(name="count")
    )
    th.to_csv("reports/summaries/themes_by_bank.csv", index=False)

    print("Saved summaries under reports/summaries/")


if __name__ == "__main__":
    main()

Customer Experience Analytics – Week 2

Overview
- Scrape Google Play reviews for three Ethiopian banks (CBE, BOA, Dashen).
- Clean and prepare data (duplicates, missing, date normalization).
- Provide initial analysis for interim submission.

Project Structure
- `src/scrape_reviews.py`: Scrapes reviews using `google-play-scraper` and saves raw CSVs.
- `src/preprocess.py`: Cleans and merges raw CSVs into `data/clean_reviews.csv`.
- `notebooks/interim_analysis.ipynb`: Quick EDA for counts and rating distribution.
- `src/sentiment_keywords.py`: Adds TextBlob sentiment and TF-IDF keywords to create `clean_reviews_enriched.csv`.
- `src/add_themes.py`: Rule-based themes from keywords/text; updates `themes` column.
- `src/summarize.py`: Saves summaries under `reports/summaries/`.
- `src/text_preprocess.py`: Tokenize/stop-word/lemmatize into `review_clean`.
- `notebooks/final_analysis.ipynb`: Final plots and tables for the report.
- `db/schema.sql`: Postgres schema for banks and reviews.
- `src/db_insert.py`: Insert cleaned data into Postgres (use env vars).
- `src/sentiment_keywords.py`: Adds TextBlob sentiment and TF-IDF keywords; saves `data/clean_reviews_enriched.csv`.
- `src/add_themes.py`: Assigns themes based on keywords; updates enriched CSV with `themes`.
- `src/summarize.py`: Exports summary CSVs to `reports/summaries/`.
- `notebooks/final_analysis.ipynb`: Final plots (sentiment per bank, rating per bank, themes).
- `db/schema.sql`, `src/db_insert.py`: PostgreSQL schema and insertion script.

Setup
1) Clone & Change dirrrectory to the Repo
2) Create/activate a virtual environment.
3) Install dependencies.

Commands 
```
python -m venv .venv

pip install -r requirements.txt
```

Scraping
- You need the Google Play app IDs for:
	- Commercial Bank of Ethiopia (CBE)
	- Bank of Abyssinia (BOA)
	- Dashen Bank
- Run after updating IDs in `src/scrape_reviews.py`.
```
python src/scrape_reviews.py
```

Preprocessing
Enrichment (Sentiment, Keywords, Themes)
```
python src/sentiment_keywords.py
python src/add_themes.py
python src/summarize.py
```

Final Analysis
Open and run `notebooks/final_analysis.ipynb` to generate plots.

PostgreSQL (optional for Task 3)
1) Create DB and apply schema (psql):
```
createdb bank_reviews
psql bank_reviews -f db/schema.sql
```
2) Set env vars and insert:
```
export PG_HOST=localhost
export PG_PORT=5432
export PG_DB=bank_reviews
export PG_USER=postgres
export PG_PASSWORD=postgres
python src/db_insert.py
```
```
python src/preprocess.py
```


Final Steps
```
# Sentiment + keywords
python src/sentiment_keywords.py

# Text preprocess (stop-words, lemmatize)
python src/text_preprocess.py

# Themes and summaries
python src/add_themes.py
python src/summarize.py

# Final analysis notebook: open and run
# notebooks/final_analysis.ipynb
```

Postgres
- Create DB `bank_reviews`; run `db/schema.sql`.
- Set env vars: `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`.
- Insert:
```
python src/db_insert.py
```
# customer-experience-analytics-week-2
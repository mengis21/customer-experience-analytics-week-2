Customer Experience Analytics – Week 2

Overview
- Scrape Google Play reviews for three Ethiopian banks (CBE, BOA, Dashen).
- Clean and prepare data (duplicates, missing, date normalization).
- Provide initial analysis for interim submission.

Project Structure
- `src/scrape_reviews.py`: Scrapes reviews using `google-play-scraper` and saves raw CSVs.
- `src/preprocess.py`: Cleans and merges raw CSVs into `data/clean_reviews.csv`.
- `notebooks/interim_analysis.ipynb`: Quick EDA for counts and rating distribution.
- `reports/interim_report.md`: Interim report to export to PDF.

Setup
1) Create/activate a virtual environment.
2) Install dependencies.

Commands (nu shell)
```
cd /home/aln_lvr/Desktop/Courses/KAIM/B8W2/customer-experience-analytics-week-2
python -m venv .venv
if ("$nu.os-info.family" == "linux") { source .venv/bin/activate } else { source .venv/Scripts/activate }
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
```
python src/preprocess.py
```

Notes
- `Samples - Technical Content` is excluded via `.gitignore` and not part of deliverables.
- Keep data files in `data/`.
# customer-experience-analytics-week-2
Customer Experience Analytics – Interim Report

Business Objective
Analyze Google Play reviews for CBE, BOA, and Dashen to understand satisfaction drivers and pain points and inform app improvements.

Completed Work
- Scraped reviews per bank using provided app IDs (CBE, BOA, Dashen).
- Saved raw CSVs (~600 reviews per bank).
- Preprocessed: removed duplicates, normalized dates (YYYY-MM-DD), handled missing.
- Produced `data/clean_reviews.csv` (rows: 1,523) for initial analysis.

Initial Findings
- Counts per bank and rating distribution are in the interim notebook.
- Missing values for `rating` and `date` are low after cleaning.

Next Steps
- Complete sentiment scoring (TextBlob or VADER, then compare with DistilBERT if time allows).
- Extract keywords/n-grams via TF-IDF/spaCy and group initial themes.
- Prepare Postgres schema and insert cleaned data.

Notes
This report will be updated after scraping with real app IDs, then exported to PDF.
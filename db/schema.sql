-- PostgreSQL schema for bank_reviews
CREATE TABLE IF NOT EXISTS banks (
  bank_id SERIAL PRIMARY KEY,
  bank_name TEXT NOT NULL UNIQUE,
  app_name TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id BIGSERIAL PRIMARY KEY,
  bank_id INTEGER NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE,
  review_text TEXT,
  rating INTEGER,
  review_date DATE,
  sentiment_label TEXT,
  sentiment_score DOUBLE PRECISION,
  source TEXT,
  themes TEXT,
  keywords TEXT
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_review_date ON reviews(review_date);
-- Database: bank_reviews

CREATE TABLE IF NOT EXISTS banks (
  bank_id SERIAL PRIMARY KEY,
  bank_name TEXT NOT NULL,
  app_name TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id SERIAL PRIMARY KEY,
  bank_id INTEGER NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE,
  review_text TEXT,
  rating INTEGER,
  review_date DATE,
  sentiment_label TEXT,
  sentiment_score DOUBLE PRECISION,
  source TEXT
);

CREATE INDEX IF NOT EXISTS idx_reviews_bank ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
-- Runs only when Postgres creates a data directory for the first time.
-- The pgvector image ships the extension; this turns it on in `rolefit`.
CREATE EXTENSION IF NOT EXISTS vector;

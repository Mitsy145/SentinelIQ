import os

# Tests that do not touch the database only need a syntactically valid URL.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://sentineliq:test@localhost:5432/sentineliq",
)

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def initialize_database():
    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r") as schema_file:
        conn.executescript(schema_file.read())

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully!")
    print(f"Database created at: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()
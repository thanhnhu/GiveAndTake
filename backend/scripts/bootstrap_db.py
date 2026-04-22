import json
import os
from pathlib import Path

import psycopg


def db_dsn() -> str:
    return (
        f"host={os.getenv('DB_HOST', 'postgres')} "
        f"port={os.getenv('DB_PORT', '5432')} "
        f"dbname={os.getenv('DB_NAME', 'giveandtake')} "
        f"user={os.getenv('DB_USER', 'giveandtake')} "
        f"password={os.getenv('DB_PASSWORD', 'giveandtake')}"
    )


def run_sql_migrations(conn: psycopg.Connection, migrations_dir: Path) -> None:
    # Ensure the migrations tracking table exists so we can skip already-applied files
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                name TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
    conn.commit()

    migrations = sorted(migrations_dir.glob("*.sql"))
    for migration in migrations:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM schema_migrations WHERE name = %s", (migration.name,))
            if cur.fetchone():
                print(f"Skipping already-applied migration: {migration.name}")
                continue

        sql = migration.read_text(encoding="utf-8")
        with conn.cursor() as cur:
            cur.execute(sql)
            cur.execute("INSERT INTO schema_migrations (name) VALUES (%s)", (migration.name,))
        conn.commit()
        print(f"Applied migration: {migration.name}")


def load_cities_fixture(conn: psycopg.Connection, fixture_path: Path) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM takers_city")
        count = int(cur.fetchone()[0])
        if count > 0:
            print("Cities already exist, skipping fixture load")
            return

    data = json.loads(fixture_path.read_text(encoding="utf-8-sig"))
    rows = [
        (int(item["pk"]), item["fields"]["name"])
        for item in data
        if item.get("model") == "takers.city"
    ]

    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO takers_city (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
            rows,
        )
    conn.commit()
    print(f"Loaded {len(rows)} cities")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    migrations_dir = base_dir / "migrations"
    cities_file = base_dir / "cities.json"

    with psycopg.connect(db_dsn()) as conn:
        run_sql_migrations(conn, migrations_dir)
        if cities_file.exists():
            load_cities_fixture(conn, cities_file)

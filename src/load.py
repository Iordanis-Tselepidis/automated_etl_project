import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os

# ----------------------------
# DB CONFIG
# ----------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": 5432,
    "database": os.getenv("DB_NAME", "weather_db"),
    "user": os.getenv("DB_USER", "etl_user"),
    "password": os.getenv("DB_PASSWORD", "etl_pass"),
}

TABLE_NAME = "weather_hourly"


# ----------------------------
# CREATE ENGINE
# ----------------------------

def get_engine():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return engine


# ----------------------------
# WAIT FOR DB
# ----------------------------

def wait_for_db(engine, retries=30, delay=3):
    print("Waiting for PostgreSQL to be ready...")

    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            return
        except OperationalError:
            print(f"DB not ready yet... retry {i+1}/{retries}")
            time.sleep(delay)

    raise Exception("PostgreSQL did not become ready in time")


# ----------------------------
# LOAD DATA
# ----------------------------

def load_data(engine, df: pd.DataFrame):
    print(f"Loading {len(df)} rows into {TABLE_NAME}...")

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print("Load complete.")


# ----------------------------
# MAIN
# ----------------------------

def main():
    # Load transformed data
    df = pd.read_parquet("clean_weather.parquet")

    # Connect
    engine = get_engine()

    # Wait for DB
    wait_for_db(engine)

    # Load data
    load_data(engine, df)


if __name__ == "__main__":
    main()

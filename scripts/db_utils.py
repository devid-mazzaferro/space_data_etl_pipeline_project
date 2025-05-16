import sys
import os
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from classes.db_tables import Base, Asteroid

sys.path.append("/opt/airflow")
DB_URI = os.getenv("AIRFLOW__CORE__SQL_ALCHEMY_CONN")
CSV_PATH = "/opt/airflow/data/processed/processed_page.csv"


def get_existing_ids():
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        result = session.execute(select(Asteroid.id)).scalars().all()
    return set(result)


def load_to_db():
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)

    df = pd.read_csv(CSV_PATH)

    df.to_sql(
        name=Asteroid.__tablename__,
        con=engine,
        if_exists='append',
        index=False
    )

    print(f"[INFO] Loaded {len(df)} records into table '{Asteroid.__tablename__}'.")
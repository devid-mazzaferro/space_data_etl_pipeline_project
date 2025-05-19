import pandas as pd
from src.classes.query_classes import SearchQuery
from src.classes.db_tables import Asteroid
from sqlalchemy import create_engine
from sqlalchemy import select, desc, and_
from sqlalchemy.orm import Session
from pathlib import Path
import dotenv
import os

env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
dotenv.load_dotenv(env_path)
user = os.getenv('POSTGRES_USER')
pwd = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
db = os.getenv('POSTGRES_DB')

engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db}')


def get_by_id(obj_id: str) -> list[dict]:
    """
    Retrieve a single asteroid object from the database by its unique identifier.

    Parameters:
        obj_id (str): The unique ID of the asteroid.

    Returns:
        list[dict]: A list containing one dictionary representing the asteroid, or an empty list if not found.
    """
    sqlquery = (select(Asteroid)
                .where(Asteroid.id == obj_id))
    with Session(engine) as session:
        df = pd.read_sql_query(sqlquery, session.connection())
        df = df.fillna('null')

    return df.to_dict(orient='records')


def retrieve_all_data() -> list[dict]:
    """
    Retrieve all asteroid records from the database.

    Returns:
        list[dict]: A list of dictionaries, each representing an asteroid record.
    """
    sqlquery = select(Asteroid)

    with Session(engine) as session:
        df = pd.read_sql_query(sqlquery, session.connection())
        df = df.fillna('null')

    return df.to_dict(orient='records')


def get_hazardous_objs() -> list[dict]:
    """
    Retrieve all asteroids flagged as hazardous.

    Returns:
       list[dict]: A list of dictionaries representing hazardous asteroids.
    """
    sqlquery = select(Asteroid).where(Asteroid.hazard == True)

    with Session(engine) as session:
        df = pd.read_sql_query(sqlquery, session.connection())
        df = df.fillna('null')

    return df.to_dict(orient='records')


def get_top_n_largest(top_n: int) -> list[dict]:
    """
    Retrieve the top N largest asteroids by maximum diameter.

    Parameters:
        top_n (int): The number of largest asteroids to retrieve.

    Returns:
        list[dict]: A list of dictionaries for the top N largest asteroids.
    """
    sqlquery = (select(Asteroid)
                .where(Asteroid.max_d > 0)
                .order_by(desc(Asteroid.max_d))
                .limit(top_n))

    with Session(engine) as session:
        df = pd.read_sql_query(sqlquery, session.connection())
        df = df.fillna('null')

    return df.to_dict(orient='records')

def search_asteroids(query: SearchQuery) -> list[dict]:
    """
    Perform a filtered search for asteroids based on multiple optional query parameters.

    Parameters:
        query (SearchQuery): A search query object with optional filters such as name,
                             absolute magnitude range, diameter range, and inclination range.

    Returns:
        list[dict]: A list of dictionaries representing asteroids that match the search criteria.
    """

    conditions = []

    if query.name:
        conditions.append(Asteroid.name.ilike(f"%{query.name}%"))

    if query.abs_mag_min is not None:
        conditions.append(Asteroid.abs_mag >= query.abs_mag_min)

    if query.abs_mag_max is not None:
        conditions.append(Asteroid.abs_mag <= query.abs_mag_max)

    if query.diameter_min is not None:
        conditions.append(Asteroid.min_d >= query.diameter_min)

    if query.diameter_max is not None:
        conditions.append(Asteroid.max_d <= query.diameter_max)

    if query.inclination_min is not None:
        conditions.append(Asteroid.inclination >= query.inclination_min)

    if query.inclination_max is not None:
        conditions.append(Asteroid.inclination <= query.inclination_max)

    sqlquery = select(Asteroid)
    if conditions:
        sqlquery = sqlquery.where(and_(*conditions))

    with Session(engine) as session:
        df = pd.read_sql_query(sqlquery, session.connection())
        df = df.fillna('null')

    return df.to_dict(orient='records')


def asteroids_stats() -> list[dict]:
    """
    Compute summary statistics about asteroids, including general info, brightness, dimensions, and orbit characteristics.

    Returns:
        list[dict]: A nested dictionary containing:
            - General statistics: total objects, hazardous count, hazardous percentage.
            - Brightness: min, max, mean, std of absolute magnitude and ID of brightest object.
            - Dimensions: min, max, mean, std of diameter and ID of largest object.
            - Orbits: min, max, mean, std of eccentricity and IDs of highly eccentric orbit objects.
    """
    sqlquery = select(Asteroid)

    with Session(engine) as session:
        df = pd.read_sql_query(sqlquery, session.connection())

    stats = {
        'general_statistics':
            {
                "n_obj": len(df),
                "n_hazardous_objects": len(df[df['hazard'] == True]),
                "perc_hazardous_objects": round(len(df[df['hazard'] == True]) / len(df) * 100, 2)
            },

        'brightness':
            {
            "abs_mag_min": float(df['abs_mag'].min()),
            "abs_mag_max": float(df['abs_mag'].max()),
            "abs_mag_mean": float(df['abs_mag'].mean()),
            "abs_mag_std": float(df['abs_mag'].std()),
            "brightest_obj_id": list(df[df['abs_mag'] == df['abs_mag'].min()]['id'])
            },

        'dimensions':
            {
                "min_diameter": df['min_d'].min(),
                "max_diameter": df['max_d'].max(),
                "mean_diameter": df['max_d'].mean(),
                "diameter_std": df['max_d'].std(),
                "largest_obj_id": list(df[df['max_d'] == df['max_d'].max()]['id'])
            },

        'orbits':
            {
                "min_eccentricity": df['eccentricity'].max(),
                "max_eccentricity": df['eccentricity'].min(),
                "mean_eccentricity": df['eccentricity'].mean(),
                "eccentricity_std": df['eccentricity'].std(),
                "extreme_orbits_obj_id": list(df[df['eccentricity'] > .9]['id'])
            }
    }

    return stats
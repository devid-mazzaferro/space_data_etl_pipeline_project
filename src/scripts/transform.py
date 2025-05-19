from src.scripts.db_utils import get_existing_ids
import pandas as pd
import json
import os

DATA_DIR = os.getenv("DATA_DIR", "/opt/airflow/data")

def extract_fields(obj):
    return {
        'id': obj.get('id'),
        'name': obj.get('name'),
        'abs_mag': obj.get('absolute_magnitude_h'),
        'min_d': obj.get('estimated_diameter', {}).get('meters', {}).get('estimated_diameter_min'),
        'max_d': obj.get('estimated_diameter', {}).get('meters', {}).get('estimated_diameter_max'),
        'hazard': obj.get('is_potentially_hazardous_asteroid'),
        'eccentricity': obj.get('orbital_data', {}).get('eccentricity'),
        'semi_maj_ax': obj.get('orbital_data', {}).get('semi_major_axis'),
        'inclination': obj.get('orbital_data', {}).get('inclination'),
        'ascending_node_lon': obj.get('orbital_data', {}).get('ascending_node_longitude'),
        'perihelion_dist': obj.get('orbital_data', {}).get('perihelion_distance'),
        'aphelion_dist': obj.get('orbital_data', {}).get('aphelion_distance'),
        'perihelion_argument': obj.get('orbital_data', {}).get('perihelion_argument'),
        'mean_anomaly': obj.get('orbital_data', {}).get('mean_anomaly'),
        'mean_motion': obj.get('orbital_data', {}).get('mean_motion'),
        'epoch_osculation': obj.get('orbital_data', {}).get('epoch_osculation')
    }


def create_df():
    files = [
        f for f in os.listdir(DATA_DIR)
        if f.endswith(".json") and f != "progress.json"
    ]

    if not files:
        print("[WARN] No data files found in data directory.")
        return pd.DataFrame()

    df_out = pd.DataFrame()
    for file in files:
        with open(rf"{DATA_DIR}/{file}") as f:
            data = json.load(f)

        records = [extract_fields(obj) for obj in data['near_earth_objects']]
        obj_df = pd.DataFrame(records)

        df_out = pd.concat([df_out, obj_df], ignore_index=True)

    df_out[['eccentricity', 'semi_maj_ax',
            'inclination', 'ascending_node_lon',
            'perihelion_dist', 'aphelion_dist']] = df_out[['eccentricity', 'semi_maj_ax',
                                                           'inclination', 'ascending_node_lon',
                                                           'perihelion_dist', 'aphelion_dist']].astype(float)

    return df_out


def transform():
    print("[INFO] Starting transform step")
    df = create_df()

    if df.empty:
        print("[INFO] No data to transform.")
        return df

    print(f"[INFO] Fetched {len(df)} total records")

    existing_ids = get_existing_ids()
    before = len(df)
    df = df[~df['id'].isin(existing_ids)]
    after = len(df)

    print(f"[INFO] Filtered {before - after} existing records; {after} new remain")
    return df

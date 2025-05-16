from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys
import json
import requests

sys.path.append('/opt/airflow')

from scripts.fetch_from_neows import fetch_asteroids
from scripts.transform import transform
from scripts.db_utils import load_to_db

API_KEY = os.getenv("NASA_API_KEY")
DATA_DIR = "/opt/airflow/data"
DB_URI = os.getenv("AIRFLOW__CORE__SQL_ALCHEMY_CONN")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
PAGES_PER_RUN = 500  # Adjust to stay within rate limits


def extract_incremental(**context):
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        response = requests.get(
            "https://api.nasa.gov/neo/rest/v1/neo/browse",
            params={"api_key": API_KEY, "page": 0, "size": 20}
        )
        response.raise_for_status()
        total_pages = response.json()["page"]["total_pages"]
        print(f"[INFO] Total pages on API: {total_pages}")
    except Exception as e:
        raise RuntimeError(f"Failed to get total pages from API: {e}")

    last_page = -1
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE) as f:
                state = json.load(f)
                last_page = state.get("last_page", -1)
        except json.JSONDecodeError:
            print("[WARNING] Invalid progress file, starting fresh.")

    print(f"[INFO] Last downloaded page: {last_page}")

    start_page = last_page + 1
    if start_page >= total_pages:
        print("[INFO] Already up-to-date. Re-downloading last page just in case.")
        start_page = total_pages - 1

    end_page = min(start_page + PAGES_PER_RUN, total_pages)

    fetched_files = []
    final_page_fetched = last_page  # Updated only when successful
    # return start_page, end_page


    for page in range(start_page, end_page):
        try:
            filename, current_page, _ = fetch_asteroids(API_KEY, page, DATA_DIR)
            fetched_files.append(filename)
            final_page_fetched = page
            print(f"[INFO] Downloaded page {page}")
        except Exception as e:
            print(f"[ERROR] Could not fetch page {page}: {e}")
            break  # Stop on first failure

    with open(PROGRESS_FILE, "w") as f:
        json.dump({"last_page": final_page_fetched}, f)
        print(f"[INFO] Updated progress to page {final_page_fetched}")

    context['ti'].xcom_push(key='json_paths', value=fetched_files)

def transform_task():
    os.makedirs(f"{DATA_DIR}/processed", exist_ok=True)
    df = transform()
    df.to_csv(f"{DATA_DIR}/processed/processed_page.csv", index=False)

def load_task():
    load_to_db()


with DAG(
    dag_id='asteroid_etl',
    start_date=datetime.now(),
    schedule_interval='@hourly',
    catchup=False,
    tags=['nasa', 'etl', 'browse'],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_incremental,
        provide_context=True,
    )

    transform_step = PythonOperator(
        task_id="transform",
        python_callable=transform_task
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task,
        provide_context=True,
    )

extract >> transform_step >> load
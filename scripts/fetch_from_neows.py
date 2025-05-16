import requests
import os
import json

def fetch_asteroids(api_key, page, save_dir):
    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?page={page}&api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    filename = os.path.join(save_dir, f"asteroids_page_{page}.json")
    with open(filename, "w") as f:
        json.dump(data, f)

    return filename, data["page"]["number"], data["page"]["total_pages"]

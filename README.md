
# Space Data ETL Pipeline – NeoWs Asteroid Ingestion

## Overview
This project builds a complete data engineering pipeline that ingests data from NASA's Near Earth Object Web Service (NeoWs), transforms and stores it in a PostgreSQL database, and exposes it via a REST API built with FastAPI.

The pipeline is orchestrated using Apache Airflow and containerized with Docker for local development and testing.

## Data Source
**NeoWs (Near Earth Object Web Service) - Feed Endpoint**  
API URL: `https://api.nasa.gov/neo/rest/v1/browse?api_key=DEMO_KEY&page=N&size=0`

This endpoint provides data on asteroids that are near Earth, including their estimated diameters and orbital information.

## Goal
Ingest, clean, and serve only the most relevant fields for potential analysis and visualization:
- `id`
- `name`
- `absolute_magnitude_h`
- `estimated_diameter` → min and max in meters
- Whether the object is considered hazardous 
- Selected `orbital_data` fields (i.e. `eccentricity`, `semi_maj_ax`, `inclination`, `ascending_node_lon`, `perihelion_dist`, `aphelion_dist`) – for potential plotting use


## Features
- Hourly ingestion of near-Earth asteroid data
- Data cleaning and transformation
- PostgreSQL storage with a clean, queryable schema
- REST API using FastAPI to expose filtered or specific asteroid data
- Containerized with Docker

## Stack
- Apache Airflow
- PostgreSQL
- Python
- FastAPI
- Docker

## Folder Structure
- `dags/` – Airflow DAGs
- `data/` - Processed data
- `docker/` – Dockerfiles and docker-compose setup
- `fastapi_app/` – API code to serve data
- `scripts/` – Data extraction and transformation logic

## Planned FastAPI Endpoints (TODO)
- `GET /asteroids`
- `GET /asteroids/{asteroid_id}`
- `GET /asteroids/search`: Search by name, magnitude range, diameter range, or orbital parameters.
- `GET /asteroids/stats`: Return basic statistics like count, average magnitude, average diameter, etc.
- `GET /asteroids/hazardous`
- `GET /asteroids/largest`

## Example Use Cases
- Track all NEOs
- Search and filter NEOs
- Get NEOs overall stats
- Filter potentially hazardous objects
- Support visualization of orbital paths or encounter timelines

## Getting Started
## Environment Setup

This project uses Docker to ensure compatibility with Apache Airflow, which requires a POSIX-compliant environment.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Ensure **WSL2 integration** is enabled (Settings > General > "Use the WSL 2 based engine")
- (Optional) [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) with a Linux distro (e.g. Ubuntu)
- Git (to clone this repo)
- Python 3.11+

.env file in the project root with the following

```
# NASA API
NASA_API_KEY=your_api_key_here
START_DATE=YYYY-MM-DD  # e.g., 2024-01-01

# PostgreSQL connection
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=asteroids
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Airflow configuration
AIRFLOW__WEBSERVER__SECRET_KEY=your_airflow_webserver_secret_key
```

### Starting the Services

From the project root directory, run:

```bash
docker compose --env-file .env -f docker/docker-compose.yml up --build
```
The PostgreSQL container automatically initializes the `asteroids` table during startup using a SQL script mounted in the container. There is no need for manual table creation or schema setup.

Then navigate to http://localhost:8080/home and log in with admin/admin. Activate asteroid_etl's DAG and wait for it to succeed.

Once activated, the pipeline fetches up to 500 pages of asteroid data from NeoWs. It deduplicates entries based on asteroid ID and only stores new asteroids not already present in the database. If the final page has no new entries, it will still be polled hourly for updates.


## Author
Devid Mazzaferro

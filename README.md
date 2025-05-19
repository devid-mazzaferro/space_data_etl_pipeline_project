# NeoWs Asteroid Ingestion and service data pipeline

## Overview

This project builds a complete data engineering pipeline that ingests data from NASA's Near Earth Object Web Service (NeoWs), transforms and stores it in a PostgreSQL database, and exposes it via a REST API built with FastAPI.

The pipeline is orchestrated using Apache Airflow and containerized with Docker for local development and testing.

⚠️ **Note:** This code is not production-ready. It's a personal exercise designed to gain hands-on experience with real-world datasets and modern data engineering tools.

---

## Data Source

**NeoWs (Near Earth Object Web Service) – Browse Endpoint**  
API URL: `https://api.nasa.gov/neo/rest/v1/browse?api_key=DEMO_KEY&page=N&size=20`

Provides data on near-Earth asteroids, including:

- Estimated diameters  
- Orbital information  
- Hazard potential

---

## Goal

Extract, transform, and expose the following key features:

- `id`  
- `name`  
- `absolute_magnitude_h`  
- Estimated diameter (min/max in meters)  
- Hazardous flag (`is_potentially_hazardous_asteroid`)  
- Selected `orbital_data` fields:  
  - `eccentricity`  
  - `semi_major_axis`  
  - `inclination`  
  - `ascending_node_longitude`  
  - `perihelion_distance`  
  - `aphelion_distance`
  - `perihelion_argument`
  - `mean_anomaly`
  - `mean_motion`
  - `epoch_osculation`

---

## Features

- Hourly ingestion of near-Earth asteroid data
- Deduplication and transformation
- PostgreSQL storage with a clean schema
- REST API for exploration and analysis
- Full containerization with Docker
- API documentation via Swagger UI

---

## Tech Stack

- **Apache Airflow** – Orchestrate ETL  
- **PostgreSQL** – Persist structured data  
- **FastAPI** – Serve endpoints  
- **Docker** – Local dev environment  
- **SQLAlchemy** – ORM  
- **Pandas** – Data transformation

---

## Folder Structure

```
project-root/
│
├── dags/                  # Airflow DAG definition
├── data/                  # Processed data
├── docker/                # Dockerfile, init SQL, logs, etc.
├── src/                   # All source code
│   ├── scripts/           # ETL scripts
│   ├── classes/           # ORM & Pydantic models
│   └── fastapi_app/       # FastAPI app, routes, utils
└── requirements.txt       # Python dependencies
```

---

## Available FastAPI Endpoints

| Method | Endpoint               | Description                           |
| ------ | ---------------------- | ------------------------------------- |
| `GET`  | `/asteroids`           | Retrieve all asteroid entries         |
| `POST` | `/asteroids/id`        | Retrieve object by ID (via JSON body) |
| `POST` | `/asteroids/search`    | Search by name, diameter, inclination |
| `GET`  | `/asteroids/stats`     | Basic descriptive statistics          |
| `POST` | `/asteroids/hazardous` | All hazardous asteroids               |
| `POST` | `/asteroids/largest`   | Top N largest asteroids by diameter   |

Documentation: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## Use Cases

- Filter NEOs by characteristics  
- Analyze overall dimensions  
- Identify potentially hazardous objects  
- Power visualizations of orbital elements

---

## Getting Started

### Prerequisites

- Docker Desktop (with **WSL2 integration** enabled)  
- Git  
- Python 3.11+ (for local testing only)

### .env Setup

Create a `.env` file in the root directory:

```env
# NASA API
NASA_API_KEY=your_api_key_here
START_DATE=2024-01-01

# PostgreSQL connection
POSTGRES_USER=devid
POSTGRES_PASSWORD=spacepass
POSTGRES_DB=asteroids
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Airflow
AIRFLOW__WEBSERVER__SECRET_KEY=your_secret_key
```

---

### Start the Stack

```bash
docker compose --env-file .env -f docker/docker-compose.yml up --build
```

- Airflow UI → [http://localhost:8080](http://localhost:8080) → Login with `admin` / `admin`  
- FastAPI → [http://localhost:8001/docs](http://localhost:8001/docs)

- Activate the DAG named `asteroid_etl`  
- It will ingest and process up to ~950 pages/hours  
- Deduplication ensures no repeated asteroid entries  
- The last page is polled hourly for new updates

---

## Author

**Devid Mazzaferro**  
Built as a portfolio project to gain hands-on data engineering experience.

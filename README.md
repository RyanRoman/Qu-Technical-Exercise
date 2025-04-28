# Insights Service • Take‑Home Exercise

Welcome! This starter repository contains just enough scaffolding so you can focus on the interesting parts:

| Folder | Purpose |
|--------|---------|
| `openapi/` | Minimal OpenAPI spec for the existing monolith you will extend/consume |
| `data/` | Mock time‑series data (`mock_timeseries.json`) |
| `db/` | PostgreSQL seed SQL (`db/init/init.sql`) |
| `app/` | FastAPI application skeleton |
| `services/insights/` | Your new endpoints, schemas, and business logic |
| `docs/` | Design‑brief template you must fill out |
| `tests/` | Example pytest setup |


## ⏱ Time Expectations
* **Design brief:** 2 minute read 
* **Coding:** ~1h (implement two endpoints)


## 🎯 Deliverables
1. Read **`docs/design_brief.md`** 
2. Implement **two endpoints** in `services/insights/router.py`.
   * **Circuit‑level total usage** (watts over a time window).  
   * **Organization‑level aggregate** (roll‑up across locations). 
3. Push your repo and share the link.

A third endpoint or an extension to an existing endpoint will be added **live** during the follow‑up call.



## 🔧 Endpoint Requirements

| Level | Endpoint description |
|-------|-----------------------------|
| **Circuit** | Return total power usage (watts) for a *single circuit* across a time window. Must reference the circuit’s metadata record. |
| **Organization** | Aggregate power across **all locations** in an organization for the same window. Provide at least total watts and average watts per circuit. |

- Each endpoint must accept sensible query parameters (e.g., time window) and validate them.  Edge‑cases (missing params, invalid ranges, etc.) should return clear errors.
- Auto‑generated FastAPI docs should describe parameters & responses.
- Responses should be JSON and include enough identifiers for clients to link back to metadata. Exact field names and nesting are up to you.

## 🏃‍♂️ Quick Start
```bash
docker-compose up --build 
# OR:
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
pytest
```

## 🛠️ Tech Stack
* Python 3.10+, FastAPI, SQLAlchemy 2.x
* PostgreSQL — metadata store (pre‑seeded)
* **Mock time‑series DB** (`data/mock_timeseries.json`)


## Metadata Schema
See `db/init/init.sql` for full DDL + seed data (1 brand, 3 orgs, 6 locations, 12 sensors, 36 circuits).


## Existing Monolith Endpoints
| Path | Purpose |
|------|---------|
| `GET /v1/electric_sensors/{sensor_id}` | Sensor metadata |
| `GET /v1/locations/{location_id}/circuit-summary` | Location summary |
| `GET /v1/brands/{brand_id}/metadata` | Brand metadata |

Use these (spec in **`openapi/monolith.yaml`**) or query the DBs directly.

---

Good luck — we look forward to reviewing your insights!
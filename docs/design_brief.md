# Design Brief – Insights Service

## 1. Service Boundaries
What belongs here? What stays in the monolith?

    Belongs in Insights:

    • Calculating total and average usage

    • Summarizing data across time windows

    Stays in Monolith:

    • Managing metadata (brands, locations, circuits)

## 2. Data Flow
How will metadata & time‑series data reach the Insights Service?

    • Metadata (circuits, sensors, locations) is queried from a PostgreSQL database populated by the provided init.sql script.

    • Timeseries usage data is read from a mock static JSON file (data/mock_timeseries.json) for the purpose of this exercise.

    • In production, timeseries data would typically be streamed from a real ingestion service or timeseries database.

## 3. Failure & Retry Strategy
Downstream outages, retries, idempotency.

    • If metadata queries or timeseries data loading fails, the service returns clear error codes (404 or 500).

    • Retries are not implemented (out of scope for this take-home) but would use exponential backoff strategies for transient errors in production.

    • Endpoints are read-only and safe to retry from clients if needed.

## 4. API Design & Versioning
Chosen URL patterns, versioning, pagination/filtering approach.

    Endpoints:

        • /v1/insights/circuit-usage

        • /v1/insights/org-aggregate

    • Versioning: All endpoints are prefixed with /v1/ to allow future upgrades without breaking clients.

    • Filtering: start_time and end_time are required query parameters.

    • Pagination: Not implemented; each call returns a single aggregate result.

## 5. Trade‑offs & Alternatives
Discuss other options you considered and why you chose this path.

    • Considered using SQLAlchemy ORM models, but raw SQL was chosen to minimize boilerplate and speed up querying.

    • Considered using Monolith HTTP APIs, but querying the DB directly reduced complexity and improved performance for local development.

    • Mock timeseries data was used as provided. In production, this would be replaced with live queries to a timeseries data store.

## 6. Scaling Considerations
Millions of points/day, hot paths vs. cold paths, observability.

    • Metadata (locations, circuits, sensors) scales easily with standard PostgreSQL.

    • Timeseries scaling: Would move to a real timeseries database when volume grows.

    • Caching hot paths could improve performance at scale.

    • Cold paths could be optimized with background jobs.

    • Observability: Would add structured logging, request tracing, and metrics collection.
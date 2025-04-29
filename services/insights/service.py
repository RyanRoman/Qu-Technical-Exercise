import json
from pathlib import Path
from datetime import datetime
from typing import Tuple, Set, List
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def load_timeseries() -> List[dict]:
    """Load the mock timeseries data once."""
    data_path = Path("data/mock_timeseries.json")
    if not data_path.exists():
        raise FileNotFoundError("Time series data not found.")

    with data_path.open("r") as f:
        return json.load(f)


def calculate_total_usage(
    timeseries: List[dict],
    circuit_keys: Set[Tuple[str, int]],
    start_time: datetime,
    end_time: datetime,
) -> int:
    """Sum power_watts for matching (duid, circuit_number) pairs over a time window."""
    total_usage = 0

    for record in timeseries:
        record_duid = record.get("duid")
        record_circuit_number = record.get("circuit_number")

        if (record_duid, record_circuit_number) not in circuit_keys:
            continue

        record_timestamp_str = record.get("timestamp")
        record_power_watts = record.get("power_watts", 0)

        if not record_timestamp_str:
            continue

        try:
            record_timestamp = datetime.fromisoformat(record_timestamp_str.rstrip("Z"))
        except ValueError:
            continue

        if start_time <= record_timestamp <= end_time:
            total_usage += record_power_watts

    return total_usage


def sum_circuit_usage(
    circuit_number: int, start_time: datetime, end_time: datetime
) -> int:
    """Sum total power usage for a single circuit over a time window."""
    timeseries = load_timeseries()

    circuit_keys = set()
    for record in timeseries:
        if record.get("circuit_number") == circuit_number:
            duid = record.get("duid")
            if duid and circuit_number is not None:
                circuit_keys.add((duid, circuit_number))

    if not circuit_keys:
        raise ValueError(f"No circuit found with circuit_number {circuit_number}")

    return calculate_total_usage(timeseries, circuit_keys, start_time, end_time)


def sum_org_usage(
    org_id: UUID, start_time: datetime, end_time: datetime
) -> Tuple[int, int]:
    """Sum total power usage across all circuits for an organization by querying the database."""
    db: Session = SessionLocal()

    sql = text(
        """
        SELECT s.duid, c.circuit_number
        FROM circuits c
        JOIN electric_sensors s ON c.sensor_id = s.id
        JOIN locations l ON s.location_id = l.id
        WHERE l.organization_id = :org_id
        """
    )

    results = db.execute(sql, {"org_id": str(org_id)}).fetchall()

    if not results:
        raise ValueError(f"No circuits found for org_id {org_id}")

    circuit_lookup = set((row.duid, row.circuit_number) for row in results)

    timeseries = load_timeseries()

    total_usage = calculate_total_usage(
        timeseries, circuit_lookup, start_time, end_time
    )
    circuit_count = len(circuit_lookup)

    return total_usage, circuit_count

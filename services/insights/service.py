from datetime import datetime, timezone
from pathlib import Path
from typing import List, Set, Tuple

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def load_timeseries() -> pd.DataFrame:
    """Load mock timeseries into a pandas DataFrame."""
    data_path = Path("data/mock_timeseries.json")
    if not data_path.exists():
        raise FileNotFoundError("Time series data not found.")

    df = pd.read_json(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def normalize_to_utc(dt: datetime) -> datetime:
    """Ensure a datetime is timezone-aware and set to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    else:
        return dt.astimezone(timezone.utc)


def calculate_total_usage(
    df: pd.DataFrame,
    circuit_keys: Set[Tuple[str, int]],
    start_time: datetime,
    end_time: datetime,
) -> int:
    """Compute total power usage in watts for matching circuits within a given time window."""
    if df.empty or not circuit_keys:
        return 0

    start_time = normalize_to_utc(start_time)
    end_time = normalize_to_utc(end_time)

    circuit_keys_df = pd.DataFrame(circuit_keys, columns=["duid", "circuit_number"])

    calc_usage = int(
        df.merge(circuit_keys_df, on=["duid", "circuit_number"])
        .query("@start_time <= timestamp <= @end_time")
        .power_watts.sum()
    )

    return calc_usage


def sum_circuit_usage(circuit_id: int, start_time: datetime, end_time: datetime) -> int:
    """Calculate total power usage for a single circuit over a time window."""
    df = load_timeseries()
    circuit_keys = set(
        df[df["circuit_number"] == circuit_id][["duid", "circuit_number"]].itertuples(
            index=False, name=None
        )
    )
    if not circuit_keys:
        raise ValueError(f"No circuit found with circuit_number {circuit_id}")
    return calculate_total_usage(df, circuit_keys, start_time, end_time)


# fmt: off
def sum_org_usage(org_id: str, start_time: datetime, end_time: datetime) -> Tuple[int, int]:
    """Calculate total and average power usage across an organization's circuits."""
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
    results = db.execute(sql, {"org_id": org_id}).fetchall()
    if not results:
        raise ValueError(f"No circuits found for org_id {org_id}")
    circuit_keys = set((row.duid, row.circuit_number) for row in results)

    df = load_timeseries()
    total_usage = calculate_total_usage(df, circuit_keys, start_time, end_time)
    circuit_count = len(circuit_keys)
    return total_usage, circuit_count

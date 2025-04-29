from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from uuid import UUID

from services.insights.service import sum_circuit_usage, sum_org_usage

router = APIRouter(tags=["insights"])


@router.get("/circuit-usage")
async def get_circuit_usage(
    circuit_number: int = Query(..., description="Circuit ID to look up"),
    start_time: datetime = Query(..., description="Start of the time window"),
    end_time: datetime = Query(..., description="End of the time window"),
):
    """Return total power usage in watts for a single circuit over a specified time window."""
    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="start_time must be before end_time",
        )

    try:
        total_usage = sum_circuit_usage(circuit_number, start_time, end_time)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Time series data not found.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "circuit_number": circuit_number,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_usage_watts": total_usage,
    }


@router.get("/org-aggregate")
async def get_org_aggregate(
    org_id: UUID = Query(..., description="Organization ID to look up"),
    start_time: datetime = Query(..., description="Start of the time window"),
    end_time: datetime = Query(..., description="End of the time window"),
):
    """Aggregate total and average power usage (watts) across all circuits in an organization."""
    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="start_time must be before end_time",
        )

    try:
        total_usage, circuit_count = sum_org_usage(org_id, start_time, end_time)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Time series data not found.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    average_usage = total_usage / circuit_count if circuit_count > 0 else 0

    return {
        "org_id": str(org_id),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_usage_watts": total_usage,
        "average_usage_watts_per_circuit": average_usage,
        "circuit_count": circuit_count,
    }

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from services.insights.service import sum_circuit_usage, sum_org_usage

# Openapi tests reference: http://localhost:8000/docs#/
# id: 1, 955c3c4d-3a03-4d79-9655-3871f5ad999d
# start_time: 2024-04-01T00:00:00
# end_time: 2024-04-02T00:00:00


@pytest.fixture
def time_window():
    """Provide a common start_time and end_time for tests."""
    start_time = datetime(2024, 4, 1, 0, 0, 0)
    end_time = datetime(2024, 4, 2, 0, 0, 0)
    return start_time, end_time


@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    with patch("services.insights.service.SessionLocal") as mock_sessionlocal:
        mock_session = MagicMock()
        mock_sessionlocal.return_value = mock_session
        yield mock_session


def test_sum_circuit_usage_valid(time_window):
    circuit_id = 1
    start_time, end_time = time_window

    total_usage = sum_circuit_usage(circuit_id, start_time, end_time)

    assert isinstance(total_usage, int)
    assert total_usage >= 0


def test_sum_org_usage_valid(mock_db_session, time_window):
    mock_db_session.execute.return_value.fetchall.return_value = [
        MagicMock(duid="FAKE_DUID1", circuit_number=1),
        MagicMock(duid="FAKE_DUID2", circuit_number=2),
    ]

    start_time, end_time = time_window
    total_usage, circuit_count = sum_org_usage(
        org_id=1, start_time=start_time, end_time=end_time
    )

    assert isinstance(total_usage, int)
    assert isinstance(circuit_count, int)
    assert circuit_count == 2


def test_sum_org_usage_invalid_org(mock_db_session, time_window):
    mock_db_session.execute.return_value.fetchall.return_value = []

    start_time, end_time = time_window
    with pytest.raises(ValueError, match="No circuits found for org_id"):
        sum_org_usage(org_id=9999, start_time=start_time, end_time=end_time)

from datetime import datetime, timezone
from src.crew import Crew
from src.flight import Flight
from src.validator import can_assign_next, dynamic_rest_minutes


def dt(s: str) -> datetime:
    # helper: "2024-02-01T08:00:00" assumed UTC
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def test_range_limit_short_haul_cannot_take_long_haul():
    crew = Crew(crew_id="C001", home_base="JFK", max_range_miles=2000)
    long_flight = Flight(
        flight_id="FL999",
        origin="JFK",
        destination="LHR",
        departure=dt("2024-02-01T08:00:00"),
        arrival=dt("2024-02-01T16:00:00"),
        distance_miles=3500,
    )
    ok, reason = can_assign_next(crew, [], long_flight)
    assert ok is False
    assert reason == "range"


def test_dynamic_rest_long_flight_requires_longer_break():
    short = Flight(
        flight_id="FL1",
        origin="JFK",
        destination="BOS",
        departure=dt("2024-02-01T08:00:00"),
        arrival=dt("2024-02-01T10:00:00"),  # 120 min
        distance_miles=200,
    )
    long = Flight(
        flight_id="FL2",
        origin="JFK",
        destination="LAX",
        departure=dt("2024-02-01T08:00:00"),
        arrival=dt("2024-02-01T12:30:00"),  # 270 min
        distance_miles=2500,
    )
    assert dynamic_rest_minutes(short) == 60
    assert dynamic_rest_minutes(long) == 120


def test_home_base_start_first_flight_must_match_home_base():
    crew = Crew(crew_id="C002", home_base="JFK", max_range_miles=5000)
    flight = Flight(
        flight_id="FL10",
        origin="LHR",  # not home base
        destination="JFK",
        departure=dt("2024-02-01T08:00:00"),
        arrival=dt("2024-02-01T12:00:00"),
        distance_miles=3500,
    )
    ok, reason = can_assign_next(crew, [], flight)
    assert ok is False
    assert reason == "home_base_start"

from __future__ import annotations

from dataclasses import dataclass

from typing import Dict, List, Tuple

from .crew import Crew
from .flight import Flight
from .roster import Roster


@dataclass(frozen=True)
class ValidationError:
    crew_id: str
    message: str


def dynamic_rest_minutes(prev_flight: Flight) -> int:
    return 60 if prev_flight.duration_minutes < 180 else 120


def validate_chain_for_crew(crew: Crew, flights: List[Flight]) -> List[str]:
    """
    Returns a list of error messages for this crew's chain (empty = valid).
    """
    errors: List[str] = []
    if not flights:
        return errors

    # Start rule: first flight must depart home_base
    if flights[0].origin != crew.home_base:
        errors.append(
            f"Start rule violated: first flight origin {flights[0].origin} != home_base {crew.home_base}"
        )

    for i, f in enumerate(flights):
        # Distance rule
        if f.distance_miles > crew.max_range_miles:
            errors.append(
                f"Range rule violated: {f.flight_id} distance {f.distance_miles} > max {crew.max_range_miles}"
            )

        # Continuity + rest checks 
        if i > 0:
            prev = flights[i - 1]

            # Chain rule
            if prev.destination != f.origin:
                errors.append(
                    f"Chain rule violated: {prev.flight_id} destination {prev.destination} != {f.flight_id} origin {f.origin}"
                )

            # Rest rule
            min_rest = dynamic_rest_minutes(prev)
            actual_rest = int((f.departure - prev.arrival).total_seconds() // 60)
            if actual_rest < min_rest:
                errors.append(
                    f"Rest rule violated: rest between {prev.flight_id}->{f.flight_id} is {actual_rest} min, needs {min_rest} min"
                )

    return errors


def validate_roster(roster: Roster, crew_by_id: Dict[str, Crew]) -> List[ValidationError]:
    """
    Validate entire roster. Returns list of ValidationError; empty = roster is valid.
    """
    all_errors: List[ValidationError] = []

    for crew_id, flights in roster.schedule.items():
        crew = crew_by_id.get(crew_id)
        if crew is None:
            all_errors.append(ValidationError(crew_id, "Unknown crew_id in roster"))
            continue

        flights_sorted = sorted(flights, key=lambda f: f.departure)
        errs = validate_chain_for_crew(crew, flights_sorted)
        for e in errs:
            all_errors.append(ValidationError(crew_id, e))

    return all_errors


def can_assign_next(crew: Crew, assigned_flights: List[Flight], new_flight: Flight) -> Tuple[bool, str]:
    """
    Incremental check used by scheduler BEFORE assigning.
    Returns (True, "") if valid, else (False, reason).
    """
    # Distance rule
    if new_flight.distance_miles > crew.max_range_miles:
        return False, "range"

    if not assigned_flights:
        # Start rule
        if new_flight.origin != crew.home_base:
            return False, "home_base_start"
        return True, ""

    # Find last chronological flight 
    last = max(assigned_flights, key=lambda f: f.departure)

    # Must be at the right airport
    if last.destination != new_flight.origin:
        return False, "continuity"

    # Must have enough rest after last flight
    min_rest = dynamic_rest_minutes(last)
    actual_rest = int((new_flight.departure - last.arrival).total_seconds() // 60)
    if actual_rest < min_rest:
        return False, "rest"

    return True, ""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def parse_iso_utc(ts: str) -> datetime:
    """
    Parses ISO 8601 timestamps like:
      2024-02-01T08:00:00Z
      2024-02-01T08:00:00+00:00
    Returns a timezone-aware datetime.
    """
    ts = ts.strip()
    if ts.endswith("Z"):
        # Convert common UTC suffix to offset form accepted by fromisoformat.
        ts = ts[:-1] + "+00:00"
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        # Assume UTC if timezone is missing.
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class Flight:
     # Immutable flight “demand” record loaded from CSV.
    flight_id: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    distance_miles: int

    @property
    def duration_minutes(self) -> int:
        # Derived metric used by dynamic rest rule (<3h => 60m, >=3h => 120m).
        delta = self.arrival - self.departure
        return int(delta.total_seconds() // 60)

    def validate(self) -> None:
        # Validate domain invariants early to keep scheduler logic simple and safe.
        if self.arrival <= self.departure:
            raise ValueError(f"{self.flight_id}: arrival must be after departure")
        if not isinstance(self.distance_miles, int) or self.distance_miles <= 0:
            raise ValueError(f"{self.flight_id}: distance_miles must be a positive integer")
        if not self.flight_id:
            raise ValueError("flight_id must not be empty")
        if not self.origin or not self.destination:
            raise ValueError(f"{self.flight_id}: origin/destination must not be empty")

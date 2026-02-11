from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Crew:
    # Immutable crew “resource” record loaded from CSV.
    # frozen=True prevents accidental mutation during scheduling/validation.
    crew_id: str
    home_base: str
    max_range_miles: int

    def validate(self) -> None:
        # Fail fast on bad input data so downstream scheduling logic can trust objects.
        if not self.crew_id:
            raise ValueError("crew_id must not be empty")
        if not self.home_base:
            raise ValueError(f"{self.crew_id}: home_base must not be empty")
        if not isinstance(self.max_range_miles, int) or self.max_range_miles <= 0:
            raise ValueError(f"{self.crew_id}: max_range_miles must be a positive integer")

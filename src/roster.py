from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .flight import Flight


@dataclass
class Roster:
    # Core data structure required :
    # Key = crew_id, Value = list of Flight objects (kept sorted by departure time).
    schedule: Dict[str, List[Flight]] = field(default_factory=dict)

    def assign(self, crew_id: str, flight: Flight) -> None:
        # Maintain the "sorted by departure" invariant after every assignment,
        # so validation and reporting can assume chronological order.
        if crew_id not in self.schedule:
            self.schedule[crew_id] = []
        self.schedule[crew_id].append(flight)
        self.schedule[crew_id].sort(key=lambda f: f.departure)

    def get_flights(self, crew_id: str) -> List[Flight]:
        # Return a copy so callers can’t accidentally mutate internal state.
        return list(self.schedule.get(crew_id, []))

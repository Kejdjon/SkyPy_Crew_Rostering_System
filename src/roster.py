from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .flight import Flight


@dataclass
class Roster:
    # Key = crew_id, Value = list of Flight objects (sorted by departure)
    schedule: Dict[str, List[Flight]] = field(default_factory=dict)

    def assign(self, crew_id: str, flight: Flight) -> None:
        if crew_id not in self.schedule:
            self.schedule[crew_id] = []
        self.schedule[crew_id].append(flight)
        self.schedule[crew_id].sort(key=lambda f: f.departure)

    def get_flights(self, crew_id: str) -> List[Flight]:
        return list(self.schedule.get(crew_id, []))

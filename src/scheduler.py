from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .crew import Crew
from .flight import Flight
from .roster import Roster
from .validator import can_assign_next


@dataclass
class ScheduleResult:
    roster: Roster
    unassigned: List[Flight]


def generate_schedule(flights: List[Flight], crew_list: List[Crew]) -> ScheduleResult:
    """
    Greedy scheduler:
    - Sort flights by departure
    - For each flight, try crews in given order, assign to first that fits
    - If none fit, mark unassigned
    """
    flights_sorted = sorted(flights, key=lambda f: f.departure)
    roster = Roster()
    unassigned: List[Flight] = []

    # Ensure roster has keys for every crew 
    for c in crew_list:
        roster.schedule.setdefault(c.crew_id, [])

    for fl in flights_sorted:
        placed = False
        reasons = set()
        for crew in crew_list:
            current = roster.schedule.get(crew.crew_id, [])
            ok, reason = can_assign_next(crew, current, fl)
            if ok:
                roster.assign(crew.crew_id, fl)
                placed = True
                break
            reasons.add(reason)
        if not placed:
            reasons_str = ", ".join(sorted(reasons))
            print(f"Unassigned: {fl.flight_id} (reasons: {reasons_str})")
            unassigned.append(fl)

    return ScheduleResult(roster=roster, unassigned=unassigned)

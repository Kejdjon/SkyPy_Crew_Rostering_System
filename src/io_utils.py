from __future__ import annotations

import csv
from typing import Dict, List

from .crew import Crew
from .flight import Flight, parse_iso_utc


def load_flights_csv(path: str) -> List[Flight]:
    flights: List[Flight] = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fl = Flight(
                flight_id=row["flight_id"].strip(),
                origin=row["origin"].strip(),
                destination=row["destination"].strip(),
                departure=parse_iso_utc(row["departure"]),
                arrival=parse_iso_utc(row["arrival"]),
                distance_miles=int(row["distance_miles"]),
            )
            fl.validate()
            flights.append(fl)
    return flights


def load_crew_csv(path: str) -> List[Crew]:
    crew_list: List[Crew] = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c = Crew(
                crew_id=row["crew_id"].strip(),
                home_base=row["home_base"].strip(),
                max_range_miles=int(row["max_range_miles"]),
            )
            c.validate()
            crew_list.append(c)
    return crew_list


def crew_by_id(crew_list: List[Crew]) -> Dict[str, Crew]:
    return {c.crew_id: c for c in crew_list}

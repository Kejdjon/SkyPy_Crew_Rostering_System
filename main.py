from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from src.io_utils import load_flights_csv, load_crew_csv, crew_by_id
from src.scheduler import generate_schedule
from src.validator import validate_roster


def roster_to_json_dict(roster, crew_map) -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    for crew_id, flights in roster.schedule.items():
        total_minutes = sum(f.duration_minutes for f in flights)
        total_hours = round(total_minutes / 60.0, 2)

        out[crew_id] = {
            "flights": [f.flight_id for f in flights],
            "total_hours": total_hours,
        }

    return out


def main() -> None:
    data_dir = Path("data")
    flights_path = data_dir / "flight.csv"   
    crew_path = data_dir / "crew.csv"

    flights = load_flights_csv(str(flights_path))
    crew_list = load_crew_csv(str(crew_path))
    crew_map = crew_by_id(crew_list)

    result = generate_schedule(flights, crew_list)

    # Validate final roster 
    errors = validate_roster(result.roster, crew_map)
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(f"- {e.crew_id}: {e.message}")
    else:
        print("Roster is valid ")

    if result.unassigned:
        print("\nUnassigned flights:")
        for f in result.unassigned:
            print(f"- {f.flight_id} ({f.origin}->{f.destination} at {f.departure.isoformat()})")

    output = roster_to_json_dict(result.roster, crew_map)
    out_path = Path("outputs")/"output_roster.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()

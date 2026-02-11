from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from src.io_utils import load_flights_csv, load_crew_csv, crew_by_id
from src.scheduler import generate_schedule
from src.validator import validate_roster
from src.roster import Roster

def roster_to_json_dict(roster:Roster) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    """
    Convert the internal Roster (crew_id -> List[Flight]) into the required JSON shape:
      - flight IDs per crew
      - total_hours per crew (sum of flight durations)
    """

    for crew_id, flights in roster.schedule.items():
        # Total flying time is derived from Flight.duration_minutes.
        total_minutes = sum(f.duration_minutes for f in flights)
        total_hours = round(total_minutes / 60.0, 2)

        out[crew_id] = {
            "flights": [f.flight_id for f in flights],
            "total_hours": total_hours,
        }

    return out


def main() -> None:
    # Input folder layout (data/*.csv).
    data_dir = Path("data")
    flights_path = data_dir / "flight.csv"   
    crew_path = data_dir / "crew.csv"

    # Load + validate domain objects from CSV (fail-fast on invalid rows).
    flights = load_flights_csv(str(flights_path))
    crew_list = load_crew_csv(str(crew_path))

    # Build mapping for validator: crew_id -> Crew (used in validate_roster).
    crew_map = crew_by_id(crew_list)

    # Run greedy scheduler to assign flights to crews while enforcing constraints incrementally.
    result = generate_schedule(flights, crew_list)

    # Ensures the final roster respects range + home base start + continuity + dynamic rest for every crew chain.
    errors = validate_roster(result.roster, crew_map)
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(f"- {e.crew_id}: {e.message}")
    else:
        print("Roster is valid ")

    # Reporting: show which flights could not be assigned under the rules.
    if result.unassigned:
        print("\nUnassigned flights:")
        for f in result.unassigned:
            print(f"- {f.flight_id} ({f.origin}->{f.destination} at {f.departure.isoformat()})")

    # Export roster to outputs/output_roster.json in the required structure.
    output = roster_to_json_dict(result.roster)
    out_path = Path("outputs")/"output_roster.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()

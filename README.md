# SkyPy Crew Rostering System

A backend scheduling engine that assigns airline crews to flights while enforcing real-world aviation constraints such as **crew range certification**, **home base rules**, **flight continuity**, and **dynamic rest requirements**.

This project was developed as part of a technical test and demonstrates **clean Python architecture**, **domain modeling**, **validation logic**, and **scheduling algorithms**.

---

## Project Overview

The system:

- Reads flight and crew data from CSV files
- Builds an internal roster (crew → flight assignments)
- Uses a greedy scheduling algorithm
- Enforces aviation rules:
  - Crew maximum range
  - Home base start rule
  - Flight continuity (destination → next origin)
  - Dynamic rest time based on previous flight duration

Produces:

- A validated roster
- A list of unassigned flights with explanations
- A JSON output file

---

## Key Design Decisions

- **Dataclasses** for immutable domain models (`Crew`, `Flight`)
- **Separation of concerns**
  - Parsing: `io_utils.py`
  - Scheduling: `scheduler.py`
  - Validation: `validator.py`
  - Data model: `crew.py`, `flight.py`, `roster.py`
- **Greedy algorithm** for simplicity and performance
- **Post-scheduling validation** to ensure correctness
- **Type hints** throughout for clarity and tooling support

---

## Project Structure

```text
skypy-crew-rostering-system/
├─ src/
│  ├─ crew.py          # Crew domain model
│  ├─ flight.py        # Flight domain model and time parsing
│  ├─ roster.py        # Roster (crew to flights)
│  ├─ io_utils.py      # CSV loaders
│  ├─ scheduler.py     # Greedy scheduling algorithm
│  └─ validator.py     # Rule enforcement and validation
├─ data/
│  ├─ crew.csv
│  └─ flight.csv
├─ outputs/
│  └─ output_roster.json
├─ tests/
│  └─ test_rules.py
├─ main.py             # Program entry point
├─ requirements.txt
├─ pytest.ini
└─ README.md
```

## Scheduling Rules Implemented

### Range rule
A crew can only operate flights within their certified maximum range.

### Home base start rule
The first assigned flight must depart from the crew’s home base.

### Continuity rule
A crew must end a flight at the same airport where the next flight begins.

### Dynamic rest rule
- Flight shorter than 3 hours → **60 minutes** rest  
- Flight equal to or longer than 3 hours → **120 minutes** rest  

## Validation Result
### Crew Roster Output

```json
{
  "C001": {
    "flights": [
      "FL001",
      "FL002",
      "FL006",
      "FL007",
      "FL008"
    ],
    "total_hours": 10.5
  },
  "C002": {
    "flights": [
      "FL003",
      "FL004",
      "FL010",
      "FL011",
      "FL012"
    ],
    "total_hours": 22.5
  },
  "C003": {
    "flights": [
      "FL005",
      "FL014",
      "FL015"
    ],
    "total_hours": 14.5
  },
  "C004": {
    "flights": [
      "FL018",
      "FL019"
    ],
    "total_hours": 3.0
  },
  "C005": {
    "flights": [],
    "total_hours": 0.0
  },
  "C006": {
    "flights": [
      "FL017"
    ],
    "total_hours": 1.5
  },
  "C007": {
    "flights": [
      "FL016"
    ],
    "total_hours": 1.5
  },
  "C008": {
    "flights": [
      "FL009"
    ],
    "total_hours": 3.0
  },
  "C009": {
    "flights": [],
    "total_hours": 0.0
  },
  "C010": {
    "flights": [
      "FL013"
    ],
    "total_hours": 3.0
  }
}
```





### List of unassigned flights with explanations

- **FL020**  
  - Route: `LHR → JFK`  
  - Departure: `2026-02-05T13:00:00+00:00`  
  - Reasons: `continuity`, `home_base_start`, `range`

- **FL021**  
  - Route: `JFK → SYD`  
  - Departure: `2026-02-06T08:00:00+00:00`  
  - Reason: `range`
---


# Productivime

A small, arcade-style productivity game built with Python and Pygame. Carry task cards from To Do to In Progress to Done while dodging moving distractor tags. Earn points for correct flow, lose points for mistakes or collisions, and race the clock to meet the delivery target.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Game Rules](#game-rules)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Run](#run)
- [Configuration](#configuration)

## About
Kanban Carrier is a mini game designed to demonstrate a simple gameplay loop, OOP scene architecture, scoring, persistent leaderboards via SQLite, and lightweight UX polish. It’s suitable as a coding exercise, test assignment, or educational prototype.

## Features
- Three-zone board: To Do (left), In Progress (right‑upper), Done (bottom).
- Player movement with arrows/WASD and clamped play area under a HUD header.
- Task flow: To Do → In Progress → Done with scoring and penalties for skipping.
- Auto‑pickup near To Do, visual “carried” state, soft zone highlighting.
- Distractors: vertical moving text tags in the right band; collisions apply penalties and a short post‑hit invulnerability.
- Win/Lose conditions: deliver TARGET_N tasks under TIME_LIMIT; lose if score drops to 0 or time runs out.
- SQLite leaderboard: records name, score, delivered, time, reason, timestamp; Top‑5 screen.
- Modular OOP: scenes, board, player, task, obstacle, HUD, and DB manager.

## Game Rules
- Move to the To Do card to auto‑pickup (within range), then deliver in order to In Progress and then to Done.
- Correct transitions grant points; skipping stages or colliding with distractors subtracts points and can reset the card to To Do.
- The run ends when:
  - Win: delivered TARGET_N tasks before TIME_LIMIT.
  - Time up: TIME_LIMIT reached without meeting target.
  - Score depleted: score ≤ 0 at any time.

## Screenshots
<img width="1591" height="1117" alt="image" src="https://github.com/user-attachments/assets/42b77064-84c2-4616-aca6-4fbd55206f6d" />

## Tech Stack
- Python 3.10+
- Pygame 2.x
- SQLite (sqlite3 from the Python standard library)

## Project Structure
- run.py — entry point and main loop
- settings.py — constants (window, colors, gameplay params)
- core/
  - scene_manager.py — base Scene and manager
  - ui.py — HUD, Label, Button
- scenes/
  - menu.py — main menu
  - input_name.py — name entry screen
  - play.py — gameplay scene
  - game_over.py — results + save to DB
  - leaderboard.py — Top‑5
- game/
  - board.py — zones geometry/drawing
  - player.py — movement and clamping
  - task.py — TaskCard and stages
  - obstacle.py — ObstacleTag (distractors)
- data/
  - db.py — DBManager (init/insert/top5)
  - scores.db — SQLite database (auto‑created)

## Getting Started
Prerequisites:
- Python 3.10+ installed
- Recommended: virtual environment

Setup:
- Clone:

```bash
git clone https://github.com/davy1ex/Productivime
cd Productivime
```

- Create a virtual environment
  - Linux/macOS:
    - `python -m venv .venv`
    - `source .venv/bin/activate`
  - Windows (PowerShell):
    - `python -m venv .venv`
    - `.\\.venv\\Scripts\\Activate.ps1`
- Upgrade pip and install dependencies
  - `python -m pip install --upgrade pip`
  - `pip install pygame`
- Optional: freeze requirements
  - `pip freeze > requirements.txt`

## Run
- From the project root:
  - `python run.py`
- Flow:
  - Menu → Start → Enter name → Play
  - ESC in Play opens Game Over
  - From Game Over: Play Again or Leaderboard

## Configuration
Adjust key parameters in `settings.py`:

- Window: `WIDTH`, `HEIGHT`, `FPS`, `TITLE`
- HUD/UI: `HUD_HEIGHT`, pastel zone colors and borders
- Player: `PLAYER_SIZE`, `PLAYER_SPEED`
- Tasks:
  - `TASK_SIZE`, `TASK_TITLES` (random short titles)
- Scoring:
  - `SCORE_TO_PROGRESS`, `SCORE_TO_DONE`
  - `PENALTY_SKIP_STAGE`, `PENALTY_HIT_DISTRACTOR`
  - `START_SCORE` (initial score)
- Run:
  - `TIME_LIMIT` (seconds), `TARGET_N` (tasks to deliver)
- Distractors:
  - `DISTRACTOR_WORDS` (list of short tags)
  - Spawn/speed tuning: `DISTRACTOR_SPAWN_INTERVAL`, `DISTRACTOR_MIN_INTERVAL`, `DISTRACTOR_MIN_SPEED`, `DISTRACTOR_MAX_SPEED`, `DISTRACTOR_DIFFICULTY_STEP`, `DISTRACTOR_STEP_TIME`
- Leaderboard DB:
  - DB path configured in `data/db.py` (default `data/scores.db`, auto‑created)


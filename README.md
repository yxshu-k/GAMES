# Game Collection — Python Mini-Games

This repository is a small collection of standalone Python game scripts and demos. Each file is intended to be runnable on its own from the project root.

Project structure
- `algorithm_arena.py` — small scripts or exercises for algorithm demonstrations and testing.
- `Flower.py` — an interactive demo or small game named "Flower" (check the file header for controls).
- `Game.py` — shared helper utilities or a main entrypoint used by one or more games.
- `magic.py` — "magic" themed script; likely the one you run most recently.
- `memory_match.py` — a memory card matching game.
- `neon_drift_runner.py` — runner-style arcade game with a neon theme.
- `time_echo.py` — a small time/echo demonstration (input/echo/time-based behavior).
- `Treasure_hunt.py` — a treasure-hunt style game or demo.

Prerequisites
- Python 3.8 or newer.
- No additional packages are assumed. If a script requires extras, the top of that script will usually note them (e.g. `pygame`).

Recommended setup (optional)
1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. If a game requires dependencies (see file header), install them with `pip`.

How to run
1. Open a terminal in this folder.
2. Run any script directly, for example:

```powershell
python magic.py
python memory_match.py
```

Tips
- If a script imports `pygame` or other libraries, install them before running: `pip install pygame`.
- On Windows PowerShell, use `python` (not `python3`) if your PATH maps `python` to the correct interpreter.

Per-game notes
- Look at the top of each script for usage hints, required assets, or control mappings.
- If a game opens a window and nothing appears, ensure required assets (images/sounds) live in the same folder or follow paths referenced in the script.

Contributing
- Add new games as standalone `.py` files and include a short header comment explaining controls and any dependencies.

License
- No license is specified. Add a `LICENSE` file if you want to set one (MIT or similar recommended for small projects).

Contact / Support
- If you want the README expanded with screenshots, control diagrams, or a requirements file, tell me which games you want documented and I will add those sections.

Enjoy!

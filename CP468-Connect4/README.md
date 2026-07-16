# CP468 Connect Four - Starter

## Setup

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Game

### Option 1: Tkinter GUI (This is not woring)
```powershell
python play_game.py
```

### Option 2: PySimpleGUI (alternative if Tkinter has display issues)
```powershell
.\.venv\bin\python.exe play_game_psgui.py
```

### Option 3: Interactive Text-based Demo
```powershell
.\.venv\bin\python.exe demo.py
```

This launches a menu where you can choose to run different agent matchups and watch games play out move-by-move.

## Run Tests
```powershell
.\.venv\bin\python.exe -m pytest -q
```

## Run Experiments
```powershell
.\.venv\bin\python.exe experiments/run_experiments.py --seed 42
```

## Notes
- Agents use a seedable random.Random instance for reproducibility.
- Minimax uses fixed depth 4 by default in experiments.
- The game window requires a display; it will not work in remote/headless environments.

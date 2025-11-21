# Connect Four with Minimax

This project implements a playable Connect Four game with a time-bounded Minimax AI.

- A human can play against the AI.
- Two AIs can play against each other (self-play).
- The AI uses Minimax with iterative deepening and a heuristic evaluation tailored to Connect Four.
- Alpha–beta pruning is implemented (enabled by default) to search deeper under a fixed per-move time limit.

The board is the standard **6 rows × 7 columns**. Players alternate dropping discs into a column; pieces fall to the lowest empty cell.  
- **Win:** first to connect 4 horizontally, vertically, or diagonally.  
- **Draw:** board is full with no winner.  
- **Illegal move:** choosing a full column (rejected and not applied).

---
# HOW TO RUN

## AI VS AI

#### Minimax vs Random
```bash
python3 main.py --mode ai-ai --seconds 1 --ai1 MinimaxAgent --ai2 RandomAgent --first 1 --games 1
```

#### Strength vs RandomAgent (Recommended Test)
```bash
python3 main.py --mode ai-ai --seconds 1 --ai1 MinimaxAgent --ai2 RandomAgent --games 1
```

#### Minimax Starts as Player 2
```bash
python3 main.py --mode ai-ai --seconds 1 --ai1 MinimaxAgent --ai2 RandomAgent --first 2 --games 1
```

#### 50-Game Evaluation (for Assignment Report)
```bash
python3 main.py --mode ai-ai --seconds 1 --ai1 MinimaxAgent --ai2 RandomAgent --games 50 --first 1
```

### Human vs AI

#### Human as Player 1
```bash
python3 main.py --mode human-ai --seconds 2 --ai1 MinimaxAgent --first 1
```

#### AI Starts First (Human is Player 2)
```bash
python3 main.py --mode human-ai --seconds 2 --ai1 MinimaxAgent --first 2
```


## REQUIREMENTS

- **Python**: 3.8+ (standard library only; no external dependencies)


# heuristics.py
import math
from board import ROWS, COLS, EMPTY, PLAYER1, PLAYER2


def evaluate_board(board, player):
    """Static evaluation from perspective of `player`."""
    winner = board.check_winner()
    if winner == player:
        return math.inf
    elif winner != EMPTY and winner != player:
        return -math.inf
    if board.is_full():
        return 0

    opp = PLAYER1 if player == PLAYER2 else PLAYER2
    grid = board.grid

    score = 0

    # Center column control
    center_col = COLS // 2
    center_array = [grid[r][center_col] for r in range(ROWS)]
    center_count = center_array.count(player)
    score += center_count * 3  # weight center a bit

    # Score all length-4 windows
    def score_window(window):
        score_w = 0
        my_count = window.count(player)
        opp_count = window.count(opp)
        empty_count = window.count(EMPTY)

        if my_count == 4:
            score_w += 100000
        elif my_count == 3 and empty_count == 1:
            score_w += 100
        elif my_count == 2 and empty_count == 2:
            score_w += 10

        if opp_count == 3 and empty_count == 1:
            # Block opponent threats
            score_w -= 80
        elif opp_count == 2 and empty_count == 2:
            score_w -= 5

        return score_w

    # Horizontal windows
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [grid[r][c + i] for i in range(4)]
            score += score_window(window)

    # Vertical windows
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [grid[r + i][c] for i in range(4)]
            score += score_window(window)

    # Diagonal up-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [grid[r + i][c + i] for i in range(4)]
            score += score_window(window)

    # Diagonal up-left
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            window = [grid[r + i][c - i] for i in range(4)]
            score += score_window(window)

    return score

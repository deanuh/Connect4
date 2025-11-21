# board.py
"""
Pure Connect Four rules implementation.

- 6 rows x 7 columns
- Two players: 1 and 2
- Gravity: discs fall to the lowest empty cell in a column
- Win: four in a row horizontally, vertically, or diagonally
- Draw: board full with no winner
"""

ROWS = 6
COLS = 7

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2


class Board:
    def __init__(self):
        # Internal representation:
        #   grid[row][col] where row 0 is the *bottom* of the board
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    # core game rules

    def get_legal_moves(self):
        """Return list of columns (0–6) that are not full."""
        return [c for c in range(COLS) if self.grid[ROWS - 1][c] == EMPTY]

    def is_column_full(self, col):
        """True if no checker can be dropped in this column."""
        if col < 0 or col >= COLS:
            return True
        return self.grid[ROWS - 1][col] != EMPTY

    def make_move(self, col, player):
        """
        Drop a checker of `player` into column `col`.
        Return True if the move is legal and applied, False if column is full or out of range.
        """
        if col < 0 or col >= COLS:
            return False
        if self.is_column_full(col):
            return False

        # Gravity: find the lowest empty row in this column
        for r in range(ROWS):
            if self.grid[r][col] == EMPTY:
                self.grid[r][col] = player
                return True

        # Should never reach here because we checked is_column_full
        return False

    def undo_move(self, col):
        """
        Remove the *topmost* checker from column `col`.
        Useful for search (minimax). No-op if column empty.
        """
        for r in reversed(range(ROWS)):
            if self.grid[r][col] != EMPTY:
                self.grid[r][col] = EMPTY
                return

    def is_full(self):
        """Return True if the whole board is full (draw if no winner)."""
        return all(self.grid[ROWS - 1][c] != EMPTY for c in range(COLS))

    # win & terminal checks 

    def check_winner(self):
        """
        Return:
          PLAYER1 if player 1 has four in a row,
          PLAYER2 if player 2 has four in a row,
          EMPTY   if no winner.
        """
        g = self.grid

        # Horizontal ( ---- )
        for r in range(ROWS):
            for c in range(COLS - 3):
                window = [g[r][c + i] for i in range(4)]
                if window[0] != EMPTY and all(x == window[0] for x in window):
                    return window[0]

        # Vertical ( | )
        for c in range(COLS):
            for r in range(ROWS - 3):
                window = [g[r + i][c] for i in range(4)]
                if window[0] != EMPTY and all(x == window[0] for x in window):
                    return window[0]

        # Diagonal up-right ( / )
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [g[r + i][c + i] for i in range(4)]
                if window[0] != EMPTY and all(x == window[0] for x in window):
                    return window[0]

        # Diagonal up-left ( \ )
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                window = [g[r + i][c - i] for i in range(4)]
                if window[0] != EMPTY and all(x == window[0] for x in window):
                    return window[0]

        return EMPTY

    def is_terminal(self):
        """True if game is over: someone won or board is full."""
        return self.check_winner() != EMPTY or self.is_full()


    def __str__(self):
        """
        Render the board in ASCII.

        Top row printed last, so visually it matches the real game.
        PLAYER1 -> 'X'
        PLAYER2 -> 'O'
        EMPTY   -> '.'
        """
        lines = []
        for r in reversed(range(ROWS)):
            line = "|"
            for c in range(COLS):
                v = self.grid[r][c]
                if v == PLAYER1:
                    line += "X"
                elif v == PLAYER2:
                    line += "O"
                else:
                    line += "."
            line += "|"
            lines.append(line)
        lines.append(" " + "".join(str(c) for c in range(COLS)))
        return "\n".join(lines)


#  simple human vs human 

def play_human_vs_human():
    board = Board()
    current = PLAYER1

    print("Connect Four – Human vs Human")
    print("Player 1 = X, Player 2 = O")
    print(board)

    while not board.is_terminal():
        print()
        print(f"Player {current} ({'X' if current == PLAYER1 else 'O'}) turn.")
        try:
            col = int(input("Choose a column (0-6): "))
        except ValueError:
            print("Please enter an integer between 0 and 6.")
            continue

        if not board.make_move(col, current):
            print("Illegal move (column full or out of range). Try again.")
            continue

        print(board)

        # Switch player
        current = PLAYER1 if current == PLAYER2 else PLAYER2

    print()
    winner = board.check_winner()
    if winner == EMPTY:
        print("Game over: draw (board is full).")
    else:
        print(f"Game over: Player {winner} wins!")


if __name__ == "__main__":
    play_human_vs_human()

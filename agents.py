# agents.py
import random
import time
import math

from board import Board, EMPTY, PLAYER1, PLAYER2, COLS
from heuristics import evaluate_board


class Agent:
    def __init__(self, player_id):
        self.player_id = player_id

    def select_move(self, board, seconds):
        """Return chosen column index."""
        raise NotImplementedError


class RandomAgent(Agent):
    def select_move(self, board, seconds):
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None
        return random.choice(legal_moves)


class SearchTimeout(Exception):
    """Raised when the search has exceeded the allotted time."""
    pass


class MinimaxAgent(Agent):
    def __init__(self, player_id, use_alpha_beta=True, max_depth=20):
        super().__init__(player_id)
        self.use_alpha_beta = use_alpha_beta
        self.max_depth = max_depth

    def select_move(self, board, seconds):
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None

        deadline = time.perf_counter() + seconds
        best_move = random.choice(legal_moves)  # fallback
        best_value = -math.inf

        # center-first ordering is good in Connect Four
        center = COLS // 2
        move_order = sorted(legal_moves, key=lambda c: abs(c - center))

        depth = 1
        while depth <= self.max_depth:
            if time.perf_counter() >= deadline:
                break
            try:
                value, move = self._search_depth(board, depth, deadline, move_order)
                if move is not None:
                    best_value = value
                    best_move = move
                depth += 1
            except SearchTimeout:
                # Could not finish this depth; return best from last completed depth
                break

        return best_move

    # Fixed-depth search
    def _search_depth(self, board, depth, deadline, move_order):
        """Search to fixed depth with minimax (and optional alpha–beta)."""
        best_value = -math.inf
        best_move = None

        for move in move_order:
            if time.perf_counter() >= deadline:
                raise SearchTimeout()

            if not board.make_move(move, self.player_id):
                continue

            try:
                if self.use_alpha_beta:
                    value = self._min_value(board, depth - 1,
                                            -math.inf, math.inf, deadline)
                else:
                    value = self._min_value_plain(board, depth - 1, deadline)
            finally:
                # ALWAYS undo the move, even if timeout happens
                board.undo_move(move)

            if value > best_value:
                best_value = value
                best_move = move

        return best_value, best_move

    # Alpha–beta minimax

    def _max_value(self, board, depth, alpha, beta, deadline):
        if time.perf_counter() >= deadline:
            raise SearchTimeout()
        if depth == 0 or board.is_terminal():
            return evaluate_board(board, self.player_id)

        value = -math.inf
        center = COLS // 2
        for move in sorted(board.get_legal_moves(), key=lambda c: abs(c - center)):
            if time.perf_counter() >= deadline:
                raise SearchTimeout()

            if not board.make_move(move, self.player_id):
                continue

            try:
                value = max(
                    value,
                    self._min_value(board, depth - 1, alpha, beta, deadline),
                )
            finally:
                board.undo_move(move)

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def _min_value(self, board, depth, alpha, beta, deadline):
        if time.perf_counter() >= deadline:
            raise SearchTimeout()
        if depth == 0 or board.is_terminal():
            return evaluate_board(board, self.player_id)

        value = math.inf
        opp = PLAYER1 if self.player_id == PLAYER2 else PLAYER2
        center = COLS // 2
        for move in sorted(board.get_legal_moves(), key=lambda c: abs(c - center)):
            if time.perf_counter() >= deadline:
                raise SearchTimeout()

            if not board.make_move(move, opp):
                continue

            try:
                value = min(
                    value,
                    self._max_value(board, depth - 1, alpha, beta, deadline),
                )
            finally:
                board.undo_move(move)

            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    # Plain minimax (no alpha–beta) for comparison / ablation

    def _max_value_plain(self, board, depth, deadline):
        if time.perf_counter() >= deadline:
            raise SearchTimeout()
        if depth == 0 or board.is_terminal():
            return evaluate_board(board, self.player_id)

        value = -math.inf
        for move in board.get_legal_moves():
            if time.perf_counter() >= deadline:
                raise SearchTimeout()

            if not board.make_move(move, self.player_id):
                continue

            try:
                value = max(
                    value,
                    self._min_value_plain(board, depth - 1, deadline),
                )
            finally:
                board.undo_move(move)

        return value

    def _min_value_plain(self, board, depth, deadline):
        if time.perf_counter() >= deadline:
            raise SearchTimeout()
        if depth == 0 or board.is_terminal():
            return evaluate_board(board, self.player_id)

        value = math.inf
        opp = PLAYER1 if self.player_id == PLAYER2 else PLAYER2
        for move in board.get_legal_moves():
            if time.perf_counter() >= deadline:
                raise SearchTimeout()

            if not board.make_move(move, opp):
                continue

            try:
                value = min(
                    value,
                    self._max_value_plain(board, depth - 1, deadline),
                )
            finally:
                board.undo_move(move)

        return value

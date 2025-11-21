# game.py
import random

from board import Board, EMPTY, PLAYER1, PLAYER2
from agents import RandomAgent, MinimaxAgent


def create_agent(name, player_id):
    """Map string to agent instance."""
    if name == "RandomAgent":
        return RandomAgent(player_id)
    elif name == "MinimaxAgent":
        return MinimaxAgent(player_id)
    else:
        raise ValueError(f"Unknown agent class: {name}")


def print_board(board):
    print(board)
    print()


def human_turn(board, player_id):
    while True:
        try:
            col = int(input(f"Player {player_id} - choose column (0-6): "))
        except ValueError:
            print("Please enter an integer 0-6.")
            continue
        if col in board.get_legal_moves():
            board.make_move(col, player_id)
            break
        else:
            print("Illegal move (column full or out of range). Try again.")


def ai_turn(board, agent, seconds):
    move = agent.select_move(board, seconds)
    if move is None or move not in board.get_legal_moves():
        # Safety fallback
        legal = board.get_legal_moves()
        move = random.choice(legal) if legal else None
    if move is not None:
        board.make_move(move, agent.player_id)
    return move


def play_human_ai(ai1_name, seconds, first_player):
    board = Board()

    if first_player == 1:
        # Human goes first as Player 1
        human_player = PLAYER1
        ai_player = PLAYER2
    else:
        # AI goes first as Player 1
        human_player = PLAYER2
        ai_player = PLAYER1


    ai_agent = create_agent(ai1_name, ai_player)

    current = PLAYER1
    while not board.is_terminal():
        print_board(board)
        if current == human_player:
            human_turn(board, human_player)
        else:
            print(f"AI (Player {ai_player}) thinking...")
            ai_turn(board, ai_agent, seconds)
        current = PLAYER1 if current == PLAYER2 else PLAYER2

    print_board(board)
    winner = board.check_winner()
    if winner == EMPTY:
        print("Game over: draw.")
    else:
        who = "Human" if winner == human_player else "AI"
        print(f"Game over: {who} (Player {winner}) wins!")


def play_ai_ai(ai1_name, ai2_name, seconds, first_player, games=1):
    """Run AI vs AI; return stats (wins/draws)."""
    ai1_wins = 0
    ai2_wins = 0
    draws = 0

    for g in range(games):
        board = Board()
        if first_player == 1:
            p1_agent = create_agent(ai1_name, PLAYER1)
            p2_agent = create_agent(ai2_name, PLAYER2)
        else:
            p1_agent = create_agent(ai2_name, PLAYER1)
            p2_agent = create_agent(ai1_name, PLAYER2)

        current = PLAYER1
        while not board.is_terminal():
            # Note: no prints to keep self-play fast
            if current == PLAYER1:
                ai_turn(board, p1_agent, seconds)
            else:
                ai_turn(board, p2_agent, seconds)
            current = PLAYER1 if current == PLAYER2 else PLAYER2

        winner = board.check_winner()
        if winner == PLAYER1:
            if first_player == 1:
                ai1_wins += 1
            else:
                ai2_wins += 1
        elif winner == PLAYER2:
            if first_player == 1:
                ai2_wins += 1
            else:
                ai1_wins += 1
        else:
            draws += 1

    return ai1_wins, draws, ai2_wins

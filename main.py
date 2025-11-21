# main.py
import argparse
import random

from game import play_human_ai, play_ai_ai


def main():
    parser = argparse.ArgumentParser(description="Connect Four with Minimax AI")
    parser.add_argument("--mode", choices=["human-ai", "ai-ai"], required=True)
    parser.add_argument("--seconds", type=float, default=2.0,
                        help="Per-move time limit in seconds.")
    parser.add_argument("--ai1", type=str, default="RandomAgent",
                        help="Agent class name for AI 1.")
    parser.add_argument("--ai2", type=str, default="RandomAgent",
                        help="Agent class name for AI 2 (only in ai-ai mode).")
    parser.add_argument("--first", type=int, choices=[1, 2], default=1,
                        help="Which player moves first (1 or 2).")
    parser.add_argument("--games", type=int, default=1,
                        help="Number of games for ai-ai mode.")
    parser.add_argument("--seed", type=int, default=0,
                        help="Random seed for determinism.")

    args = parser.parse_args()
    random.seed(args.seed)

    if args.mode == "human-ai":
        play_human_ai(ai1_name=args.ai1,
                      seconds=args.seconds,
                      first_player=args.first)
    else:
        ai1_wins, draws, ai2_wins = play_ai_ai(
            ai1_name=args.ai1,
            ai2_name=args.ai2,
            seconds=args.seconds,
            first_player=args.first,
            games=args.games,
        )
        print(f"Results over {args.games} games:")
        print(f"AI1 wins: {ai1_wins}")
        print(f"Draws:    {draws}")
        print(f"AI2 wins: {ai2_wins}")


if __name__ == "__main__":
    main()

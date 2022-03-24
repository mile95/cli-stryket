from __future__ import annotations
from fake_data_generator import GAMES, generate_random_goal
from read_input import read_input

import sys
import time
import curses

HEADER = "Stryktipset v12 2022-03-12"

TABLE_START_ROW_INDEX = 4
TABLE_END_ROW_INDEX = TABLE_START_ROW_INDEX + 13
RESULT_START_COL_INDEX = 30
SYSTEM_START_COL_INDEX = 45
stdscr = curses.initscr()

if curses.has_colors():
    curses.start_color()
    curses.use_default_colors()

    # -1 gives transparent background
    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)
    curses.init_pair(4, curses.COLOR_RED, -1)


def score_to_sign(score: str) -> str:
    home = int(score.split("-")[0])
    away = int(score.split("-")[1])

    if home > away:
        return "1"
    if home < away:
        return "2"
    return "x"


def update(system: str, scores: list(str)) -> list(str):
    scores = generate_random_goal(scores)
    correct = 0
    for i, row in enumerate(system):
        stdscr.addstr(TABLE_START_ROW_INDEX + i, 0, f"{i+1}. {GAMES[i]}")
        stdscr.addstr(TABLE_START_ROW_INDEX + i, RESULT_START_COL_INDEX, scores[i])
        for k, sign in enumerate(row):
            correct += sign in score_to_sign(scores[i])
            stdscr.addstr(
                TABLE_START_ROW_INDEX + i,
                SYSTEM_START_COL_INDEX + k,
                sign,
                curses.color_pair(2)
                if sign in score_to_sign(scores[i])
                else curses.color_pair(4),
            )
            stdscr.refresh()

    stdscr.addstr(TABLE_END_ROW_INDEX + 1, 0, "")
    stdscr.addstr(TABLE_END_ROW_INDEX + 2, 0, f"Antal rätt: {correct}")
    stdscr.addstr(TABLE_END_ROW_INDEX + 3, 0, "")
    return scores


def render(system: list(str)) -> int:
    stdscr.addstr(0, 0, HEADER, curses.color_pair(1))
    stdscr.addstr(2, 0, "Matcher")
    stdscr.addstr(2, RESULT_START_COL_INDEX, "Resultat")
    stdscr.addstr(2, SYSTEM_START_COL_INDEX, "System")

    scores = ["0-0"] * 13
    while True:
        scores = update(system, scores)
        time.sleep(2)


def main() -> int:
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Please provide the filename with your system")
        return 1

    system = read_input(filename)
    return render(system)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations
from random import randrange

import sys
import time
import curses

HEADER = "Stryktipset v12 2022-03-12"
GAMES = [
    "England - Schweiz",
    "Nederland - Danmark",
    "Finland - Island",
    "Irland - Belgien",
    "Spanien - Albanien",
    "Tyskland - Israel",
    "Ipswich - Plymouth",
    "Accringt. - Gillingh.",
    "AFC Wimb. - Cambridge",
    "Doncaster - Charlton",
    "Sheff.W - Cheltenh.",
    "Shrewsb. - Lincoln",
    "Port Vale - Sutton U",
]

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


class InvalidSystemException(Exception):
    pass


def parse_input_file(filename: str) -> list(str):
    with open(filename) as f:
        raw_system = f.read().split("\n")

    return raw_system


def validate_system(system: list(str)) -> list(str):
    system = [row for row in system if row]  # Remove empty lines
    if len(system) != 13:
        raise InvalidSystemException("System must have 13 rows")
    for i, row in enumerate(system):
        if row not in ["1", "x", "2", "1x", "12", "x2", "1x2"]:
            raise InvalidSystemException(f"Row {i + 1}: {row} is not valid")
    return system


def format_system_row(system_row: str) -> str:
    if len(system_row) == 3:
        return system_row
    if len(system_row) == 2:
        if "1" not in system_row:
            return " x2"
        if "x" not in system_row:
            return "1 2"
        if "2" not in system_row:
            return "1x "
    if len(system_row) == 1:
        if "1" in system_row:
            return "1  "
        if "x" in system_row:
            return " x "
        if "2" in system_row:
            return "  2"


def generate_random_goal(scores: list(str)) -> list(str):
    game_index = randrange(13)
    home = randrange(2) == 0
    if home:
        scores[game_index] = (
            str(int(scores[game_index].split("-")[0]) + 1)
            + "-"
            + scores[game_index].split("-")[1]
        )
    else:
        scores[game_index] = (
            scores[game_index].split("-")[0]
            + "-"
            + str(int(scores[game_index].split("-")[1]) + 1)
        )
    return scores


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
        formatted_row = format_system_row(row)
        for k, sign in enumerate(formatted_row):
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
    return scores


def render(system: list(str)) -> int:
    stdscr.addstr(0, 0, HEADER, curses.color_pair(1))
    stdscr.addstr(2, 0, "Matcher")
    stdscr.addstr(2, RESULT_START_COL_INDEX, "Resultat")
    stdscr.addstr(2, SYSTEM_START_COL_INDEX, "System")

    scores = ["0-0"] * 13
    while True:
        scores = update(system, scores)
        # if stdscr.get_wch() == "\n":
        #    return 0
        time.sleep(2)


def main() -> int:
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Please provide the filename with your system")
        return 1

    raw_system = parse_input_file(filename)
    try:
        system = validate_system(raw_system)
    except InvalidSystemException as e:
        print(f"Invalid system input. {e}")
        return 1

    return render(system)


if __name__ == "__main__":
    raise SystemExit(main())

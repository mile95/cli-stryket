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
RESULT_START_COL_INDEX = 30
SYSTEM_START_COL_INDEX = 45

stdscr = curses.initscr()


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


def update_table(system: str, scores: list(str)) -> list(str):
    scores = generate_random_goal(scores)
    for i, row in enumerate(system):
        stdscr.addstr(TABLE_START_ROW_INDEX + i, 0, f"{i+1}. {GAMES[i]}")
        stdscr.addstr(TABLE_START_ROW_INDEX + i, RESULT_START_COL_INDEX, scores[i])
        stdscr.addstr(TABLE_START_ROW_INDEX + i, SYSTEM_START_COL_INDEX, system[i])
        stdscr.refresh()
    return scores


def render(system: list(str)) -> None:
    stdscr.addstr(HEADER)
    stdscr.addstr(2, 0, "Matcher")
    stdscr.addstr(2, RESULT_START_COL_INDEX, "Resultat")
    stdscr.addstr(2, SYSTEM_START_COL_INDEX, "System")

    scores = ["0-0"] * 13
    while True:
        scores = update_table(system, scores)
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

    render(system)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations
from read_input import read_input
from stryket_scraper import get_game_information, GameStatus

import sys
import time
import curses

HEADER = "Stryktipset v12 2022-03-12"

TABLE_START_ROW_INDEX = 4
TABLE_END_ROW_INDEX = TABLE_START_ROW_INDEX + 13
RESULT_START_COL_INDEX = 45
TIME_START_COL_INDEX = 30
SYSTEM_START_COL_INDEX = 60
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


def update(system: str, games: list(dict)):
    correct = 0
    for i, row in enumerate(system):
        game = games[i]
        home_team = game["home_team"]
        away_team = game["away_team"]
        stdscr.addstr(TABLE_START_ROW_INDEX + i, 0, f"{i+1}. {home_team}-{away_team}")
        if game["status"] in [GameStatus.live, GameStatus.finished]:
            goal_home = game["goals_home"]
            goal_away = game["goals_away"]
            score = f"{goal_home}-{goal_away}"
            stdscr.addstr(
                TABLE_START_ROW_INDEX + i,
                RESULT_START_COL_INDEX,
                score,
            )
            stdscr.addstr(
                TABLE_START_ROW_INDEX + i,
                TIME_START_COL_INDEX,
                "Slut" if game["status"] == GameStatus.finished else game["time"],
            )
        elif game["status"] == GameStatus.not_started:
            score = "0-0"
            stdscr.addstr(TABLE_START_ROW_INDEX + i, RESULT_START_COL_INDEX, score)
            stdscr.addstr(
                TABLE_START_ROW_INDEX + i, TIME_START_COL_INDEX, game["start_time"]
            )
        for k, sign in enumerate(row):
            correct += sign in score_to_sign(score)
            stdscr.addstr(
                TABLE_START_ROW_INDEX + i,
                SYSTEM_START_COL_INDEX + k,
                sign,
                curses.color_pair(2)
                if sign in score_to_sign(score)
                else curses.color_pair(4),
            )

    stdscr.addstr(TABLE_END_ROW_INDEX + 1, 0, "")
    stdscr.addstr(TABLE_END_ROW_INDEX + 2, 0, f"Antal rätt: {correct}")
    stdscr.addstr(TABLE_END_ROW_INDEX + 3, 0, "")
    stdscr.refresh()


def render(system: list(str)) -> int:
    stdscr.addstr(0, 0, HEADER, curses.color_pair(1))
    stdscr.addstr(2, 0, "Matcher")
    stdscr.addstr(2, RESULT_START_COL_INDEX, "Resultat")
    stdscr.addstr(2, TIME_START_COL_INDEX, "Tid")
    stdscr.addstr(2, SYSTEM_START_COL_INDEX, "System")

    while True:
        games = get_game_information()
        update(system, games)
        time.sleep(30)


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

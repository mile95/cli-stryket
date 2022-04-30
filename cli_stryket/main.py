from __future__ import annotations
from cli_stryket.read_input import read_input
from cli_stryket.stryket_scraper import get_game_information, GameStatus
from cli_stryket.stryket_scraper import FetchException
from datetime import datetime

import sys
import time
import curses
import argparse

HEADER = "Stryktipset"
TABLE_START_ROW_INDEX = 4
TABLE_END_ROW_INDEX = TABLE_START_ROW_INDEX + 13
RESULT_START_COL_INDEX = 45
TIME_START_COL_INDEX = 30
SYSTEM_START_COL_INDEX = 60


def score_to_sign(score: str) -> str:
    home = int(score.split("-")[0])
    away = int(score.split("-")[1])

    if home > away:
        return "1"
    if home < away:
        return "2"
    return "x"


def update(stdscr: _Curses.Window, system: str, games: list(dict)):
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
                "End" if game["status"] == GameStatus.finished else game["time"],
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
    latest_updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stdscr.addstr(TABLE_END_ROW_INDEX + 1, 0, "")
    stdscr.addstr(TABLE_END_ROW_INDEX + 2, 0, f"Correct: {correct}")
    stdscr.addstr(TABLE_END_ROW_INDEX + 3, 0, "")
    stdscr.addstr(TABLE_END_ROW_INDEX + 4, 0, f"Last updated: {latest_updated_time}")
    stdscr.addstr(TABLE_END_ROW_INDEX + 6, 0, f"Press [q] to exit (delayed)")
    stdscr.addstr(TABLE_END_ROW_INDEX + 7, 0, "")
    stdscr.refresh()


def render(stdscr: Curses._CursesWindow, args: argparse.Namespace) -> int:
    system = read_input(args.input_file)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()

        # -1 gives transparent background
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)

    stdscr.addstr(0, 0, HEADER, curses.color_pair(1))
    stdscr.addstr(2, 0, "Games")
    stdscr.addstr(2, RESULT_START_COL_INDEX, "Score")
    stdscr.addstr(2, TIME_START_COL_INDEX, "Time")
    stdscr.addstr(2, SYSTEM_START_COL_INDEX, "System")
    stdscr.nodelay(True)

    while True:
        try:
            games = get_game_information()
            update(stdscr, system, games)
        except FetchException as e:
            pass
        if stdscr.getch() == ord("q"):
            return 0
        curses.napms(30 * 1000)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Command Line Application for Stryktipset"
    )
    parser.add_argument("--input-file", type=str, required=True)
    args = parser.parse_args()

    return curses.wrapper(render, args)


if __name__ == "__main__":
    raise SystemExit(main())

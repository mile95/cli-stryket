from __future__ import annotations
import re

from bs4 import BeautifulSoup
from pprint import pprint
from requests_html import HTMLSession
from enum import Enum

URL = "https://spela.svenskaspel.se/resultat/stryktipset"
GAME_DIVS_CLASS = "js-expandable-box"


class GameStatus(Enum):
    live = 1
    finished = 2
    not_started = 3


def get_teams(team_names: list(str)) -> tuple(str, str):
    """Returns the home team and the away team from a raw list of team names.

    Parameters
    __________
    team_names : list(str)
        The raw list of team names. The '-' is used as team delimiter.
        Example:
            ["Port", "Vale", "-", "Lincon"] or ["Arsenal", "-", "Manchester", "United"]

    Returns
    _______
    tuple(str, str)
        A tuple with home team as first element and away team as last element.
        Example:
            ("PortVale", "Licon") or ("Arsenal", "ManchesterUnited")

    """
    home_team = ""
    away_team = ""
    home_team_done = False
    for item in team_names:
        if item == "-":
            home_team_done = True
        elif not home_team_done:
            home_team += item
        else:
            away_team += item
    return (home_team, away_team)


def fetch_raw_data() -> BeautifulSoup:
    """Fetch the raw HTML and JS generated raw data from svenskaspel.

    Returns
    _______
    BeautifulSoup: Soup object with the fully generated page. HTML and JS content.
    """
    session = HTMLSession()
    r = session.get(URL)
    r.html.render()
    session.close()
    return BeautifulSoup(r.html.raw_html, "html.parser")


def extract_game_info(soup: BeautifulSoup) -> list(dict):
    """Extract game information from the soup representation of svenskaspels webpage.

    Parameters
    __________
    soup : BeautifulSoup
        Raw soup representation of the svenskaspels webpage.

    Returns
    _______
    list(dict)
        A list (of len 13) of dict objects representing a game.
        A game is represented by a dict, the keys and values depend
        on the status of the game. The status can be one of
        'GameStatus.live', 'GameStatus.not_started' or 'GameStatus.finished'

        All games have the following keys:
            - status
            - number
            - home_team
            - away_team
        A game with 'GameStatus.live' have the following key/s:
            - goals_home
            - goals_away
            - time
        A game with 'GameStatus.not_started have the following extra key/s:
            - start_time
        A game with 'GameStatus.finished' have the following extra key/s:
            - goals_home
            - goals_away
    """
    game_divs = soup.find_all("div", {"class": GAME_DIVS_CLASS})

    games = []
    for i, div in enumerate(game_divs):
        raw_info = div.get_text().replace("\n", " ").replace("\r", "")
        info_parts = raw_info.split()
        try:
            # All game rows starts with a number between 1 and 13.
            int(info_parts[0])
        except ValueError:
            break

        status = ""
        rev_info_parts = list(reversed(info_parts))
        try:
            # If the game has started, the last item is the score of the away team
            int(rev_info_parts[0])
            status = GameStatus.live
        except ValueError:
            # If the game has not started, the last item is the start time. Eg 18:00.
            if ":" in rev_info_parts[0]:
                status = GameStaus.not_started
            else:
                status = GameStatus.finished

        game = {}
        game["status"] = status
        game["number"] = i + 1
        if status == GameStatus.live:
            home_team, away_team = get_team(rev_info_parts[5:-1])
            game["goals_home"] = rev_info_parts[2]
            game["goals_away"] = rev_info_parts[0]
            game["time"] = rev_info_parts[4]
        elif status == GameStatus.not_started:
            home_team, away_team = get_teams(info_parts[2:-1])
            game["start_time"] = rev_info_parts[1] + " " + rev_info_parts[0]
        elif status == GameStatus.finished:
            home_team, away_team = get_teams(info_parts[5:])
            game["goals_home"] = info_parts[1]
            game["goals_away"] = info_parts[3]

        game["home_team"] = home_team
        game["away_team"] = away_team

        games.append(game)
    return games


def get_game_information() -> list(dict):
    """Entry point for this module.
    Fetch raw data and return a user friendly dict represenation of each one of the 13 games.

    Returns
    ______

    list(dict)
        List containing all 13 games represented as dict
        Returns
        ______

        list(dict)
            List containing all 13 games represented as dicts..
    """
    soup = fetch_raw_data()
    return extract_game_info(soup)

import re

from bs4 import BeautifulSoup
from pprint import pprint
from requests_html import HTMLSession

URL = "https://spela.svenskaspel.se/resultat/stryktipset"

session = HTMLSession()
r = session.get(URL)
r.html.render()
soup = BeautifulSoup(r.html.raw_html, "html.parser")

game_divs = soup.find_all("div", {"class": "js-expandable-box"})

games = []

# TODO: Handle case when games are done.
for i, div in enumerate(game_divs):
    raw_info = div.get_text().replace("\n", " ").replace("\r", "")
    info_parts = raw_info.split()
    try:
        # All interesting rows starts with a number between 1 and 13.
        int(info_parts[0])
    except ValueError:
        break

    started = False
    rev_info_parts = list(reversed(info_parts))
    try:
        # If the game has started, the last item is the score of the away team
        # If the game has not started, the last item is the start time. Eg 18:00.
        int(rev_info_parts[0])
        started = True
    except ValueError:
        pass

    game = {}
    game["started"] = started
    game["number"] = i + 1
    if started:
        goals_away = rev_info_parts[0]
        goals_home = rev_info_parts[2]
        time = rev_info_parts[4]
        team_names = list(reversed(rev_info_parts[5:-1]))
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
        game["goals_home"] = goals_home
        game["goals_away"] = goals_away
        game["time"] = time
        game["home_team"] = home_team
        game["away_team"] = away_team
    else:
        start_time = rev_info_parts[1] + " " + rev_info_parts[0]
        team_names = list(reversed(rev_info_parts[2:-1]))
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
        game["start_time"] = start_time
    game["home_team"] = home_team
    game["away_team"] = away_team

    games.append(game)

for game in games:
    pprint(game)

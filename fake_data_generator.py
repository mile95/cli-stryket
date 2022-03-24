from __future__ import annotations
from random import randrange

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

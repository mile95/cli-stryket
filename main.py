import json
from datetime import datetime

with open("data.json") as json_file:
    data = json.load(json_file)

games = data["draws"][0]["drawEvents"]


print(data["draws"][0]["drawComment"])
print("")
for i, game in enumerate(games):
    desc = game["eventDescription"]
    start = ":".join(game["match"]["matchStart"].split("T")[1].split(":")[:2])
    print(f"{i + 1}. {desc}".ljust(25) + f":: {start}")

import json
from battle_data import battle_data

def save():
    with open("battle.json", "w") as f:
        json.dump(battle_data, f)

def load():
    try:
        with open("battle.json") as f:
            battle_data.update(json.load(f))
    except:
        pass
import os
import json

def search(champ):
    with open("champions.json", "r") as f:
        dict = json.load(f)
        for name in dict[champ[0].upper()]:
            if champ.upper() in name.upper():
                return name
    return "0"

print (search("aat"))

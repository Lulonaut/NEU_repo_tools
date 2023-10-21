#!/usr/bin/python3
import requests
import json


r = requests.get("https://api.hypixel.net/resources/skyblock/items")
items = r.json()["items"]

with open("NotEnoughUpdates-REPO/constants/essencecosts.json", "r+") as file:
    essencecosts = json.loads(file.read())

    for item in items:
        if item["id"] in essencecosts:
            if "catacombs_requirements" in item:
                essencecosts[item["id"]]["catacombs_requirements"] = item[
                    "catacombs_requirements"
                ]
            if "requirements" in item:
                    essencecosts[item["id"]]["requirements"] = item["requirements"]    

    file.seek(0)
    file.truncate()
    file.write(json.dumps(essencecosts, indent=2, ensure_ascii=False))
    file.close()

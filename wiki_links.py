import sys
import os
import json
import urllib3
from time import sleep
import string

repo = "repo" if len(sys.argv) == 1 else sys.argv[1]

check_fandom_input = input("check fandom wiki? [y/n]: ")
check_fandom = True if check_fandom_input == "y" else False

check_official_wiki_input = input("check Hypixel wiki? [y/n]: ")
check_official_wiki = True if check_official_wiki_input == "y" else False

if not check_fandom and not check_official_wiki:
    print("Nothing to check")
    exit(0)

http = urllib3.PoolManager()

for file in os.listdir(os.fsencode(os.path.join(repo, "items"))):
    with open(os.path.join(repo, "items", os.fsdecode(file)), "r+") as file:
        json_data = json.loads(file.read().encode("utf-8"))

        if "vanilla" in json_data or json_data["itemid"] == "minecraft:enchanted_book" or json_data["itemid"] == "minecraft:potion":
            file.close()
            continue


        name = ""
        whatever = False
        for i in json_data["displayname"]:
            if not whatever and i != "§":
                name += i

            whatever = True if i == "§" else False

        if "[Lvl {LVL}] " in name:
            name = name.replace("[Lvl {LVL}] ", "") + " Pet"

        name = name.strip()
        name_list = list(name)
        for i in range(0, len(name_list)):
            if name_list[i] == " ":
                name_list[i] = "_"
                name_list[i + 1] = name_list[i + 1].upper()
        name = "".join(name_list)
        name = name.replace("'", "%27")

        skipped = False
        changed = False
        if check_fandom:
            url = "https://hypixel-skyblock.fandom.com/wiki/" + name
            if "info" in json_data:
                for item in json_data["info"]:
                    if "hypixel-skyblock.fandom.com" in item:
                        print(f"{name}: Fandom: Skipped")
                        skipped = True
            if not skipped:
                r = http.request("GET", url)
                if r.status == 200:
                    if not "infoType" in json_data or json_data["infoType"] == "":
                        json_data["infoType"] = "WIKI_URL"

                    if not "info" in json_data:
                        json_data["info"] = []

                    json_data["info"].append(url)
                    changed = True
                    print(f"{name}: Fandom: added")
                else:
                    print(f"{name}: Fandom: not found")

        if check_official_wiki:
            url = "https://wiki.hypixel.net/" + name
            if "info" in json_data:
                for item in json_data["info"]:
                    if "wiki.hypixel.net" in item:
                        print(f"{name}: Hypixel: Skipped")
                        skipped = True
            if not skipped:
                r = http.request("GET", url)
                if r.status == 200:
                    if not "infoType" in json_data or json_data["infoType"] == "":
                        json_data["infoType"] = "WIKI_URL"

                    if not "info" in json_data:
                        json_data["info"] = []

                    json_data["info"].append(url)
                    changed = True
                    print(f"{name}: Hypixel: added")
                else:
                    print(f"{name}: Hypixel: not found")

        if changed:
            file.seek(0)
            file.truncate()
            file.write(
                json.dumps(json_data, indent=2, ensure_ascii=False).replace(
                    "=", "\\u003d"
                ).replace("'", "\\u0027")
            )
        file.close()
        if not skipped:
            sleep(1)

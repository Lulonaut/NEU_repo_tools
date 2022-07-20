import json
import sys


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [path to MAXED_ENCHANT_BOOK.json]")
    exit(1)

path = sys.argv[1]
print(path)

#path = "NotEnoughUpdates-REPO/items/MAXED_ENCHANT_BOOK.json"
with open(path, mode="r+", encoding="utf-8") as file:
    json_data: dict = json.loads(file.read())

    nbttag: str = json_data["nbttag"]
    lore: list[str] = json_data["lore"]
    old_enchantments_start = nbttag.find("enchantments:{")
    old_enchantments_end = nbttag.find("}", old_enchantments_start)
    new_enchantments_string = ""

    # make the enchantments array empty
    nbttag = nbttag.replace(
        nbttag[old_enchantments_start + 14 : old_enchantments_end], ""
    )
    new_enchantments_start = old_enchantments_start + 14

    for entry in lore:
        for enchant in entry.split(","):
            if not enchant.strip().startswith("§9"):
                continue
            print(enchant)
            ultimate_enchant = True if "§9§d§l" in enchant else False

            enchant_clean = ""
            last_char_section_sign = False
            for char in enchant.strip():
                if char == "§":
                    last_char_section_sign = True
                else:
                    if not last_char_section_sign:
                        enchant_clean += char
                    last_char_section_sign = False
            level_str = enchant_clean.split(" ")[len(enchant_clean.split(" ")) - 1]

            roman_numerals = {"I": 1, "V": 5, "X": 10}
            level = 0
            for i, j in enumerate(level_str):
                if (i + 1) == len(level_str) or roman_numerals[j] >= roman_numerals[
                    level_str[i + 1]
                ]:
                    level += roman_numerals[j]
                else:
                    level -= roman_numerals[j]

            # remove roman numerals at the end
            enchant_clean = enchant_clean.rsplit(" ", 1)[0]
            enchant_clean = enchant_clean.replace("-", "_").replace(" ", "_").lower()
            if ultimate_enchant:
                enchant_clean = "ultimate_" + enchant_clean

            new_enchantments_string += f"{enchant_clean}:{level},"
    nbttag = (
        nbttag[:new_enchantments_start]
        + new_enchantments_string[:-1]
        + nbttag[new_enchantments_start:]
    )
    json_data["nbttag"] = nbttag
    print("writing")
    file.seek(0)
    file.truncate()
    file.write(
        json.dumps(json_data, indent=2, ensure_ascii=False)
        .replace("=", "\\u003d")
        .replace("'", "\\u0027")
    )

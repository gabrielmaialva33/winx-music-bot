import os
import sys
from typing import List

import yaml

languages = {}
commands = {}

languages_present = {}


def get_command(value: str) -> List:
    return commands["command"][value]


def command(cmd: str):
    cmds = " ".join([f"/{c}" for c in get_command(cmd)])
    return cmds


def get_string(lang: str):
    return languages[lang]


for filename in os.listdir(r"./strings"):
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        commands[language_name] = yaml.safe_load(
            open(r"./strings/" + filename, encoding="utf8")
        )

for filename in os.listdir(r"./strings/langs/"):
    if "pt_br" not in languages:
        languages["pt_br"] = yaml.safe_load(
            open(r"./strings/langs/pt.yml", encoding="utf8")
        )
        languages_present["pt_br"] = languages["pt_br"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "pt_br":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        for item in languages["pt_br"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["pt_br"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except:
        print(
            "There is some issue with the language file inside bot. Please report it to the TheTeamvk at @TheTeamvk on Telegram"
        )
        sys.exit()

import pandas as pd

df = pd.read_csv("crawler/playerid.csv")
ALL_NAMES = df["name"].tolist()

def find_name_in_text(text: str):
    found = ""
    for name in ALL_NAMES:
        if name in text:
            found = name
    return found

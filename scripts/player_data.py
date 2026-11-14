import pandas as pd
import json
import os
import requests
import numpy as np
import re

# Column names sourced from Tennis Abstract's
# Serena Williams player page HTML source code (var matchhead).
# https://www.tennisabstract.com/cgi-bin/wplayer-classic.cgi?p=SerenaWilliams
matchhead = ["date","tourn","surf","level","wl","rank","seed","entry","round", 
             "score","max","opp","orank","oseed","oentry","ohand","obday",
             "oht","ocountry","oactive","time","aces","dfs","pts","firsts","fwon",
             "swon","games","saved","chances","oaces","odfs","opts","ofirsts",
             "ofwon","oswon","ogames","osaved","ochances","obackhand","chartlink",
             "pslink","whserver","matchid"]

# exctracting js data and create dataframe
def extract_player_data(text):
    s = text[text.find("["):text.rfind("]")+1]
    player_data = json.loads(s)
    # Both male and female share first 17 columns
    player_df = pd.DataFrame(
        [row[:17] for row in player_data],
        columns=matchhead[:17]
    )
    player_df = player_df.replace("", np.nan)
    return player_df

# calculates opponents age, male and female cases
def calculate_opp_age(player_fig_df):
    bday = str(player_fig_df["obday"].dropna().head(1).item())
    #female case
    if len(bday) == 8 and bday.isdigit():
        player_fig_df["obday"] = pd.to_datetime(
            player_fig_df["obday"], format="%Y%m%d", errors="coerce"
        )
        player_fig_df["opp_age"] = (player_fig_df["date"] - player_fig_df["obday"]).dt.days / 365
    #male case
    else:
        player_fig_df["opp_age"] = pd.to_numeric(player_fig_df["obday"], errors="coerce")

    return player_fig_df

# process dataframe for plotting around birthday
def career_data(text, bday):
    # raw dataframe
    player_df = extract_player_data(text)

    # extracting necessary columns
    player_fig_df = player_df[['date', 'tourn', 'wl', 'opp', 'obday']].copy()

    
    # converting dates
    player_fig_df["date"] = pd.to_datetime(player_fig_df["date"], format="%Y%m%d")

    # calculating player's age
    player_fig_df["age"] = (player_fig_df["date"] - pd.Timestamp(bday)).dt.days / 365

    # calculating opponent's age
    player_fig_df = calculate_opp_age(player_fig_df)

    # calculating age difference
    player_fig_df['age_difference'] = player_fig_df['age'] - player_fig_df['opp_age']

    return player_fig_df

def get_player_career(player):
    #checking for valid input                
    if not player.strip():
        raise ValueError("Please enter a player name.")
    # format player name
    if " " in player:
        player_name = "".join(word.capitalize() for word in player.split())
    else:
        player_name = player[0].upper() + player[1:]
    # download career data
    url = f"https://www.tennisabstract.com/jsmatches/{player_name}Career.js"

    print("Downloading career data...")
    r = requests.get(url, timeout=10)
    print("Career data downloaded")
    #checking if input player exists in site
    if r.status_code == 404:
        raise ValueError(f"Player '{player}' not found.")
    r.raise_for_status()

    # find player's birthday
    # different urls for male and female players
    for page in ["wplayer-classic.cgi", "player-classic.cgi"]:
        profile_url = f"https://www.tennisabstract.com/cgi-bin/{page}?p={player_name}"
        # try block to prevent excessive runtime due to site
        try:
            profile = requests.get(profile_url, timeout=10).text
        except requests.exceptions.Timeout:
            continue
        #finding birthday in site
        if "var dob = " in profile:
            bday = profile.split("var dob = ")[1].split(";")[0]
            return career_data(r.text, pd.to_datetime(bday, format="%Y%m%d"))

    raise ValueError(f"Birthday not found for '{player}'.")
    


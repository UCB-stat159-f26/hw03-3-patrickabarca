import pandas as pd
import json
import os
import requests
import numpy as np

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

# process dataframe for plotting
def career_data(text, birthday):
    # raw dataframe
    player_df = extract_player_data(text)

    # extracting necessary columns
    player_fig_df = player_df[['date', 'tourn', 'wl', 'opp', 'obday']].copy()

    
    # converting dates
    player_fig_df["date"] = pd.to_datetime(player_fig_df["date"], format="%Y%m%d")

    # calculating player's age
    player_fig_df["age"] = (player_fig_df["date"] - pd.Timestamp(birthday)).dt.days / 365

    # calculating opponent's age
    player_fig_df = calculate_opp_age(player_fig_df)

    # calculating age difference
    player_fig_df['age_difference'] = player_fig_df['age'] - player_fig_df['opp_age']

    return player_fig_df


import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sqlite3
import wikipedia as wp
import urllib.parse

""" 
    Starting with Men's 2023 tournament teams
    Will gather that data using requests and bs4

url = "https://www.sbnation.com/college-basketball/2023/3/12/23636762/2023-ncaa-tournament-full-rankings-alabama-houston-kansas-purdue"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')

teams = soup.find('p', {'id':'wc1TA4'}).text
teams_array = teams.split('. ')
"""

"""
Women's tournament teams will be scraped with the wikipedia pandas extension
"""
import wikipedia

html = wp.page("2023 NCAA Division I women's basketball tournament").html().encode("UTF-8")

teams_array = []
df = pd.read_html(html)[5]
teams_array.append(df[1][2:].values)

kaggle_womens_ids = pd.read_csv('./WTeams.csv')

womens_teams_clean = {}
womens_teams_missing = []
for team in teams_array[0]:
    try:
        #print(kaggle_womens_ids.query(f"TeamName=={clean_team_name}")["TeamID"])

        temp_team_id = kaggle_womens_ids[kaggle_womens_ids["TeamName"].str.match(team)]
        print(temp_team_id.iloc[0]["TeamID"])
        womens_teams_clean[temp_team_id.iloc[0]["TeamID"]] = team
    except:
        womens_teams_missing.append(team)
        #print(clean_team_name)

print(womens_teams_missing)
for team in womens_teams_missing:
    print(team)
    team_id = input("What is this team's ID?")
    womens_teams_clean[team_id] = team

final_teams_ids = pd.DataFrame(womens_teams_clean.items(), columns=['TeamID', 'TeamName'])

final_teams_ids.to_csv('./2023WteamIDs.csv', index=False)
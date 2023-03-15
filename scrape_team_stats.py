import requests
from bs4 import BeautifulSoup
import sqlite3
import numpy as np
import pandas as pd

column_titles = ["year", "school", "games", "wins", "losses", "wlper", "srs", "sos", 'div1', "conf_w", "conf_l", "div2", "home_w", "home_l", "div3", "away_w", "away_l", "div4", "tm_points", "opp_points", "div5", "mp", "fg", "fga", "fgper", "threes_made", "threes_att", "threeper", "fts", "fta", "ftper", "orb", "trb", "ast", "stl", "blk", "tov", "pf"]

team_stats_df = pd.DataFrame(columns=column_titles)

connection = sqlite3.connect("ncaa.db")
cursor = connection.cursor()

#cursor.execute("CREATE TABLE IF NOT EXISTS mensteamstats (year INT, school TEXT, games INT, wins INT, losses INT, wlper FLOAT, srs FLOAT, sos FLOAT, conf_w INT, conf_l INT, home_w INT, home_l INT, away_w INT, away_l INT, tm_points INT, opp_points INT, mp, fg INT, fga INT, fgper FLOAT, threes_made INT, threes_att INT, threeper FLOAT, fts INT, fta INT, ftper FLOAT, orb INT, trb INT, ast INT, stl INT, blk INT, tov INT, pf INT)")

#insert_array = "INSERT INTO mensteamstats (year, school, games, wins, losses, wlper, srs, sos, conf_w, conf_l, home_w, home_l, away_w, away_l, tm_points, opp_points, mp, fg, fga, fgper, threes_made, threes_att, threeper, fts, fta, ftper, orb, trb, ast, stl, blk, tov, pf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format()

def gather_data(year, df):
    print(f"working on year {year}")
    url = f"https://www.sports-reference.com/cbb/seasons/women/{year}-school-stats.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_team_table = soup.find('table', id="basic_school_stats")

    for row in all_team_table.tbody.find_all('tr'):
        temp_stats_array = [year]
        columns = row.find_all('td')
        try:
            for td in columns:
                if td.text == columns[0].text:
                    temp_stats_array.append(td.text)
                else:
                    temp_stats_array.append(td.text)
        except:
            continue

        if (len(temp_stats_array) == len(column_titles)):
            df.loc[len(df)] = temp_stats_array
        else:
            print(len(temp_stats_array), len(column_titles))
            continue
        
    print(f"finished with year {year}")
    return df

years = np.arange(2010, 2024)

for year in years:
    team_stats_df = gather_data(year, team_stats_df)

print(team_stats_df)
conn = sqlite3.connect('./ncaa.db')

team_stats_df.to_sql("womensteamstats", conn, if_exists="replace")
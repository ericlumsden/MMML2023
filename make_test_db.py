"""
Will be creating test and training data from all previous tourney matchups, combining each team's year stats
For men will start at 2008 (first year 3PAs > 600)
Women will take entire dataset (2010+)
"""
import pandas as pd
import sqlite3
import numpy as np


columns_to_select = ["wlper", "srs", "sos", "conf_w", "conf_l", "home_w", "home_l", "away_w", "away_l", "tm_points", "opp_points", "fg", "fga", "fgper", "threes_made", "threes_att", "threeper", "fts", "fta", "ftper", "orb", "trb", "ast", "stl", "blk", "tov", "pf"]

column_titles = ["wlper_1", "srs_1", "sos_1", "conf_w_1", "conf_l_1", "home_w_1", "home_l_1", "away_w_1", "away_l_1", "tm_points_1", "opp_points_1", "fg_1", "fga_1", "fgper_1", "threes_made_1", "threes_att_1", "threeper_1", "fts_1", "fta_1", "ftper_1", "orb_1", "trb_1", "ast_1", "stl_1", "blk_1", "tov_1", "pf_1"]
column_titles_new = []

for x in column_titles:
    column_titles_new.append(x.replace('_1', '_2'))

column_titles += column_titles_new
column_titles.append('winner')

# Mens
conn = sqlite3.connect('./ncaa.db')
df_tourney_m = pd.read_sql("SELECT year, team_1, team_2, winner FROM menstourney WHERE year > 2007", conn)
df_stats_m = pd.read_sql("SELECT * FROM mensteamstats WHERE year > 2007", conn)

mens_training_db = pd.DataFrame(columns=column_titles)

caught_bad_names = set()
name_corrections = {
    'UNC': 'North Carolina',
    'Ole Miss': 'Mississippi',
    'USC': 'Southern California',
    'UMass': 'Massachusetts',
    'SMU': 'Southern Methodist',
    "St. Joseph's": "Saint Joseph's",
    "LSU": "Louisiana State",
    "UCSB": "UC Santa Barbara",
    "UConn": "Connecticut",
    "UC-Irvine": "UC Irvine",
    "UCF": "Central Florida",
    "St. Peter's": "Saint Peter's",
    "BYU": "Brigham Young",
    "UNLV": "Nevada-Las Vegas",
    "VCU": "Virginia Commonwealth",
    "UMBC": "Maryland-Baltimore County"}

years = list(range(2008,2020)) + list(range(2021,2023))

for year in years:
    temp_tourney_yr = df_tourney_m[df_tourney_m.year == year]
    temp_stats_yr = df_stats_m[df_stats_m.year == year]

    for index, row in temp_tourney_yr.iterrows():
        team_1, team_2 = row['team_1'], row['team_2']

        if team_1 in name_corrections.keys():
            team_1 = name_corrections[team_1]
        if team_2 in name_corrections.keys():
            team_2 = name_corrections[team_2]

        winner_int = row['winner']

        team_1_stats = temp_stats_yr[temp_stats_yr['school'].str.contains(team_1)]
        team_2_stats = temp_stats_yr[temp_stats_yr['school'].str.contains(team_2)]

        if len(team_1_stats) == 0:
            caught_bad_names.add(team_1)
        if len(team_2_stats) == 0:
            caught_bad_names.add(team_2)

        if (len(team_1_stats) != 1) or (len(team_2_stats) != 1):
            continue
        else:
            temp_stats_array = []
            for team in [team_1_stats, team_2_stats]:
                print(temp_stats_array)
                temp_stats_array.append(team.iloc[0]['wlper'])
                temp_stats_array.append(team.iloc[0]['srs'])
                temp_stats_array.append(team.iloc[0]['sos'])
                temp_stats_array.append(team.iloc[0]['conf_w'])
                temp_stats_array.append(team.iloc[0]['conf_l'])
                temp_stats_array.append(team.iloc[0]['home_w'])
                temp_stats_array.append(team.iloc[0]['home_l'])
                temp_stats_array.append(team.iloc[0]['away_w'])
                temp_stats_array.append(team.iloc[0]['away_l'])
                temp_stats_array.append(team.iloc[0]['tm_points'])
                temp_stats_array.append(team.iloc[0]['opp_points'])
                temp_stats_array.append(team.iloc[0]['fg'])
                temp_stats_array.append(team.iloc[0]['fga'])
                temp_stats_array.append(team.iloc[0]['fgper'])
                temp_stats_array.append(team.iloc[0]['threes_made'])
                temp_stats_array.append(team.iloc[0]['threes_att'])
                temp_stats_array.append(team.iloc[0]['threeper'])
                temp_stats_array.append(team.iloc[0]['fts'])
                temp_stats_array.append(team.iloc[0]['fta'])
                temp_stats_array.append(team.iloc[0]['ftper'])
                temp_stats_array.append(team.iloc[0]['orb'])
                temp_stats_array.append(team.iloc[0]['trb'])
                temp_stats_array.append(team.iloc[0]['ast'])
                temp_stats_array.append(team.iloc[0]['stl'])
                temp_stats_array.append(team.iloc[0]['blk'])
                temp_stats_array.append(team.iloc[0]['tov'])
                temp_stats_array.append(team.iloc[0]['pf'])

            temp_stats_array.append(winner_int)
            mens_training_db.loc[len(mens_training_db)] = temp_stats_array

mens_training_db.to_sql("menstraining", conn, if_exists='replace')

print("Caught bad names:")
print(caught_bad_names)
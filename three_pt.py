import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect("./ncaa.db")
df = pd.read_sql("SELECT year, threes_att FROM mensteamstats", conn)
df2 = pd.read_sql("SELECT year, threes_att FROM womensteamstats", conn)

df['threes_att'].replace('', np.nan, inplace=True)
df.dropna(subset=['threes_att'], inplace=True)
df = df.astype(float)
year_mean = df.groupby('year').mean()

plt.figure(0)
plt.scatter(df.year, df.threes_att, color='blue', alpha=0.5)
plt.plot(np.arange(1993,2024), year_mean, color='red', label='yearly avg')
plt.legend()
plt.title('3PAs over time [M]')
plt.xlabel('year')
plt.ylabel('Total 3PAs for all teams')
plt.savefig('./mens3PAs_yr.png')

df2['threes_att'].replace('', np.nan, inplace=True)
df2.dropna(subset=['threes_att'], inplace=True)
df2 = df2.astype(float)
year_mean_w = df2.groupby('year').mean()

plt.figure(1)
plt.scatter(df2.year, df2.threes_att, color='blue', alpha=0.5)
plt.plot(np.arange(2010,2024), year_mean_w, color='red', label='yearly avg')
plt.legend()
plt.title('3PAs over time [W]')
plt.xlabel('year')
plt.ylabel('Total 3PAs for all teams')
plt.savefig('./womens3PAs_yr.png')

plt.show()
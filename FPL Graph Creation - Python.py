#!/usr/bin/env python
# coding: utf-8

# # FPL Graph Creation Notebook

# ## Notebook to create the graphs to show how different members of leagues/friend groups have progressed throughout the season

# In[5]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load Data
DF = pd.read_csv('FPL_weekly_tracker.csv')

# Weekly Points Line Graph
gameweeks = DF.columns[3:]
team_names = DF['Owner Name'].unique()

colors = plt.cm.tab20.colors

plt.figure(figsize=(12, 6))  # Increase the figure width to accommodate legends

for i, team_name in enumerate(team_names):
    team_data = DF[DF['Owner Name'] == team_name]
    points = [team_data[f'Gameweek {i}'].iloc[0] for i in range(1, len(gameweeks) + 1)]
    plt.plot(range(1, len(gameweeks) + 1), points, label=team_name, color=colors[i])

average_points = DF[gameweeks].mean()
plt.plot(range(1, len(gameweeks) + 1), average_points, linestyle='--', color='black', label='Average')

plt.xlabel('Gameweek', fontweight='bold')
plt.ylabel('Points', fontweight='bold')
plt.title('Points Gained per Gameweek', fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Adjust legend position
plt.grid(True)
plt.savefig('Points Gained per Gameweek.jpg', bbox_inches='tight')  # Ensure the legend is included in the saved image
plt.close()

# Total Points Talley Line Graph
plt.figure(figsize=(12, 6))  # Increase the figure width to accommodate legends

for i, team_name in enumerate(team_names):
    team_data = DF[DF['Owner Name'] == team_name]
    cumulative_points = team_data[gameweeks].cumsum(axis=1)
    plt.plot(range(1, len(gameweeks) + 1), cumulative_points.iloc[0], marker='x', label=team_name, color=colors[i])

plt.xlabel('Gameweek', fontweight='bold')
plt.ylabel('Cumulative Points', fontweight='bold')
plt.title('Cumulative Points Accrued per Gameweek', fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Adjust legend position
plt.grid(True)
plt.savefig('Cumulative Points Accrued per Gameweek.jpg', bbox_inches='tight')  # Ensure the legend is included in the saved image
plt.close()

# Proportion of weeks in the lead
gameweeks = DF.columns[3:]
player_names = DF['Owner Name'].unique()

cumulative_totals_df = pd.DataFrame(columns=player_names, index=gameweeks)

for gw in gameweeks:
    for player_name in player_names:
        player_data = DF[DF['Owner Name'] == player_name]
        cumulative_points = player_data[gameweeks[:gameweeks.get_loc(gw) + 1]].sum(axis=1)
        cumulative_totals_df.at[gw, player_name] = cumulative_points.iloc[0]

cumulative_totals_df = cumulative_totals_df.apply(pd.to_numeric)

cumulative_totals_df['Highest Scorer'] = cumulative_totals_df.idxmax(axis=1)

winner_counts = cumulative_totals_df['Highest Scorer'].value_counts()

plt.figure(figsize=(10, 8))
plt.pie(winner_counts, labels=winner_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Proportion of Game Weeks Led by Each Person', fontweight='bold')
plt.savefig('Proportion of Weeks Led by Each Individual.jpg')
plt.close()

# Weekly distance to the leader
DF2 = DF.copy()

for column in DF2.columns[3:]:
    DF2[column] = pd.to_numeric(DF2[column], errors='coerce')

gameweeks = DF2.columns[3:]
player_names = DF2['Owner Name'].unique()

cumulative_totals_df2 = pd.DataFrame(columns=player_names, index=gameweeks)

for gw in gameweeks:
    for player_name in player_names:
        player_data = DF2[DF2['Owner Name'] == player_name]
        cumulative_points = player_data[gameweeks[:gameweeks.get_loc(gw) + 1]].sum(axis=1)
        cumulative_totals_df2.at[gw, player_name] = cumulative_points.iloc[0]

cumulative_totals_df2 = cumulative_totals_df2.apply(pd.to_numeric)
cumulative_totals_df2['Highest Scorer'] = cumulative_totals_df2.idxmax(axis=1)

for gw in gameweeks:
    highest_scorer = cumulative_totals_df2.loc[gw, 'Highest Scorer']
    
    for player_name in player_names:
        leader_points = cumulative_totals_df2.loc[gw, highest_scorer]
        player_points = cumulative_totals_df2.loc[gw, player_name]
        difference = leader_points - player_points
        cumulative_totals_df2.at[gw, f"{player_name}_Difference"] = difference

num_teams = len(player_names)
colors = plt.cm.tab20.colors
teams_to_plot = cumulative_totals_df2.columns[-num_teams:]

plt.figure(figsize=(12, 6))
for i, team in enumerate(teams_to_plot):
    color = colors[i % len(colors)]
    plt.plot(cumulative_totals_df2.index, cumulative_totals_df2[team], label=team, color=color)

plt.xlabel('Gameweeks')
plt.ylabel('Points')
plt.title('Points of Teams Across Gameweeks')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

plt.savefig('Weekly Points Behind Leader.jpg')
plt.close()





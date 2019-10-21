#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:17:32 2019

@author: marco
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    
    
    print("Loading datasets...")
    events = pd.read_json('./dataset/events/events_England.json')
    matches = pd.read_json('./dataset/matches/matches_England.json')
    teams = pd.read_json('./dataset/teams.json')
    players = pd.read_json('./dataset/players.json')
    print("Datasets loaded.")
    
    cols = ['playerId', 'matchPeriod','matchId','teamId', 'eventSec', 'eventInterval']
    
    goals_df = pd.DataFrame(columns=cols)
    
    for i in range(len(events)):
        tags = [t['id'] for t in events['tags'][i]]
        
        if 101 in tags or 102 in tags:
            player_id = events['playerId'][i]
            match_period = events['matchPeriod'][i]
            match_id = events['matchId'][i]
            team_id = events['teamId'][i]
            event_sec = events['eventSec'][i]
            
            row = [{'playerId':player_id,
                    'matchPeriod':match_period,
                    'matchId':match_id,
                    'teamId':team_id,
                    'eventSec':event_sec,
                    'eventInterval': 0}]
            
            new_df_row = pd.DataFrame(row, index=[i])
            #print(row)
            goals_df = goals_df.append(new_df_row, ignore_index=True)
            
    goals_df.reindex()
    
    for i in range(len(goals_df)):
        seconds = goals_df['eventSec'][i]
        period = goals_df['matchPeriod'][i]
        
        minutes = seconds // 60.0
        
        if period == '1H':
            if minutes < 45:
                interval = minutes // 9 # 1H with no extra time
            else:
                interval = 5 # Extra time of the 1H
        elif period == '2H':
            if minutes < 45:
                interval = 6 + ( minutes // 9) # 2H with no extra time
            else:
                interval = 11 # Extra time of the 2H
        
        goals_df.at[i, 'eventInterval'] = interval
        
    fr_interval = np.zeros(12) # Frequencies interval
    for index_interval in range (0, 12):
        for i in range(len(goals_df)):       
            if goals_df['eventInterval'][i] == index_interval:
                fr_interval[index_interval] += 1
    
    
    # Plotting the goal frequencies for each interval
    x = np.arange(12)
    plt.bar(x, fr_interval)
    plt.show()
                
        
# For each team, find the 10 that scored the most in the 81-90 min range 
# which is interval number 11 (index 10).
    
    team_scores_81_90 = {}
    
    for i in range(len(goals_df)):
        team_id = goals_df['teamId'][i]
        
        if team_id not in team_scores_81_90.keys():
            team_scores_81_90[team_id] = 0
        
        # If the scored goal happened in 
        interval = goals_df['eventInterval'][i]
        if interval == 10:
            team_scores_81_90[team_id] += 1

    
    # Make a DataFrame so we can easily merge with the teams dataset
    team_scores_81_90 = pd.DataFrame(list(team_scores_81_90.items()), columns=['wyId', 'Scores8190'])
    team_scores_81_90 = team_scores_81_90.merge(teams, on='wyId', how='inner')
    team_scores_81_90 = team_scores_81_90.sort_values(by='Scores8190', ascending=False)
    team_scores_81_90 = team_scores_81_90.reset_index(drop=True)
    
    for i in range(10):
        team_name = team_scores_81_90['officialName'][i]
        team_goals_81_90 = team_scores_81_90['Scores8190'][i]
        
        print('(%d°) - %s has scored %d goals in the [81-90) minutes range.' %  (i+1, team_name, team_goals_81_90))
    
# CRQ1 - III
    print()

    players_eight_intervals = {}
    
    # Build list
    for i in range(len(goals_df)):
        player_id = goals_df['playerId'][i]
        goal_interval = int(goals_df['eventInterval'][i])
        
        if player_id not in players_eight_intervals.keys():
            players_eight_intervals[player_id] = np.zeros(12)
        
        players_eight_intervals[player_id][goal_interval] = 1
        
    for key in players_eight_intervals.keys():
        
        num_goals_in_intervals = sum(players_eight_intervals[key])
        
        if num_goals_in_intervals >= 8:
            player_name = players.loc[players['wyId'] == key, 'shortName'].iloc[0]
            
            # Disable this in case it was not requested.
            print('\t%s has scored goals in %d different intervals.' % (player_name, num_goals_in_intervals))
    
    print()

    if len(players_eight_intervals.keys()) > 0:
        print('So there are players that scored goals in at least 8 different intervals.')
    else:
        print('Unfortunately there were not any players that scored goals in 8 different intervals.')
        
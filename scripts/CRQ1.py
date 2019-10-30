#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:17:32 2019

@author: marco
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

''' In this exercise, the main goal is to analyze different matches by 
    dividing each match in different time intervals of 9 minutes each. 
    
    I.   Make a barplot with the absolute frequency of goals in all the time slots.
    II.  Find the top 10 teams that score the most in the interval "81-90".
    III. Show if there are players that were able to score at least one goal in 8 different intervals.

    The first time interval will be the one [0-9), so [0-8]. 
    We are supposing that when each half time ends, it's at the 45 and 90 minute
    mark. So when, for example, a goal is scored at the 45th minute, it's score
    in the extra time given (45+). 
'''

if __name__ == '__main__':
    
    print("Loading datasets...")
    events = pd.read_json('./dataset/events/events_England.json')
    matches = pd.read_json('./dataset/matches/matches_England.json')
    teams = pd.read_json('./dataset/teams.json')
    players = pd.read_json('./dataset/players.json')
    print("Datasets loaded.")
    
    # Here we are preparing to make a new dataframe that will contain only useful information
    # for doing this exercise
    cols = ['playerId', 'matchPeriod','matchId','teamId', 'eventSec', 'eventInterval']
    goals_df = pd.DataFrame(columns=cols)
    
    for i in range(len(events)):
        tags = [t['id'] for t in events['tags'][i]]
        
        # A goal(101) or an autogoal(102) might be scored. Either way, it's a goal.
        if 101 in tags or 102 in tags:
            player_id = events['playerId'][i]
            match_period = events['matchPeriod'][i]
            match_id = events['matchId'][i]
            team_id = events['teamId'][i]
            event_sec = events['eventSec'][i] # This for now is just a raw string containing the seconds in which the event happened
            
            row = [{'playerId':player_id,
                    'matchPeriod':match_period,
                    'matchId':match_id,
                    'teamId':team_id,
                    'eventSec':event_sec,
                    'eventInterval': -1}] # The interval # can be for now set to a default value (-1) which is meaningless (easier debugging).
    
            # Here is the new row for the dataframe ready to be inserted
            new_df_row = pd.DataFrame(row, index=[len(goals_df)]) # Create
            goals_df = goals_df.append(new_df_row, ignore_index=False)
    
    # Using the new dataset (goals_df) we can start to put each event in its time interval
    for i in range(len(goals_df)):
        seconds = goals_df['eventSec'][i]
        period = goals_df['matchPeriod'][i]
        
        minutes = seconds // 60.0 # From seconds to minutes using an integer resulting division
        
        if period == '1H':
            if minutes < 45: # If it happened before the beginning of the 45th minute, it's not extra time.
                interval = minutes // 9 # 1H with no extra time, dividing by nine will give the interval index (IMPORTANT!)
            else:
                interval = 5 # Extra time of the 1H, it's going to be assigned to an arbitrary slot
        elif period == '2H':
            if minutes < 45:
                interval = 6 + ( minutes // 9) # 2H with no extra time
            else:
                interval = 11 # Extra time of the 2H
        
        goals_df.at[i, 'eventInterval'] = interval
    
    # Let's start preparing the absolute frequencies
    fr_interval = np.zeros(12) # Frequencies interval
    for i in range(len(goals_df)):       
        interval_index = int(goals_df['eventInterval'][i]) # Conversion necessary: fetching from dataset directly gives you a float
        fr_interval[interval_index] += 1 # We can access directly by index the frequency intervals array
    
    # Here we are preparing the label names for each interval
    x_labels = []
    for i in range(0, 11):
        label = ''
        start_minute = 9 * i
        end_minute = start_minute + 9
        
        if start_minute == 45 or start_minute == 90:
            x_labels.append(str('%d+' % start_minute))
        
        if start_minute != 90:
            x_labels.append(str('[%d-%d)' % (start_minute, end_minute)))
        
    
    # Plotting the goal frequencies for each interval
    plt.figure(figsize=(10,7))
    x = np.arange(12)
    plt.xticks(x, x_labels, rotation=45) # Each 'tick' is a time interval
    plt.bar(x, fr_interval) # Drawing the actual absolute frequencies
    plt.show()
    
    ''' CRQ1 - II 
    # For each team, find the 10 that scored the most in the 81-90 min range 
    # which is interval number 11 (index 10).
    '''
    print() # Just a new line
    # The team ids will be the keys
    team_scores_81_90 = {}
    
    for i in range(len(goals_df)):
        
        
        # First we analyze the goal interval, if it's not in the [81-90)
        # don't even bother fetching the teamId.
        interval = goals_df['eventInterval'][i]
        if interval == 10:
            team_id = goals_df['teamId'][i]
            # If the team is not in the dictionary, initialize it with the initial value of 0
            if team_id not in team_scores_81_90.keys():
                team_scores_81_90[team_id] = 0
            team_scores_81_90[team_id] += 1

    
    # Make a DataFrame so we can easily merge with the teams dataset
    team_scores_81_90 = pd.DataFrame(list(team_scores_81_90.items()), columns=['wyId', 'Scores8190'])
    team_scores_81_90 = team_scores_81_90.merge(teams, on='wyId', how='inner')
    # Sort the values by their scores
    team_scores_81_90 = team_scores_81_90.sort_values(by='Scores8190', ascending=False)
    # Reset the index now that the rows are sorted by score, printing will be correct (otherwise it will be like they're unordered)
    team_scores_81_90 = team_scores_81_90.reset_index(drop=True)
    
    # Print the rank of the ten teams that scored most goals in the [81-90) interval
    for i in range(10):
        team_name = team_scores_81_90['officialName'][i]
        team_goals_81_90 = team_scores_81_90['Scores8190'][i]
        
        print('(%d°) - %s has scored %d goals in the [81-90) minutes range.' %  (i+1, team_name, team_goals_81_90))
    
    ''' CRQ1 - III '''
    print()

    players_eight_intervals = {}
    
    # Build list of 'flags': one flag per interval will tell us if a players has scored at least once in the given interval
    for i in range(len(goals_df)):
        player_id = goals_df['playerId'][i]
        goal_interval = int(goals_df['eventInterval'][i])
        
        # If player not in dictionary keys, initialize the 'flag' array
        if player_id not in players_eight_intervals.keys():
            players_eight_intervals[player_id] = np.zeros(12)
        
        players_eight_intervals[player_id][goal_interval] = 1
        
    for key in players_eight_intervals.keys():
        # Since each flag is 1 or 0, a sum of the flag values is enough to tell us how many intervals 
        # the player has scored at least once in.
        num_goals_in_intervals = sum(players_eight_intervals[key])
        
        # So if it's greater or equal to 8, we bother fetching the player's name from the players dataset
        if num_goals_in_intervals >= 8:
            player_name = players.loc[players['wyId'] == key, 'shortName'].iloc[0]
            
            # Disable this in case it was not requested.
            # Here we are printing how many intervals the players has scored in.
            print('\t%s has scored goals in %d different intervals.' % (player_name, num_goals_in_intervals))
    
    print()

    # As requested by the exercise, here we are showing if there were any players that scored 
    # in at least 8 different intervals (the number of keys = the number of players that did it)
    if len(players_eight_intervals.keys()) > 0:
        print('There are players that scored goals in at least 8 different intervals.')
    else:
        print('Unfortunately there were not any players that scored goals in at least 8 different intervals.')
        
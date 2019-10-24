
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 19:15:29 2019

@author: marco
"""
import pandas as pd
import re 
import numpy as np
import matplotlib.pyplot as plt


'''-----------------------------------------------------------------------
The goal of this exercise is to find the best players (and the worst ones)
that tried most passes while succeding (or failing).
-----------------------------------------------------------------------'''


'''
The value stored in a row (match result) that contains match infos is stored as 
a string, which needs to be parsed or manipulated in some way to 
extract relevant information.
We used a division of string by dividing character.
First we divide the teams from the score, then again with a different 
character for the individual values.
'''
def get_score_from_label(string):
    string = str(string) # Make sure it's a string, altough not really necessary
    tokens = re.split('; |,', string) # Split by characters
    teams_raw = re.split('-', tokens[0])#Tokens[0] is the teams playing
    teams = list()
    for t in teams_raw:
        teams.extend([str(t.strip())])#We want leading and trailing whitespaces removed
    
    score_raw = re.split('-', tokens[1])# Getting individual scores
    score = list()
    for s in score_raw:
        score.extend([int(s.strip())])# Whitespaces removed
        
    return teams, score

''' Here we are creating a dictionary to contain, for each team (the team id
is the key), the performances for each week. 
Score = 3? Match won. Score = 1? A tie. Score = 0? Match lost. 
Each week will have a corresponding index in the 'performance array', 
with an associated value in {3,1,0}. 
'''
def get_dict_results(nation):
    ds_path = './dataset/matches/matches_'+nation+'.json'
    matches_ds = pd.read_json(ds_path)

    results = {}
    
    for i in range(len(matches_ds)):
        label = matches_ds['label'][i]
        week = matches_ds['gameweek'][i] # The gameweek goes from 1 to 38

        teams, score = get_score_from_label(label)#Getting the match info
        
        # Since there are 2 teams for each match, we are also registering
        # 2 teams's information at a time.
        team1 = teams[0]
        team2 = teams[1]
        
        score1 = score[0]        
        score2 = score[1]
        
        # We need to check if a team is in the keys of the dictionary
        # i.e. it has already a performance array that might contain data
        if team1 not in results.keys():
            results[team1] = np.zeros(38) # The 'performance array'
            
        if team2 not in results.keys():
            results[team2] = np.zeros(38)
        
        # Here we are registering the score for a given week
        # Side note: since the game week in the dataset starts from 1, a week-1 will 
        # give us the correct associated week in the performance array.
        if score1 > score2:
            # Winner is team 1
            results[team1][week-1] = 3
            results[team2][week-1] = 0
            
        elif score1 < score2: 
            # Winner is team 2
            results[team1][week-1] = 0
            results[team2][week-1] = 3
        else:
            # It's a tie
            results[team1][week-1] = 1
            results[team2][week-1] = 1
            
    return results

''' For calculating the max streak of wins, we check for consecutive occurrences
    of 3s, so when we find another value the streak is saved and the counter reset.'''
def max_streak(weekly_point):
    streaks = []
    current_streak = 0 # This acts as the counter
    for i in weekly_point:    
        if i == 3:
            current_streak +=1
        else:
            
            if current_streak > 0:
                streaks.extend([current_streak])
            current_streak = 0
            
    # Python sorts in ascending order. For ease of use, we want it in reversed
    # order, which is descending order
    streaks.sort()
    streaks.reverse()
    return streaks

''' For calculating the min streak of matches lost, we check for consecutive occurrences
    of 0s, so when we find another value the streak is saved and the counter reset.'''
def min_streak(weekly_point):
    streaks = []
    current_streak = 0
    for i in weekly_point:    
        if i == 0:
            current_streak +=1
        else:
            
            if current_streak > 0:
                streaks.extend([current_streak])
            current_streak = 0
            
    streaks.sort()
    streaks.reverse()
    return streaks

    

if __name__ == '__main__':

    # First load the relevant datasets
    players_ds = pd.read_json('./dataset/players.json')
    coaches_ds = pd.read_json('./dataset/coaches.json')
    teams_ds = pd.read_json('./dataset/teams.json')
    nations = ['England'] # It's a list so other nations can be added easily
    
    res = {}
    teams_streaks = []
    teams_streaks_loss = []
    
    for nat in nations:
        tmp_res = get_dict_results(nat)
        res.update(tmp_res)
    
    # Since the figure to plot in will be used after in a loop, 
    # we declare it before said loop. Also setting the style.
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure(figsize=(10,5))

    for key in res.keys(): # A key is a team id
        team_data = res[key] # Get the season performance array
        
        week_names = list(range(1, 39))
        
        points = np.zeros(38) # Total points
        for i in range(0, 38):
            points[i] = sum(team_data[0:i]) # For the line plot, we want the total number of points until the nth week
        
        # Here calculate the performance of the team using its 'performance array'
        team_streak = max_streak(team_data)
        team_streak_loss= min_streak(team_data)
        
        # Save the streaks for later, also save the key for later name retrieval
        teams_streaks.extend([[key, team_streak]])
        teams_streaks_loss.extend([[key, team_streak_loss]])
        
        # Add line to the plot
        plt.plot(week_names, points, label = key) #Without calling plt.show() immediately after, the lines will overlap
    
    plt.legend(bbox_to_anchor=(1, 1)) # Make a legend and put it on the right
    plt.xticks(week_names) # Give the names for each week (tick is an increment, so a new week)
    plt.xlabel('Week number')
    plt.ylabel('Points')
    plt.show()
    
    ''' Here starts the second part of the exercise. We want to know which are the teams
        that had the largest win/loss streak and the second after. '''
    
    
    # Since the sorting happens by the first value of the (ordered) performance array, 
    # we have to use this lambda to tell the sorting function to use said value as the key for ordering.
    teams_streaks.sort(key = lambda teams_streaks: teams_streaks[1][0])
    teams_streaks_loss.sort(key = lambda teams_streaks_loss: teams_streaks_loss[1][0])

    # Go from ascending order from descending order. This way we can easily get the max value
    teams_streaks.reverse()
    teams_streaks_loss.reverse()

    first_worst = teams_streaks_loss[0][0]
    second_worst = teams_streaks_loss[1][0]

    first_best = teams_streaks[0][0]
    second_best = teams_streaks[1][0]
    
    print() # Just adding a new line after the plot
    print('Best performing team: ', first_best)
    print('Second best performing team: ', second_best)
    print('----')
    print('Worst performing team: ', first_worst)
    print('Second worst performing team: ', second_worst)
    
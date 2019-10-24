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
def get_score_from_label(string):
    string = str(string)
    tokens = re.split('; |,', string)
    teams_raw = re.split('-', tokens[0])
    teams = list()
    for t in teams_raw:
        teams.extend([str(t.strip())])
    
    score_raw = re.split('-', tokens[1])
    score = list()
    for s in score_raw:
        score.extend([int(s.strip())])

    
    return teams, score

def get_dict_results(nationality):
    #ds_path = str('./dataset/matches_'+nationality+'.json')
    ds_path = './dataset/matches/matches_'+nationality+'.json'
    print(ds_path)
    matches_ds = pd.read_json(ds_path)

    results = {}
    
    
    for i in range(len(matches_ds)):
        label = matches_ds['label'][i]
        week = matches_ds['gameweek'][i]

        teams, score = get_score_from_label(label)
        
        team1 = teams[0]
        team2 = teams[1]
        
        score1 = score[0]        
        score2 = score[1]
        
        if team1 not in results.keys():
            results[team1] = np.zeros(38)
            
        if team2 not in results.keys():
            results[team2] = np.zeros(38)
        
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
        
    print("%s | # of elements: %d" % (ds_path, len(results.keys())))

    return results

def max_streak(weekly_point):
    streaks = []
    current_streak = 0
    for i in weekly_point:    
        if i == 3:
            current_streak +=1
        else:
            
            if current_streak > 0:
                streaks.extend([current_streak])
            current_streak = 0
    streaks.sort()
    streaks.reverse()
    return streaks

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

    players_ds = pd.read_json('./dataset/players.json')
    coaches_ds = pd.read_json('./dataset/coaches.json')
    teams_ds = pd.read_json('./dataset/teams.json')
    nationalities = ['England']
    
    res = {}
    teams_streaks = []
    teams_streaks_loss = []
    # Merge dictionaries
    
    for nat in nationalities:
        tmp_res = get_dict_results(nat)
        res.update(tmp_res)
    
    fig = plt.figure(figsize=(10,5))
    
    first_highest = ['', 0]
    
    for key in res.keys():
        team_data = res[key]
        
       
        week = range(1, 39)
        week_names = []
        for i in week:
            week_name = str('W\n%d' % i)
            week_names.append(week_name)
        points = np.zeros(38)
        for i in range(0, 38):
            points[i] = sum(team_data[0:i])
        
        team_streak = max_streak(team_data)
        team_streak_loss= min_streak(team_data)
        teams_streaks.extend([[key, team_streak]])
        teams_streaks_loss.extend([[key, team_streak_loss]])
        
        plt.plot(week_names, points, label = key)
    
    plt.legend(bbox_to_anchor=(1, 1))
    plt.show()
    teams_streaks.sort(key = lambda teams_streaks: teams_streaks[1][0])
    teams_streaks_loss.sort(key = lambda teams_streaks_loss: teams_streaks_loss[1][0])

    teams_streaks.reverse()
    teams_streaks_loss.reverse()

    
    first_worst = teams_streaks_loss[0]    
    second_worst = teams_streaks_loss[1]

    first_best = teams_streaks[0]    
    second_best = teams_streaks[1]
    
    print("first_worst = %s second_worst= %s \nfirst_best= %s, second_best= %s" % (first_worst[0], second_worst[0], first_best[0], second_best[0]))
    
    
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
                interval = minutes // 9
            else:
                interval = 5
        elif period == '2H':
            if minutes < 45:
                interval = 6 + ( minutes // 9)
            else:
                interval = 11
        
        goals_df.at[i, 'eventInterval'] = interval
        
        print(type(minutes))
        
    fr_interval = np.zeros(12)
    for a in range (0, 12):
        for i in range(len(goals_df)):       
            if goals_df['eventInterval'][i] == a:
                fr_interval[a] += 1
                
    x = np.arange(12)
    print(fr_interval)
    plt.bar(x, fr_interval)
    plt.show()
                
            
        
        
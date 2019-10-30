#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:35:59 2019

@author: marco
"""
import pandas as pd
from datetime import datetime
from matplotlib.pyplot import Rectangle
from matplotlib.patches import Arc, ConnectionPatch
import matplotlib.pyplot as plt
import seaborn as sns

def get_match_id(team1, team2, str_date, nationality):
    
    matches_dataset = pd.read_json(('./dataset/matches/matches_%s.json' % nationality))
    
    date = datetime.strptime(str_date, '%Y-%m-%d')
    for i in range(len(matches_dataset)):
        match_id = matches_dataset['wyId'][i]
        match_label = matches_dataset['label'][i]
        str_match_date = matches_dataset['dateutc'][i]
        
        match_date = datetime.strptime(str_match_date, '%Y-%m-%d %H:%M:%S')
        if date.year == match_date.year and date.month == match_date.month and date.day == match_date.day:
            if team1 in match_label and team2 in match_label:
                return match_id
            
    return -1
            
def get_player_id(name, last_name):
    name = name.lower()
    last_name = last_name.lower()
    
    players = pd.read_json(str('./dataset/players.json'))
    
    for i in range(len(players)):
        player_id = players['wyId'][i]
        player_name = players['firstName'][i] + players['middleName'][i] + players['lastName'][i]
        player_name = player_name.lower()
        if name in player_name and last_name in player_name:
            return player_id
        
    return -1

def get_match_events(events_dataset, match_id, player1_id, player2_id, nationality):
    event_types = ['pass', 'shot', 'duel', 'free kick']
    events = {player1_id:[], player2_id:[]}
    
    for i in range(len(events_dataset)):
        event_match_id = events_dataset['matchId'][i]
        
        if event_match_id == match_id:
            player_id = events_dataset['playerId'][i]
            
            if player1_id == player_id or player2_id == player_id:    
                event_type = events_dataset['eventName'][i]
    
                if event_type.lower() in event_types:
                    
                    positions = events_dataset['positions'][i]
                    match_period = events_dataset['matchPeriod'][i]
                    
                    positions = [positions[0]['x'], 100 - positions[0]['y']]
                    
                    if match_period == '1H' and False:
                        positions[0] = 100 - positions[0]
                        positions[1] = 100 - positions[1]
                        
                    positions[0] = 120 * positions[0] * 0.01
                    positions[1] = 80 * positions[1] * 0.01
                    
                    events[player_id].append(positions)
                  
    return events
    

def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 120, height = 80, fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    midline = ConnectionPatch([60,0], [60,80], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,32], width = 4.9, height = 16, fill = False)
    RightSixYard = Rectangle([115.1,32], width = 4.9, height = 16, fill = False)


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)

def print_field_performance(positions, color):
    # Print the field
    fig=plt.figure() #set up the figures
    fig.set_size_inches(7, 5)
    ax=fig.add_subplot(1,1,1)
    draw_pitch(ax) #overlay our different objects on the pitch
    plt.ylim(-2, 82)
    plt.xlim(-2, 122)
    plt.axis('off')
    # End drawing field
    
    x_positions = [p[0] for p in positions]
    y_positions = [p[1] for p in positions]
    
    sns.kdeplot(x_positions, y_positions, shade = "True", color = color, n_levels = 30)
   
    plt.show()

if __name__ == '__main__':
    nationality = 'Spain'
    events_dataset = pd.read_json(str('./dataset/events/events_%s.json' % nationality))
    matches_dataset = pd.read_json(('./dataset/matches/matches_%s.json' % nationality))

    match_id = get_match_id('Barcelona', 'Real Madrid', '2018-5-6', nationality)
    
    if match_id == -1:
        print('Match not found.')
        exit(-1)
    
    ronaldo_id = get_player_id('Cristiano', 'Ronaldo')
    messi_id = get_player_id('Lionel', 'Messi')
    
    events = get_match_events(events_dataset, match_id, ronaldo_id, messi_id, 'Spain')
    

    print('Ronaldo performance heatmap:')
    print_field_performance(events[ronaldo_id], 'blue')
    
    print('Messi performance heatmap: ')
    print_field_performance(events[messi_id], 'green')
        
    
    
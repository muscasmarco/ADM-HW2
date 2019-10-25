#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:10:37 2019

@author: marco
"""
import pandas as pd 
import matplotlib.pyplot as plt

''' Here we are trying to see if there's a correlation between the 
    height of a player and the number of air duels won. '''

if __name__ == '__main__':
    # Loading the events dataset for the premier league, here are stored events 
    # such as air duels and their outcome (won, lost, ...)
    event_ds = pd.read_json('./dataset/events/events_England.json')
    player_performance = {}
    
    for i in range(len(event_ds)):
        event_type = event_ds['subEventName'][i] # First we get the specific name of the event
        
        if event_type == 'Air duel': # We are only interested if the event is an air duel
            tags = event_ds['tags'][i] # The tags field contains information about the outcome
            tag_values = [t['id'] for t in tags] # but first we have to extract the individual values
            player_id = event_ds['playerId'][i]
            # The player id will be used as the key for the dictionary
            # It will be used later to join, on the player id, to make the height:ratio list
            if player_id not in player_performance.keys():
                # the performance array for a player has arbitrary indexes:
                # [0] is for won air duels, [1] is for lost ones 
                player_performance[player_id] = [0, 0] 
            
            # The 1801 and 703 tag values signal a successful outcome for the event
            if 1801 in tag_values and 703 in tag_values:
                # Successful
                player_performance[player_id][0] += 1
            else:
                # Attempted and failed
                player_performance[player_id][1] += 1


    # Build height-ratio table
    player_ds = pd.read_json('./dataset/players.json')
    plot_list = []
    
    for i in range(len(player_ds)):
        player_id = player_ds['wyId'][i] # Get the player id
        height = player_ds['height'][i] # Get the player's height
        
        if player_id in player_performance.keys(): # If we have a player id, then there should be the performance array
            
            # Calculate the ratio
            successful = player_performance[player_id][0]
            failed = player_performance[player_id][1]    
            ratio = 0 # We suppose the ratio is 0 
            if failed != 0: # Must avoid division by 0
                ratio = successful / (successful + failed)
                
            if ratio != 0: # Here is just a threshold, if this line gets deleted even the player with no successful 
                           # air duels will be plotted. 
                plot_list.append([height, ratio])
            
    # Plotting
    plot_list.sort(key=lambda x : x[0]) # We want the players data sorted by height, ascending order
    height_list = [p[0] for p in plot_list] # List remains ordered, no need to worry if we split 'plot_list'
    ratio_list = [p[1] for p in plot_list]
    
    plt.figure(figsize=(8,5))
    plt.xlabel = 'height'
    plt.ylabel = 's/f ratio'
    colors = ['blue', 'yellow', 'orange', 'red', 'green', 'purple', 'grey', 'black', 'pink']
    
    height_interval = 5 # This is an arbitrary value to split the height values in 5cm increments
    
    # Rounding the min_height to the nearest lower multiple of 10: doing so allows for a nice visualization
    min_height = min(height_list) - (min(height_list)%10) 
    max_height = max(height_list) + (10 - max(height_list)%10) # Round to the nearest greater multiple of 10
    plt.xticks(range(min_height, max_height+1, 5)) # For visibility, add ticks in 5cm increments between min height and max height

    for i in range(len(plot_list)):
        r = plot_list[i]
        
        # The way the colors is assigned seems complicated because not only we want a color from the colors list,
        # but if the colors are not enough (too many 5cm increments) they will start being assigned from the first one (rotation)
        # Also we don't want 160 to be an index, so we normalize it to be in the [0, len of color list) range.
        plt.scatter(r[0], r[1], lw=0.1, c = colors[int((r[0] - min_height)//height_interval % len(colors))])
                    
    # We want the axis to start 5cm before the min height value rounded to the lowest multiple 10, 
    # and the other max axis to be 5cm after the nearest greater multiple of 10
    plt.axis([min_height-5, max_height+5, 0, 1])
    
    
    plt.show()
    
    ''' It really looks like there is a positive correlation, between the 
        height and the success ratio in air duels! '''
            
        
    
    
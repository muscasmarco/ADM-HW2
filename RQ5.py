#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:10:37 2019

@author: marco
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

if __name__ == '__main__':
    print('Loading the events dataset')
    event_ds = pd.read_json('./dataset/events/events_England.json')
    
    print('Dataset loaded')    
    
    player_performance = {}
    
    for i in range(len(event_ds)):
        event_type = event_ds['subEventName'][i]    
        
        if event_type == 'Air duel':
            tags = event_ds['tags'][i]
            tag_values = [t['id'] for t in tags]
            player_id = event_ds['playerId'][i]
            
            if player_id not in player_performance.keys():
                player_performance[player_id] = [0, 0]
                
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
        player_id = player_ds['wyId'][i]
        height = player_ds['height'][i]
        
        if player_id in player_performance.keys():
            successful = player_performance[player_id][0]
            failed = player_performance[player_id][1]
            
            ratio = 0
            
            if failed != 0:
                ratio = successful / (successful + failed)
            
            if ratio != 0:
                plot_list.append([height, ratio])
            
    # Plotting
    plot_list.sort(key=lambda x : x[0])
    height_list = [p[0] for p in plot_list]
    ratio_list = [p[1] for p in plot_list]
    
    interval_width = len(plot_list) / 4
    
    plt.xlabel = 'height'
    plt.ylabel = 's/f ratio'
    
    #avg_height = sum(height_list)/len(height_list)
    #colors = ['blue', 'yellow', 'orange', 'red', 'green', 'purple', 'grey', 'black', 'pink',
    #          'cyan']
    
    colors = cm.rainbow(np.linspace(0, 10, len(plot_list)))
    
    min_height = min(height_list)
    for i in range(len(plot_list)):
        r = plot_list[i]
                
        plt.scatter(r[0], r[1], lw=0.1, c = colors[int((r[0] - min_height)//5)])
                    
    
    plt.axis([min(height_list)-5, max(height_list)+5, 0, 1])
    
    
    plt.show()
            
        
    
    
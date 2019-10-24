# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 06:20:30 2019

@author: melik
"""
#it is interesting to analize witch nationalities have better players! for doing that we can consider the ratio of successful passes player has made and the player's nationality
import pandas as pd
import operator
import matplotlib.pyplot as plt

if __name__ == '__main__':
    event_ds = pd.read_json('../DS/events_England.json')
    player_ds = pd.read_json('../DS/players.json')

    #threshold
    #each player has howmany passes made and calculate the mean for all players
    data = event_ds[event_ds["subEventId"].isin([i for i in range(80,87)])].groupby(["playerId"]).count()
    data.reset_index(drop=False,inplace=True)
    threshold = data["eventId"].mean()
    
    
    #check for all kind of passes with accuration
    player_performance = {}
    for i in range(len(event_ds)):
        event_type = event_ds['subEventId'][i]
        if event_type in range(80,87):
            tags = event_ds['tags'][i]
            tag_values = [t['id'] for t in tags]
            player_id = event_ds['playerId'][i]
            
            if player_id not in player_performance.keys():
                player_performance[player_id] = [0, 0]
                
            if 1801 in tag_values:
                # Successful
                player_performance[player_id][0] += 1
            else:
                # Attempted and failed
                player_performance[player_id][1] += 1
             
                
    # calculation of the ratio and showing it with players shortnames and their wyId
    #adding the nationality of players to the list
    Player_list = []
    dic = dict(player_ds["birthArea"])
    for i in range(len(player_ds)):
        player_id = player_ds['wyId'][i]
        short_name = player_ds['shortName'][i]
        try:
            v = dic.get(i).get("name")
        except:
            pass
            
    
        player_data = data.loc[data.playerId == player_id , "tags"]
  
        if player_data is not None and len(player_data) > 0:      
            number_passes = player_data.tolist()[0]
            
            #using the threshold
            if number_passes >= threshold: 
                if player_id in player_performance.keys():
                    successful = player_performance[player_id][0]
                    failed = player_performance[player_id][1]
                    
                    ratio = 0 
                    if failed != 0:
                        ratio = successful / (successful + failed)
                    Player_list.append([short_name, ratio, v])
                    
    #reversing the list and sorting it to find the 10 first players with high ratio     
    Player_list.sort(key=operator.itemgetter(1))
    Player_list.reverse()
    
    #printing the list
    for i in range(len(Player_list)):
        print('(%d) - %s' % (i+1, Player_list[i]))
    
    #to make a plot to show each country has howmany players with high ratio
    plt.figure(figsize=(20,5))
    x = pd.DataFrame(Player_list, columns=['name', 'ratio', 'nationality']).groupby('nationality').count()[['name']]
    plt.bar(height=x['name'], x = x.index)
    plt.xticks(x.index, rotation = 'vertical')
    plt.show()
    
    
        
    
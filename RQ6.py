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
    all_passes = event_ds[event_ds["subEventId"].isin([i for i in range(80,87)])].groupby(["playerId"]).count()
    all_passes.reset_index(drop=False,inplace=True)
    threshold = all_passes["eventId"].mean()
    
    #check for all kind of passes with accuration(successful passes)
    passes_successful = {}
    for i in range(len(event_ds)):
        event_type = event_ds['subEventId'][i]
        if event_type in range(80,87):
            tags = event_ds['tags'][i]
            tag_values = [t['id'] for t in tags]
            player_id = event_ds['playerId'][i]
            
            if player_id not in passes_successful.keys():
                passes_successful[player_id] = [0, 0]
                
            if 1801 in tag_values:
                # Success
                passes_successful[player_id][0] += 1
            else:
                # failure
                passes_successful[player_id][1] += 1
             
                
    # calculation of the ratio and showing it with players shortnames and their wyId
    # adding the nationality of players to the list
    Player_list = []
    dic = dict(player_ds["birthArea"])
    for i in range(len(player_ds)):
        player_id = player_ds['wyId'][i]
        short_name = player_ds['shortName'][i]
        try:
            v = dic.get(i).get("name")
        except:
            pass
        
        # for having number of passes that each player had
        player_data = all_passes.loc[all_passes.playerId == player_id , "tags"]
        if player_data is not None and len(player_data) > 0:      
            number_passes = player_data.tolist()[0]
            
            #using the threshold so if a player has less passes than the threshold we are not going to consider that player
            if number_passes >= threshold: 
                if player_id in passes_successful.keys():
                    successful = passes_successful[player_id][0]
                    failed = passes_successful[player_id][1]
                    
                    ratio = 0 
                    if failed != 0:
                        ratio = successful / (successful + failed)
                    Player_list.append([short_name, ratio, v])
                    
    #reversing the list and sorting it to find the 10 first players with high ratio     
    Player_list.sort(key=operator.itemgetter(1))
    Player_list.reverse()
    
    #printing the list of all players short names and their ratio and their nationality
    for i in range(len(Player_list)):
        print('(%d) - %s' % (i+1, Player_list[i]))
    
    #to make a plot to show each country has howmany players with high ratio
    plt.figure(figsize=(20,5))
    x = pd.DataFrame(Player_list, columns=['name', 'ratio', 'nationality']).groupby('nationality').count()[['name']]
    plt.bar(height=x['name'], x = x.index)
    plt.xticks(x.index, rotation = 'vertical')
    plt.show()
    # from the plot it is obvious that english players are more likely to have high ratio for successful passes
    
    
        
    
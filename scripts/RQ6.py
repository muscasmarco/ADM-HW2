# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------
The goal of this exercise is to show a new interesting result about the dataset
that we found. it was interesting for us to analize which nationalities have
better players!(to be more specific, players from which countries have higher 
ratio of successful passes. we had the ratio from RQ4 and now we had to use the
birth Area column in player_ds which was a dictionary and use the first value
of it(the country of birth's name).
at the end we made a plot which shows the name of the cpuntries and the number
of players with high ratio.
---------------------------------------------------------------------------'''

# First load the relevant datasets
import pandas as pd
import operator
import matplotlib.pyplot as plt

if __name__ == '__main__':
    event_ds = pd.read_json('../DS/events_England.json')
    player_ds = pd.read_json('../DS/players.json')
    
    # each player has howmany passes made and calculate the mean for all players
    all_passes = event_ds[event_ds["subEventId"].isin([i for i in range(80,87)])].groupby(["playerId"]).count()
    all_passes.reset_index(drop=False,inplace=True)
    threshold = all_passes["eventId"].mean()
    
    # creating a dictionary to contain, for each player (the playerId is the key), the successful passes.
    passes_successful = {}
    for i in range(len(event_ds)): # check for all kind of passes which has been successful
        event_type = event_ds['subEventId'][i]
        if event_type in range(80,87): # the range of the subId of all passes
            tags = event_ds['tags'][i] # the column that contains tag 1801 
            tag_values = [t['id'] for t in tags]
            player_id = event_ds['playerId'][i]
            
            if player_id not in passes_successful.keys():
                passes_successful[player_id] = [0, 0]
                
            if 1801 in tag_values: # a completed pass has tag 1801
                # Success
                passes_successful[player_id][0] += 1
            else:
                # failure
                passes_successful[player_id][1] += 1

                
    # calculation of the ratio and appending it to a list with players shortnames and wyId
    # adding the nationality of players to the list
    Player_list = []
    dic = dict(player_ds["birthArea"]) # the column that has the players nationality
    for i in range(len(player_ds)):
        player_id = player_ds['wyId'][i]
        short_name = player_ds['shortName'][i] # players short names
        try: # for avoidig errors we used try except
            v = dic.get(i).get("name")
        except:
            pass
        
        # for having number of passes that each player had
        player_data = all_passes.loc[all_passes.playerId == player_id , "tags"]
        if player_data is not None and len(player_data) > 0:      
            number_passes = player_data.tolist()[0]
            
            #calculating the ratio
            #using the threshold so if a player has less passes than the threshold we are not going to consider that player
            if number_passes >= threshold: 
                if player_id in passes_successful.keys():
                    successful = passes_successful[player_id][0]
                    failed = passes_successful[player_id][1]
                    
                    ratio = 0 
                    if failed != 0:
                        ratio = successful / (successful + failed)
                    Player_list.append([short_name, ratio, v])
                    
    #reversing the list and sorting it (Go from ascending order from descending order)to find the 10 first players with high ratio     
    Player_list.sort(key=operator.itemgetter(1))
    Player_list.reverse()
    
    #printing the list of all players short names and their ratio and their nationality
    for i in range(len(Player_list)):
        print('(%d) - %s' % (i+1, Player_list[i]))
    
    #to make a plot to show each country has howmany players with high ratio
    plt.figure(figsize=(20,5)) # stretching the plot(resizing it)
    # this line will make a dataframe from the player_list with 3 columns named like below and group them by the nationality and count how many players with same nationality exist
    x = pd.DataFrame(Player_list, columns=['name', 'ratio', 'nationality']).groupby('nationality').count()[['name']]
    plt.bar(height=x['name'], x = x.index) # making a bar plot
    plt.xticks(x.index, rotation = 'vertical') # for rotating the name of the countries 45' for better readability
    plt.show() #showing the plot
    # from the plot it is obvious that english players are more likely to have high ratio for successful passes
    
    
        
    
import pandas as pd
import operator
# we need operator for sorting the final list

'''---------------------------------------------------------------------------
The goal of this exercise is to find the top 10 players with the highest ratio
between completed passes and attempted passes.(avoiding meaningless results)
---------------------------------------------------------------------------'''
if __name__ == '__main__':
    # First load the relevant datasets
    event_ds = pd.read_json('../DS/events_England.json')
    player_ds = pd.read_json('../DS/players.json')

    
    """
    the threshold is used to make sure that we have avoided meaningless results!
    for making the threshold we calculated the mean of all passes that all players
    have made and just consider the players that have more passes than that number.
    so we need the number of passes that each player has made, by using group by 
    over playerId and knowing that the passes have the subIds between 80-86
    we count the number of passes.
    but not all these passes were successful! we need to detach the ones that were
    successful.
    then at the end we calculated the ratio of successful passes that player had.
    at the end we sorted and listed the 10 players from premier league and printed
    them out with their short names and ratios
    """ 
    
    # each player has howmany passes made and calculate the mean for all players
    allkind_passes = event_ds[event_ds["subEventId"].isin([i for i in range(80,87)])].groupby(["playerId"]).count()
    allkind_passes.reset_index(drop=False,inplace=True)
    threshold = allkind_passes["eventId"].mean() # threshold
    
    # creating a dictionary to contain, for each player (the playerId is the key), the successful passes.
    successful_player = {} 
    for i in range(len(event_ds)): # check for all kind of passes which has been successful
        event_type = event_ds['subEventId'][i]  

        if event_type in range(80,87): # the range of the subId of all passes
            tags = event_ds['tags'][i] # the column that contains tag 1801 
            tag_values = [t['id'] for t in tags]
            player_id = event_ds['playerId'][i] # check for each player
            
            if player_id not in successful_player.keys():
                successful_player[player_id] = [0, 0]
                
            if 1801 in tag_values: # a completed pass has tag 1801
                # Successful
                successful_player[player_id][0] += 1
            else:
                # failed
                successful_player[player_id][1] += 1
                
                
    # calculation of the ratio and appending it to a list with players shortnames and wyId
    Player_list = []
    for i in range(len(player_ds)):
        player_id = player_ds['wyId'][i] # each playerId
        short_name = player_ds['shortName'][i] # the player short name

        player_data = allkind_passes.loc[allkind_passes.playerId == player_id , "tags"]  
        if player_data is not None and len(player_data) > 0:      
            number_passes = player_data.tolist()[0]
            
            #using the threshold
            if number_passes >= threshold: 
                if player_id in successful_player.keys():
                    success = successful_player[player_id][0]
                    fail = successful_player[player_id][1]
                    
                    ratio = 0 
                    if fail != 0: 
                        ratio = success / (success + fail)
                    Player_list.append([short_name, ratio])
    #reversing the list and sorting it (Go from ascending order from descending order)to find the 10 first players with high ratio     
    Player_list.sort(key=operator.itemgetter(1))
    Player_list.reverse()
    
    # printing the list with numbers from 1 to 10
    for i in range(len(Player_list[:10])):
        print('(%d) - %s' % (i+1, Player_list[i]))
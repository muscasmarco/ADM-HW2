import pandas as pd
import operator
# we need operator for sorting the final list

if __name__ == '__main__':
    event_ds = pd.read_json('../DS/events_England.json')
    
    # threshold
    # each player has howmany passes made and calculate the mean for all players
    allkind_passes = event_ds[event_ds["subEventId"].isin([i for i in range(80,87)])].groupby(["playerId"]).count()
    allkind_passes.reset_index(drop=False,inplace=True)
    threshold = allkind_passes["eventId"].mean()
    
    #check for all kind of passes which has been successful
    successful_player = {}
    for i in range(len(event_ds)):
        event_type = event_ds['subEventId'][i]  

        if event_type in range(80,87):
            tags = event_ds['tags'][i]
            tag_values = [t['id'] for t in tags]
            player_id = event_ds['playerId'][i]
            
            if player_id not in successful_player.keys():
                successful_player[player_id] = [0, 0]
                
            if 1801 in tag_values:
                # Successful
                successful_player[player_id][0] += 1
            else:
                # failed
                successful_player[player_id][1] += 1
                
                
    # calculation of the ratio and appending it to a list with players shortnames and wyId
    player_ds = pd.read_json('../DS/players.json')
    
    Player_list = []
    for i in range(len(player_ds)):
        player_id = player_ds['wyId'][i]
        short_name = player_ds['shortName'][i]
        
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
                    
    #reversing the list and sorting it to find the 10 first players with high ratio     
    Player_list.sort(key=operator.itemgetter(1))
    Player_list.reverse()
    
    #printing the list:
    for i in range(len(Player_list[:10])):
        print('(%d) - %s' % (i+1, Player_list[i]))
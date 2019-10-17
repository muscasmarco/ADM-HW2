# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 02:32:20 2019

@author: melik
"""
import pandas as pd
import time
import operator

def coaches_dictionary(coaches):
    coach  = {}
    for i in range(len(coaches)):
        key = coaches['currentTeamId'][i]
        if key != 0:
            new_birth_date = coaches['birthDate'][i]
            
            if key not in coach.keys():
                coach[key] = new_birth_date
            else:
                found_birth_date = coach[key]            
                new_date = time.strptime(new_birth_date, "%Y-%m-%d")
                found_date = time.strptime(found_birth_date, "%Y-%m-%d")
                
                if new_date < found_date:
                    coach[key] = new_birth_date
    return coach
    
def team_id_name_list(df):
    
    team_names = list()
    
    for i in range(len(df)):
        t_official_name = df['officialName'][i]
        t_id = df['wyId'][i]
        
        team_names.append([t_id, t_official_name])
        
    return team_names
        
        
                
def team_birth_list(d,lst):
    team_birth = []
    for key in d.keys():
        for item in lst:
            if key == item[0]:
                team_name = item[1] 
                birth_date = d[key]
                team_birth.append([team_name,birth_date])
    return team_birth

if __name__ == "__main__":
    coaches = pd.read_json("../DS/coaches.json")
    teams = pd.read_json("../DS/teams.json")
    
    d =coaches_dictionary(coaches)
    t_id_names = team_id_name_list(teams)
    team_birth = team_birth_list(d, t_id_names)
    
    team_birth.sort(key=operator.itemgetter(1))
    team_birth.reverse()
    
    for i in range(len(team_birth[:10])):
        add_str = ''
        
        if i == 0:
            add_str = '[Youngest Coach]'
        else:
            add_str = ''
        
        print('(%d) - %s %s' % (i+1, team_birth[i][0], add_str))
    
    
    
    
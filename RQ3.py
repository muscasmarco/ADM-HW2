# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 02:32:20 2019

@author: melik
"""
import pandas as pd
import time
import operator
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

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
        t_official_name = str(df['officialName'][i])
        t_id = int(df['wyId'][i])
                
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

def get_age(birthdate):
    new_date = birthdate.split('-')    
    new_date = list(map(int, new_date))
    born = date(new_date[0], new_date[1], new_date[2])
    today = date.today() 
    days_in_year = 365.2425
    age = int((today - born).days / days_in_year)
    
    return age

if __name__ == "__main__":
    coaches = pd.read_json("./dataset/coaches.json")
    teams = pd.read_json("./dataset/teams.json")
    matches = pd.read_json('./dataset/matches/matches_England.json')
    teams = teams[teams.area.apply(lambda x : x['name'] == 'England')]
    teams = teams[teams.type == 'club']
    teams = teams.reset_index(drop=True)
    
    
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
    
    # Plotting age distribution
    coaches_ids = []
    for i in range(len(matches)):
        teams_data = matches['teamsData'][i]
        coach_id = [teams_data[key]['coachId'] for key in teams_data.keys()]
        coaches_ids.extend(coach_id)
    
    coaches_ids = list(dict.fromkeys(coaches_ids))
    age_distribution = []
    for i in range(len(coaches)):
        coach_id = coaches['wyId'][i]
        if coach_id in coaches_ids:
            coach_birthday = coaches['birthDate'][i]
            age = get_age(coach_birthday)
            age_distribution.append(age)
    
        
    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    sns.set_style("darkgrid")

    
    ax.set_xlabel('Team leagues', fontweight='bold')
    ax.set_ylabel('Age', fontweight='bold')
    fig.suptitle('Coaches age distribution', fontsize=14, fontweight='bold')
    
    b = sns.boxplot([age_distribution], ax=ax, orient='v', width=0.2)
    ax = sns.swarmplot( data=age_distribution, color=".25")    
    b.set_xticklabels(['Premier League'])
    
    
    
    
    
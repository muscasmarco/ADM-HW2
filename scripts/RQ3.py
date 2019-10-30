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

''' The point of this exercise is to show which teams, in this case the 
    ones in the premier league, have the youngest coaches.
    Then we have to rank them based on this. For the second part, it's 
    showing the age distribution.
'''


''' This function has been made to create a dictionary where the team is 
    the key, and the birthdate of the youngest coach is the value. '''
def coaches_dictionary(coaches):
    coach  = {}
    
    # We iterate over the coaches dataframe
    for i in range(len(coaches)):
        key = coaches['currentTeamId'][i] # We get the key for the dictionary
        if key != 0: # Side note: since more coaches in the df have the same team id = 0
                     # we did not make assumptions on which team they belonged.
            new_birth_date = coaches['birthDate'][i] # Get the birthdate in YYYY-mm-dd format
            if key not in coach.keys(): # if the team is not registered in the dictionary
                coach[key] = new_birth_date # add the key and put the first found birthdate
            else:
                #`Otherwise compare the newly found birthdate with the one already 'registered'
                found_birth_date = coach[key]            
                new_date = time.strptime(new_birth_date, "%Y-%m-%d")
                found_date = time.strptime(found_birth_date, "%Y-%m-%d")
                
                if new_date < found_date: # Eventually, if the newly found is more recent, delete the old one and put the new one
                    coach[key] = new_birth_date
    # Side note: A dictionary was used for easy and fast access to a value by id
    return coach
    
''' This one is basically a support function, so we get easily the official team name
    with the relative team id. '''
def team_id_name_list(df):
    
    team_names = list()
    
    for i in range(len(df)): # Iterate over the dataframe
        
        # Get team data and add it to the list
        t_official_name = str(df['officialName'][i])
        t_id = int(df['wyId'][i])
                
        team_names.append([t_id, t_official_name])
        
    return team_names
        
''' Another support function. It's supposed to take the dictionary of 
    { team id: youngest coach birthdate} and perform a 'join' on the team id,
    so we get the team name and the youngest coach's age in the same 
    data structure for easy reading when data is printed '''
def team_birth_list(d,lst):
    team_birth = []
    for key in d.keys():
        for item in lst:
            if key == item[0]:
                team_name = item[1] 
                age = get_age(d[key])
                team_birth.append([team_name,age])
    return team_birth

''' Support function to easily calculate the age given a birthdate formatted
    as a string like YYYY-mm-dd'''
def get_age(birthdate):
    new_date = birthdate.split('-')    
    new_date = list(map(int, new_date))
    born = date(new_date[0], new_date[1], new_date[2])
    today = date.today() 
    days_in_year = 365.2425 # Must keep count of the extra day in a year
    age = int((today - born).days / days_in_year)
    
    return age

if __name__ == "__main__":
    # Load the needed datasets
    coaches = pd.read_json("./dataset/coaches.json")
    teams = pd.read_json("./dataset/teams.json")
    matches = pd.read_json('./dataset/matches/matches_England.json')
    # Here we are filtering out the teams that are not from England and 
    # of course, the national teams which do not play in the Premier League.
    teams = teams[teams.area.apply(lambda x : x['name'] == 'England')]
    teams = teams[teams.type == 'club']
    teams = teams.reset_index(drop=True) # resetting the index to avoid gaps while iterating over dataset
    
    
    d = coaches_dictionary(coaches)
    t_id_names = team_id_name_list(teams)
    team_birth = team_birth_list(d, t_id_names)    # Now we have a list like [[team_name, youngest coach birthdate]]

    team_birth.sort(key=lambda r : r[1]) # Sort by age, ascending order
    
    
    # Printing the ranking of the youngest coaches
    for i in range(len(team_birth[:10])):
        add_str = ''
        
        if i == 0:
            add_str = '| [Has the youngest coach]'
        else:
            add_str = ''
        
        print('(%d) - %s | Age %d %s' % (i+1, team_birth[i][0], team_birth[i][1], add_str))
    
    # Plotting age distribution
    ''' Since before we eliminated an older coach if we found a younger one, 
        we need to retrieve again the data this considering all the coaches
        that participated in the premier league. 
        This time though, just to be sure we are getting all of them, 
        we consider the matches of the premier league: 
        each match has the coaches id that participated.'''
     
    # First we get the coach ids
    coaches_ids = []
    for i in range(len(matches)):
        teams_data = matches['teamsData'][i]
        coach_id = [teams_data[key]['coachId'] for key in teams_data.keys()]
        coaches_ids.extend(coach_id)
    
    # Then we get the birthdates from the coaches dataset where wyId == coach_id
    coaches_ids = list(dict.fromkeys(coaches_ids))
    age_distribution = []
    for i in range(len(coaches)):
        coach_id = coaches['wyId'][i]
        if coach_id in coaches_ids:
            coach_birthday = coaches['birthDate'][i]
            age = get_age(coach_birthday)
            age_distribution.append(age)
    
    ''' Here we are plotting the distribution using a boxplot '''
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    sns.set_style("darkgrid")
    ax.set_xlabel('Team leagues', fontweight='bold')
    ax.set_ylabel('Age', fontweight='bold')
    fig.suptitle('Coaches age distribution', fontsize=14, fontweight='bold')
    
    b = sns.boxplot([age_distribution], ax=ax, orient='v', width=0.2)
    b.set_xticklabels(['Premier League'])
    
    
    
    
    
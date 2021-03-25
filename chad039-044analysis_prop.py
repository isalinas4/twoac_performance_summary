
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:39:25 2020

@author: isabe
"""


import numpy as np
import pandas as pd
import seaborn 
seaborn.set()
#from jaratoolbox import extraplots
import matplotlib.pyplot as plt 
#from statsmodels.stats.proportion import proportion_confint
#import sys
from jaratoolbox import behavioranalysis 
#from jaratoolbox import settings 
#from scipy.stats import norm
from collections import Counter

#Add the subject/dates you want to look at. 
subjects =  [
             'chad039',
             'chad042',
             'chad043',
             'chad044'
             #'chad056'
             ]


paradigm = 'twochoice'

sessions = ['20200630a',
            '20200701a',
            '20200702a',
            '20200703a',
            '20200704a',
            '20200705a',
            '20200706a',
            '20200707a',
            '20200708a',
            '20200709a',
            '20200710a'
            ]

mouse_perf = {}
for subject in subjects: 
        
    bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)
    
    sessionID = bdata['sessionID'] 
    unique_sessionID = np.unique(sessionID)  

    
    choice = bdata['choice']
    choice_left = bdata['choice'] == bdata.labels['choice']['left']
    choice_right = bdata['choice'] == bdata.labels['choice']['right']
    valid_choice = bdata['choice'] != bdata.labels['choice']['none']
    no_choice = bdata['choice'] == bdata.labels['choice']['none']
    
    valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
    valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
    total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
    total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])
    
    reward_side_mode = bdata['rewardSideMode']
    #targetAMdepth = bdata['targetAMdepth']
    
    hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']
    left_hits = valid_left_trials & choice_left 
    right_hits = valid_right_trials & choice_right
    left_errors = valid_left_trials & choice_right
    right_errors = valid_right_trials & choice_left
    total_errors = right_errors + left_errors
    

    
    false_alarms = bdata['nFalseAlarms']
    missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']
    misses_left = bdata['nMissesLeft']
    misses_right = bdata['nMissesRight']
    
    
    # Dataframe below collects the information needed for each trial. 
    df_trial_information = pd.DataFrame({'sessionID': sessionID,
                                         'hit_outcome': hit_outcome,
                                         'total_errors': total_errors,
                                         'total_misses' : missed_outcomes,
                                         'valid_choice': valid_choice
                                         })
    
    #Use this groupby to gather the data that should be summed per session
    df_session_information = df_trial_information.groupby(by = ['sessionID']) .sum()
    
    #Use this groupby to gather the information that should be maxed per session
    stage_one_information = df_trial_information.groupby(by =['sessionID']) .max()
    
    #Used to calculate performance
    percent_correct = ((df_session_information['hit_outcome']) /df_session_information['valid_choice'] *100)
    

   #this dataframe consolodates all of the other information to one dataframe that gets saved to an xlsx sheet
    mouse_perf[subject] = pd.DataFrame({
                               'percent_correct': percent_correct})
    
    
    #prints the session ID, task mode, and number of trials. 


'''    
    #plots the correct performance and how the animal performed with each side. Reminder that stage 1 will not be printed.
   # plt.scatter(unique_sessionID, percent_correct, color = 'blue', label = 'Left')
    #plt.plot(unique_sessionID, left_performance, color = 'blue')
    #plt.scatter(unique_sessionID, right_performance, color = 'red' , label = 'Right')
    #plt.plot(unique_sessionID, right_performance, color = 'red')
    plt.scatter(unique_sessionID, percent_correct, color = 'black')
    plt.title(subject + 'Performance')
    plt.xlabel('session')
    plt.ylabel('Percent animal chose the correct side (%)')
    plt.xticks(ticks=unique_sessionID)
    plt.ylim(0, 100)
    plt.show() 
'''
    
chad039 = mouse_perf['chad039']
chad042 = mouse_perf['chad042']
chad043 = mouse_perf['chad043']
chad044 = mouse_perf['chad044']

df_concat = pd.concat((chad039,chad042))
session_groupby = df_concat.groupby(level=0).mean()

result = df_concat.groupby(level=0, as_index=False).agg(
                      {'percent_correct':['mean','std','sem']})



plt.scatter(unique_sessionID, result.percent_correct['mean'], color = 'red')
#plt.plot(unique_sessionID, result.percent_correct['mean'], color = 'red')
plt.errorbar(unique_sessionID, result.percent_correct['mean'], yerr=result.percent_correct['sem'], color='black', capsize=2,)
plt.title('Average performance for Chad039-044')
plt.xlabel('Days in stage 3')
plt.ylabel('Average Percent Correct (%)')
plt.xticks(ticks=unique_sessionID)
plt.ylim(0,100)
plt.savefig('chad039-044_performance.png', dpi=300)
plt.show


# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 13:25:08 2021

@author: isabe
"""

import numpy as np
import pandas as pd
#import sys
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt  
#from jaratoolbox import settings 


#Below points the computer what file to use 

#Add the subject/dates you want to look at. 
subjects =  [ 
             'chad055',
             'chad056',
             #'chad057',
             'chad058'
             ]

sessionsEachSubject = { 
    'chad055': [#'20201212a', '20201213a'
            #'20210105a','20210106a','20210108a', '20210109a','20210110a', '20210111a',
            #'20210112a','20210113a','20210114a', '20210116a', '20210117a',
            #'20210118a', '20210119a'
            '20210128a','20210129a', '20210130a', '20210131a',
            '20210201a',
            '20210202a', '20210203a', '20210207a', 
            '20210208a',
            '20210209a', '20210210a'],
    
    'chad056': [#'20201216a', '20201217a'
            #'20210105a','20210106a','20210107a','20210108a', '20210109a','20210110a', '20210111a',
            #'20210112a','20210113a','20210114a',  '20210116a', '20210117a',
            #'20210118a', '20210119a',
            '20210128a','20210129a', '20210130a', '20210131a',
            '20210201a',
            '20210202a', '20210203a', '20210207a', 
            '20210208a',
            '20210209a', '20210210a'],
    
    'chad057': [#'20210104a','20210105a'
            #'20210106a','20210107a','20210108a', '20210109a','20210110a', '20210111a',
            #'20210112a','20210113a','20210114a', '20210116a', '20210117a',
            #'20210118a', '20210119a',
            '20210128a','20210129a', '20210130a', '20210131a',
            '20210201a',
            '20210202a', '20210203a', '20210207a', 
            '20210208a',
            '20210209a', '20210210a'],
    
    'chad058': [ #'20201215a','20201216a'
            #'20210106a','20210107a','20210108a', '20210109a','20210110a', '20210111a',
            #'20210112a','20210113a','20210114a', '20210116a', '20210117a',
            #'20210118a', '20210119a',
            '20210128a','20210129a', '20210130a', '20210131a',
            '20210201a',
            '20210202a', '20210203a', '20210207a', 
            '20210208a',
            '20210209a', '20210210a']
    
    }

mouse_perf = {}
for subject in subjects: 
    sessions = sessionsEachSubject[subject]    
    bdata = behavioranalysis.load_many_sessions(subject,paradigm='twochoice',sessions=sessions)
    
    #below is all the informationthat I am going to use. You can think aobut it like setting up a spreadsheet in excel
    sessionID = bdata['sessionID'] 
    unique_sessionID = np.unique(sessionID)
    target_frequency = bdata['targetFrequency']
    
    
    choice = bdata['choice']
    choice_left = bdata['choice'] == bdata.labels['choice']['left']
    choice_right = bdata['choice'] == bdata.labels['choice']['right']
    valid_choice = bdata['choice'] != bdata.labels['choice']['none']
    no_choice = bdata['choice'] == bdata.labels['choice']['none']
    
    valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
    valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
    total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
    total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])
    
    hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']
    left_hits = valid_left_trials & choice_left 
    right_hits = valid_right_trials & choice_right
    left_errors = valid_left_trials & choice_right
    right_errors = valid_right_trials & choice_left
    total_errors = right_errors + left_errors
    
    total_errors_right = bdata['nErrorsRight']
    total_licks_left = bdata['nLicksLeft']
    total_licks_right = bdata['nLicksRight']
    
    false_alarms_right = bdata['nFalseAlarmsRight']
    false_alarms_left = bdata['nFalseAlarmsLeft']
    missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']
    misses_left = bdata['nMissesLeft']
    misses_right = bdata['nMissesRight']
    
    #This is where I set up the initial data frame. You can think about it like a table. It will be more clear if you print(trial_information)
    trial_information = pd.DataFrame({'target_frequency': target_frequency,
                              'sessionID' : sessionID,
                              'choice': choice,
                              'valid_choice': valid_choice,
                              'hit_outcome': hit_outcome,
                              'total_errors': total_errors                              
                              })
    #Here it separtates it by each session and target frequency using the .groupby([]) function. Because the data from the above data frame is organized in 1s/0s or T/F I can groupby sum so get the information I need. 
    session_information = trial_information.groupby(['sessionID','target_frequency']).sum() #sum function
    
    #Below is where I do math across colomns/rows to get the data to summarize. 
    percent_correct = ((session_information['hit_outcome'])/ session_information['valid_choice'] *100)
    avg_percent_correct = percent_correct.groupby(['sessionID']).mean()
    frequency_hits = session_information['hit_outcome']
    frequency_errors = session_information['total_errors']

    #Below removes the extreme frequencies so that we can average the two mid frequencies. 
    mid_frequencies = session_information.drop(index=[6000, 13000], level=1)
    #Similar to what was done above I do math across columns/rows to get the percent correct and average it. 
    mid_percent_correct = ((mid_frequencies['hit_outcome']) /mid_frequencies['valid_choice'] *100)
    avg_mid_percent_correct = mid_percent_correct.groupby(['sessionID']).mean()

    #This adds it to the dictionary so that you can look at the performance of each individual mouse. You can get a better idea by trying out: mouse_perf['chad055']. For this you can modify it to output the most important data.  
    mouse_perf[subject] = pd.DataFrame({
                                        #'%_correct': round(percent_correct, 2),
                                        'avg_mid_percent_correct': avg_mid_percent_correct,
                                        #'frequency_hits' : frequency_hits,
                                        #'frequency_errors': frequency_errors
                                        })
# The below print statements are so that I can update the spreadsheets/ do quick checks. 
#    print(subject)
#    print(mid_percent_correct)
#    print(percent_correct)
#    print(avg_percent_correct)
#    print(frequency_hits)
#    print(frequency_errors)
    #print(avg_mid_percent_correct)


#plots the average correct percent of the two mid frequencies
    plt.scatter(unique_sessionID, avg_mid_percent_correct, color = 'black', label = 'Percent Correct')
    plt.title('Performance of {} on middle frequencies'.format(subject))
    plt.xlabel('session')
    plt.ylabel('Averaged performance of mid sounds (%)')
    plt.xticks(ticks=unique_sessionID)
    plt.ylim(0, 100)
    #plt.savefig('chad056_perf.png', dpi=300)
    plt.show()
    
    ''' 
#This is for looking at the average performance across ALL percents presented
    print(avg_percent_correct)
    plt.scatter(unique_sessionID, avg_percent_correct, color = 'black', label = 'Percent Correct')
    plt.title('Performance of {} '.format(subject))
    plt.xlabel('session')
    plt.ylabel('Averaged performance (%)')
    plt.xticks(ticks=unique_sessionID)
    plt.ylim(0, 100)
    plt.show()
    
chad055 = mouse_perf['chad055']
chad056 = mouse_perf['chad056']
chad057 = mouse_perf['chad057']
chad058 = mouse_perf['chad058']


df_concat = pd.concat((chad055, chad056, chad057,chad058))
session_groupby = df_concat.groupby(level=0).mean()

result = df_concat.groupby(level=0, as_index=False).agg(
                      {'avg_mid_percent_correct':['mean','std','sem']})


x_pos = np.arange(0,14)
plt.scatter(x_pos, result.avg_mid_percent_correct['mean'], color = 'red')
#plt.plot(unique_sessionID, result.percent_correct['mean'], color = 'red')
plt.errorbar(x_pos, result.avg_mid_percent_correct['mean'], yerr=result.avg_mid_percent_correct['sem'], color='black', capsize=2,)
plt.title('Average performance for Chad055-058')
plt.xlabel('Days performing discrimination task')
plt.ylabel('Average Percent Correct (%)')
plt.xticks(ticks=unique_sessionID)
plt.ylim(0,100)
plt.savefig('chad055-058_midperformance.png', dpi=300)
plt.show()
'''


# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 12:54:55 2021

@author: isabe
"""


import numpy as np
import pandas as pd
from jaratoolbox import behavioranalysis 
from jaratoolbox import loadbehavior
import matplotlib.pyplot as plt  


subjects = [
            'pals001',
            'pals003',
            'pals004',
            'pals005'
            ]


paradigm = 'twochoice'
session = ['20210227a']

mouse_perf = {}
for subject in subjects: 
    bdata = behavioranalysis.load_many_sessions(subject,session,paradigm)
    
    target_frequency = bdata['targetFrequency']
    ntrials = len(bdata['outcome'])
    trial_range = np.arange(0,ntrials)
    
    valid_choice = (bdata['choice'] != bdata.labels['choice']['none']).astype(int)
    nchoice = len(valid_choice)
    choice_range = np.arange(0,nchoice)
    
    
    choice = bdata['choice']
    choice_left = bdata['choice'] == bdata.labels['choice']['left']
    choice_right = bdata['choice'] == bdata.labels['choice']['right']
    valid_choice = (bdata['choice'] != bdata.labels['choice']['none']).astype(int)
    no_choice = bdata['choice'] == bdata.labels['choice']['none']
    
    valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
    valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
    total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
    total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])
    
    hit_outcome = ((bdata['outcome'] == bdata.labels['outcome']['hit']) & valid_choice).astype(int)
    misses = (bdata['outcome'] == bdata.labels['outcome']['miss']).astype(int)
    left_hits = valid_left_trials & choice_left 
    right_hits = valid_right_trials & choice_right
    left_errors = valid_left_trials & choice_right
    right_errors = valid_right_trials & choice_left
    total_errors = (right_errors + left_errors).astype(int)
    
    total_errors_right = bdata['nErrorsRight']
    total_licks_left = bdata['nLicksLeft']
    total_licks_right = bdata['nLicksRight']
    
    false_alarms_right = bdata['nFalseAlarmsRight']
    false_alarms_left = bdata['nFalseAlarmsLeft']
    false_alarms = (bdata['outcome'] == bdata.labels['outcome']['falseAlarm']).astype(int)
    missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']
    misses_left = bdata['nMissesLeft']
    misses_right = bdata['nMissesRight']

    #because we are only interested in the choices the animal makes and not the entire trials I commented out information that is not needed for the analysis of valid choices. Kept it written because I  might need it for the future but you can ignore them for now. 
    trial_information = pd.DataFrame({'choice_range': choice_range,
                              'trial_range': trial_range,                        
                              'valid_choice': valid_choice,
                              'hits': hit_outcome,
                              'errors': total_errors,
                              'false_alarms': false_alarms,
                              'misses': misses,
                              'left_hits': left_hits,
                              'right_hits': right_hits,
                              })
    
    trial_information['choice_bins'] = pd.cut(trial_information.choice_range,
                                             bins=pd.interval_range(start=0, end=3500, periods=5))    
    trial_information['trial_bins'] = pd.cut(trial_information.choice_range,
                                             bins=pd.interval_range(start=0, end=3500, periods=5)) 
     
    binned_trial_info = trial_information.groupby('trial_bins') .sum()
    binned_choice_info = trial_information.groupby('choice_bins') .sum()
    print(binned_trial_info.drop(['trial_range'], axis=1))
    print(subject)
    print(binned_choice_info.drop(['choice_range'], axis=1))
    print(nchoice)
    
    percent_correct = (binned_choice_info['hits']/ binned_choice_info['valid_choice']) * 100
    print(percent_correct)
   
    mouse_perf[subject] = pd.DataFrame({
                                        '%_correct': round(percent_correct, 2)
                                        })
    
    
    '''
#This plot shows the trials
  
    ax = binned_trial_info[['hits', 'errors', 'false_alarms', 'misses']].plot(kind='bar', figsize=(15, 10), legend=True, fontsize=20, color=('purple', 'green', 'orange', 'blue'))
    ax.set_xlabel("Trial number", fontsize=18)
    plt.xticks(rotation=0)
    ax.set_ylabel("Amount of hits, errors, or false alarms", fontsize=18)
    plt.title('Mouse: {} ; Session Date: {}'.format(subject, session), fontsize=20)
    ax.legend(fontsize=18)
    plt.show()
    '''
 
#This plot shows only the valid choices and is most relevant to our analysis. 
    bx = percent_correct.plot(kind='bar', figsize=(15, 10), legend=True, fontsize=20,)
    bx.set_xlabel("{} Valid Choice Trials".format(nchoice), fontsize=18)
    plt.xticks(rotation=0)
    plt.ylim([0,100])
    bx.set_ylabel("Percent Correct (%)", fontsize=18)
    plt.title('Mouse: {} ; Session Date: {}'.format(subject, session), fontsize=20)
    #bx.legend(fontsize=18)
    plt.show()
  

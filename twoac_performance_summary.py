# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:33:08 2020

This is for creating summary stats. 

@author: isabe
"""

import numpy as np
import pandas as pd
from jaratoolbox import loadbehavior
#from jaratoolbox import extraplots
import numpy as np
import matplotlib.pyplot as plt 
#from statsmodels.stats.proportion import proportion_confint
#import sys
from jaratoolbox import behavioranalysis 
#from jaratoolbox import settings 
from collections import Counter as cntr
#from scipy.stats import norm
from datetime import datetime

#Add the dates you want to look at. 
subject = 'chad039'
#subject = 'chad042'
#subject = 'chad043'
#subject = 'chad044'
paradigm = 'twochoice'
#sessions = ['20200926a', '20200928a', '20200929a', '20201001a', '20201003a', '20201005a','20201006a' ,'20201007a', '20201008a', '20201009a', '20201010a']

#the sessions below are the dates that the animal discriminated AM sounds the first time
#sessions = ['20200808aii', '20200810aii','20200811aii', '20200813a', '20200814a', '20200904a', '20200905a',
#            '20200906a', '20200908a', '20200909a', '20200910a']

#the sessions below are the dates that the animal discriminated AM sounds the second time
#sessions =[ '20201012a', '20201013a', '20201014a', '20201015a', '20201019a', '20201020a', '20201021a', '20201022a', '20201023a',
#           '20201025a', '20201026a', '20201027a', '20201028a', '20201029a', '20201030a', '20201031a', '20201102a', '20201103a', '20201104a',
#           '20201105a', '20201106a', '20201108a', '20201109a', '20201110a', '20201111a']

#the sessions below are the dates the animal was reintroduced to the frequency discrimination task. This was done to see if the animal still knew how to perform the task. 
sessions = ['20200914a', '20200915a', '20200916a', '20200918a', '20200920a', '20200922a', '20200923a', '20200925a', '20200926a', 
            '20200926a', '20200928a', '20200929a', '20201001a', '20201003a', '20201005a','20201006a' ,'20201007a', '20201008a',
            '20201009a','20201010a']

#The sessions below are the dates the animal was discriminating AM vs chords. 
#sessions = ['20201114a', '20201115a', '20201116a', '20201117a', '20201118a', '20201119a'] 

bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)

sessionID = bdata['sessionID'] 
unique_sessionID = np.unique(sessionID) + 1
reward_side_mode = bdata['rewardSideMode']
repeat_mistake = bdata['rewardSideMode'] == bdata.labels['rewardSideMode']['repeat_mistake']
random_mode = bdata['rewardSideMode'] == bdata.labels['rewardSideMode']['repeat_mistake']

choice = bdata['choice']
choice_left = bdata['choice'] == bdata.labels['choice']['left']
choice_right = bdata['choice'] == bdata.labels['choice']['right']
valid_choice = bdata['choice'] != bdata.labels['choice']['none']
no_choice = bdata['choice'] == bdata.labels['choice']['none']
hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']
missed_outcomes = bdata['outcome'] == bdata.labels['outcome']['miss']

valid_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left']) & valid_choice
valid_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right']) & valid_choice
total_left_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['left'])
total_right_trials = (bdata['rewardSide'] == bdata.labels['rewardSide']['right'])
left_hits = valid_left_trials & choice_left 
right_hits = valid_right_trials & choice_right
left_errors = valid_left_trials & choice_right
right_errors = valid_right_trials & choice_left
total_errors = right_errors + left_errors

df_trial_information = pd.DataFrame({'sessionID': sessionID,
                                     'reward_side_mode' : reward_side_mode,
                                     'repeat_mistake': repeat_mistake,
                                     'hit_outcome': hit_outcome,
                                     'right_hits': right_hits,
                                     'left_hits': left_hits,
                                     'right_errors': right_errors,
                                     'left_errors': left_errors,
                                     'total_errors': total_errors,
                                     'left_choice': choice_left,
                                     'right_choice': choice_right,
                                     'valid_left_trials': valid_left_trials,
                                     'valid_right_trials': valid_right_trials,
                                     'valid_choice': valid_choice,
                                     'targetAMdepth': bdata['targetAMdepth'],
                                     'rewardside': bdata['rewardSide'],
                                     'total_left_trials': total_left_trials,
                                     'total_right_trials': total_right_trials
                                     })


df_session_information = df_trial_information.groupby(by = ['sessionID']) .sum()

#This line shows why we cant use the total number of trials to look at our outcome, since we don't force the mice to make a choice there are a lot of trials that they simply do not respond.
#all_trials_performance = ((df_session_information['hit_outcome']) /df_session_information['total_trials'] *100)

percent_correct = ((df_session_information['hit_outcome']) /df_session_information['valid_choice'] *100)
left_performance = ((df_session_information['left_hits'] / df_session_information['valid_left_trials']) *100)
right_performance = ((df_session_information['right_hits'] / df_session_information['valid_right_trials']) *100)
mean_side_performance = ((left_performance + right_performance)/ 2 )
df_overall_performance = pd.DataFrame({'percent_correct': percent_correct,
                                       'left_performance': left_performance,
                                       'right_performance': right_performance,
                                       'mean_side_performance' : mean_side_performance,
                                       #'all_trials_performance': all_trials_performance
                                       })

print(subject)
print(df_session_information[['left_hits', 'valid_left_trials', 'right_hits', 'valid_right_trials']])
print(df_overall_performance[['left_performance', 'right_performance', 'percent_correct']])

df_id_reward_mode = pd.DataFrame({'sessionID': sessionID,
                                     'reward_side_mode' : reward_side_mode,
                                     'repeat_mistake': repeat_mistake,
                                     'random_mode': random_mode
                                     })

print(df_id_reward_mode.groupby(['sessionID', 'reward_side_mode']).size())



'''
#plots the percent correct in each session
plt.scatter(unique_sessionID, percent_correct, color = 'black', label = 'only choice trials')
#plt.scatter(unique_sessionID, all_trials_performance, color = 'orange', label = 'including missed trials')
plt.title(subject + ' Performance')
plt.xlabel('session')
plt.ylabel('Percent correct in each session (%)')
#plt.legend(loc=0)
plt.xticks(ticks=unique_sessionID)
plt.ylim(0, 100)
plt.show(range(0,20)) 

'''

#plots the percent animal chose the left in each session
plt.scatter(unique_sessionID, left_performance, color = 'blue', label = 'Left')
plt.plot(unique_sessionID, left_performance, color = 'blue')
plt.scatter(unique_sessionID, right_performance, color = 'red' , label = 'Right')
plt.plot(unique_sessionID, right_performance, color = 'red')
plt.scatter(unique_sessionID, percent_correct, color = 'black', label = 'Percent Correct')
plt.title(subject + 'Performance')
plt.xlabel('session')
plt.ylabel('Percent animal correctly chose left/Right (%)')
plt.legend(loc = 3)
plt.xticks(ticks=unique_sessionID)
plt.ylim(0, 100)
plt.show() 

#plots the performance. Numbers are so low becuase it includes all trials, including missed trials
#plt.scatter(unique_sessionID, overall_performance, color = 'orange')
#plt.title(subject + ' Performance')
#plt.xlabel('session')
#plt.ylabel('Percent correct in each session (%)')
#plt.ylim(0, 100)
#plt.show() 


#plots the percent chose the right in each session
#plt.scatter(unique_sessionID, right_performance, color = 'r')
#plt.title(subject + ' Performance right')
#plt.xlabel('session')
#plt.ylabel('Percent animal correctly chose right (%)')
#plt.ylim(0, 100)
#plt.show() 



'''

#DON'T DELETE ANYTHING BELOW THIS, ONLY COPY AND PASTE! This is literally the one think I am sure about
#This code summarizes the performance of a mouse, but you can only see one session at a time. 

# Don't mess with anything under this (you finally have the summary down. )
subject = 'chad039'
#subject = 'chad042'
#subject = 'chad043'
#subject = 'chad044'
session = '20200915a'
#session = '20200814a'
paradigm = 'twochoice'
behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)

licks_left = bdata['nLicksLeft']
licks_right = bdata['nLicksRight']
total_hits_left = bdata['nHitsLeft']
total_hits_right = bdata['nHitsRight']
#per_response_left = (licks_left/ (licks_right+ licks_left) * 100)
#per_response_right = (licks_right/ (licks_left + licks_right) * 100)
choice = bdata['choice'] 
choice_left = bdata['choice'] == bdata.labels['choice']['left']
valid_choice = choice != bdata.labels['choice']['none']
no_choice = choice =bdata.labels['choice']['none']
hit_outcome = bdata['outcome'] == bdata.labels['outcome']['hit']

left_trials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
right_trials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']

total_left_trials = left_trials.sum()
total_right_trials = right_trials.sum()

percent_correct_left = (total_hits_left[-1] / total_left_trials) * 100 
percent_correct_right = (total_hits_right[-1] / total_right_trials) *100


percent_correct_choices = ((hit_outcome.sum())/ (valid_choice.sum()) * 100)
print('Percent correct responses: ({:0.1f}%)'.format(percent_correct_choices))
#print(percent_correct_choices)

numerator_l = np.sum((bdata['outcome']==bdata.labels['outcome']['hit']) & (bdata['choice']==bdata.labels['choice']['left']))
denominator_l = np.sum((bdata['rewardSide']==bdata.labels['rewardSide']['left']) & ~(bdata['choice'] == bdata.labels['choice']['none']))
percent_correct_response_l = 100 * numerator_l/denominator_l
print('Percent correct response to the left: ({:0.1f}%)'.format(100 * numerator_l/denominator_l))
#print(100 * numerator_l/denominator_l)

numerator_r = np.sum((bdata['outcome']==bdata.labels['outcome']['hit']) & (bdata['choice']==bdata.labels['choice']['right']))
denominator_r = np.sum((bdata['rewardSide']==bdata.labels['rewardSide']['right']) & ~(bdata['choice'] == bdata.labels['choice']['none']))
percent_correct_response_r = 100 * numerator_r/denominator_r
print('Percent correct response to the right: ({:0.1f}%)'.format(100 * numerator_r/denominator_r))
#print(100 * numerator_r/denominator_r)
'''
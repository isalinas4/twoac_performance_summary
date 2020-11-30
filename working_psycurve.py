# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 18:16:00 2020

@author: isabe
"""


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 
from jaratoolbox import behavioranalysis 



#subject = 'chad039'
paradigm = 'twochoice'
#sessions = ['20200803a', '20200804a', '20200805a', '20200806a']

#subject = 'chad042'
#paradigm = 'twochoice'
#sessions = ['20200712a', '20200713a', '20200715a']

#subject = 'chad043'
#paradigm = 'twochoice'
#sessions = ['20201005a', '20201006a']

subject = 'chad044'
#paradigm = 'twochoice'
sessions = ['20200718a', '20200722a']

bdata = behavioranalysis.load_many_sessions(subject,sessions,paradigm)


#setting up the variables
sessionID = bdata['sessionID']
unique_sessionID = np.unique(sessionID) + 1


target_frequency = bdata['targetFrequency']
frequency_presented = np.unique(target_frequency)
response = bdata['choice']
valid_choice = response != bdata.labels['choice']['none']
response_right = response==bdata.labels['choice']['right']
response_left = response==bdata.labels['choice']['left']
no_response = response==bdata.labels['choice']['none']


#this makes a table that has all the trials and the information/ responses for each 
df_each_trial = pd.DataFrame({'target_frequency': target_frequency,
                              'sessionID' : sessionID,
                              'response_right': response_right,
                              'response_left': response_left,
                              'valid_choice': valid_choice,
                              'response': response,
                              'no_response': no_response
                              })

group_session_frequency = df_each_trial.groupby(['sessionID','target_frequency']).sum() #sum function
percent_right = ((group_session_frequency['response_right']) / (group_session_frequency['valid_choice']) * 100)
mean_percent_by_session = percent_right.groupby(['target_frequency']).mean()


#plotting the figure
fig1, ax1 = plt.subplots()
ax1.plot(frequency_presented, mean_percent_by_session)
ax1.set_xscale('log')
ax1.set_xticks([6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_ylim([0, 100])
ax1.set_xlabel('Frequency Presented (Hz)')
ax1.set_ylabel('Percent Response Right (%)')
ax1.set_title('{} performance across multiple sessions' .format(subject))
ax1.scatter(frequency_presented, mean_percent_by_session, color = 'r') 


#Below is for individual day psycurves 
'''
session = '20201005a'
behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)


#Below is to give me the psycurve 


#setting up the variables
target_frequency = bdata['targetFrequency']
frequency_presented = np.unique(target_frequency)
response = bdata['choice']
valid_choice = response != bdata.labels['choice']['none']
response_right = response==bdata.labels['choice']['right']
response_left = response==bdata.labels['choice']['left']
no_response = response==bdata.labels['choice']['none']


#this makes a table that has all the trials and the information/ responses for each 
df_each_trial = pd.DataFrame({'target_frequency': target_frequency,
                   'response_right': response_right,
                   'response_left': response_left,
                   'valid_choice': valid_choice,
                   'response': response,
                   'no_response': no_response}, columns=['target_frequency', 'valid_choice', 'response_right', ' response_left', 'no_response'])

df_by_frequency = df_each_trial.groupby(by = ['target_frequency']) .sum()

df_prcnt_right_response = ((df_by_frequency['response_right']) / (df_by_frequency['valid_choice']) * 100)

                                     


#sepparating out responses to each frequency
mean_response_right = df_by_frequency[('response_right')] 

#plotting the figure
fig1, ax1 = plt.subplots()
ax1.plot(frequency_presented, df_prcnt_right_response)
ax1.set_xscale('log')
ax1.set_xticks([6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_ylim([0, 100])
ax1.set_xlabel('Frequency Presented (Hz)')
ax1.set_ylabel('Percent Response Right (%)')
ax1.set_title('{} Session date: {}' .format(subject, session))
ax1.scatter(frequency_presented, df_prcnt_right_response, color = 'r') 
'''
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from constants import *
from util import splitByMajor


"""
Preprocess mentee data.
Read into dataframe.
One-hot encode activity preferences.
Convert other categorical reponses to numerical.

Parameters
--------------------
    filename          -- string, path to mentee response csv

Returns
--------------------
    mentee_tables     -- dict, major_category_# -> corresponding split df
"""
def preprocess_mentee_responses(filename):
  originalMenteeData = pd.read_csv(filename)
  menteeData = originalMenteeData.copy()

  n_menteeEntries = menteeData.shape[0]

  menteeEmails = "Username"
  zeroArray = np.zeros(n_menteeEntries)
  for i in range (0, len(categoryChoices['Activities'])):
     menteeData[(categoryChoices.get('Activities'))[i]] = zeroArray

  for i in range (0, n_menteeEntries):
     for j in range (0, len(categoryChoices['ActivitiesRank'])):
         activity = menteeData.iloc[i][(categoryChoices.get('ActivitiesRank'))[j]]
         email = menteeData.iloc[i]['Username']
         menteeData.loc[menteeData['Username']==email, activity]=5-j

  for i in range (1, len(categoryChoices['FridaysResponse']) + 1):
     menteeData.loc[menteeData[categoryChoices['FridaysQuestion']].astype('str')==categoryChoices.get('FridaysResponse')[i-1], categoryChoices['FridaysQuestion']] = i

  menteeData.loc[menteeData[categoryChoices['MenteeTypeQuestion']].astype('str') ==categoryChoices.get('MentorTypeResponse')[0], categoryChoices['MenteeTypeQuestion']] = 0
  menteeData.loc[menteeData[categoryChoices['MenteeTypeQuestion']].astype('str') ==categoryChoices.get('MentorTypeResponse')[1], categoryChoices['MenteeTypeQuestion']] = 1

  for i in range (1, len(categoryChoices['Majors']) + 1):
      menteeData.loc[menteeData[categoryChoices['MajorsQuestion']].astype('str')==categoryChoices.get('Majors')[i-1], categoryChoices['MajorsQuestion']] = majorToNums[categoryChoices.get('Majors')[i-1]]

  for i in range(0, len(categoryChoices['TimeZones'])):
      if abs(i-15)<=abs(len(categoryChoices['TimeZones'])+i-15):
          timeZoneAsNum = i-15
      else:
          timeZoneAsNum = len(categoryChoices['TimeZones'])+i-15
      menteeData.loc[menteeData[categoryChoices['MenteeTimeZoneQuestion']].astype('str')==categoryChoices.get('TimeZones')[i], categoryChoices['MenteeTimeZoneQuestion']] = timeZoneAsNum

  menteeData.loc[menteeData[categoryChoices['MenteeTransferQuestion']].astype('str')==categoryChoices.get('TransferResponse')[0], categoryChoices['TransferQuestion']] = 0
  menteeData.loc[menteeData[categoryChoices['MenteeTransferQuestion']].astype('str')==categoryChoices.get('TransferResponse')[1], categoryChoices['TransferQuestion']] = 1

  for i in range (0, len(categoryChoices['Mentorship'])):
     menteeData[categoryChoices['Mentorship'][i]] = zeroArray

  for i in range (0, n_menteeEntries):
     for j in range (0, len(categoryChoices['Mentorship'])):
         menteeships = menteeData.iloc[i][categoryChoices['MenteeshipQuestion']]
         email = menteeData.iloc[i]['Username']
         menteeData.loc[(menteeData['Username']==email) & (menteeships.find(categoryChoices['Mentorship'][j])) != -1, categoryChoices['Mentorship'][j]] = 1
  
  return splitByMajor(menteeData)

"""
Preprocess mentee master data.
Read into dataframe.
Encode majors.

Parameters
--------------------
    filename          -- string, path to mentee master csv

Returns
--------------------
    mentee_master_tables     -- dict, major_category_# -> list of emails
"""
def preprocess_mentee_masterlist(filename):
  menteeData = pd.read_csv(filename)
  n_menteeEntries = menteeData.shape[0]
  
  for major in master_major_map:
    menteeData.loc[menteeData['Admit Major'].astype('str')==major, 'Admit Major'] = majorToNums[master_major_map[major]]
    
  mentee_master_tables=dict()
  for i in range(1,num_major_categories+1):
    mentee_master_tables[i]=menteeData.loc[menteeData['Admit Major']==i,'Email'].to_list()
    
  return mentee_master_tables


"""
Cluster mentees into groups to establish representative mentees.

Parameters
--------------------
    menteeData             -- pandas df, parsed mentee data
    num_clusters           -- int, number of clusters (should equal number of mentors)

Returns
--------------------
    familyToMentees       -- dict, representative_mentee# -> [mentee emails]
    menteeClusterData     -- dict, representative_mentee# -> [arrays of numerical mentee data] (these correspond to the data used to cluster)
"""
def cluster_mentees(menteeData, num_clusters):
  # menteeKM is a copy of menteeData
  menteeKM = menteeData.copy()

  # menteeNewData is what KMeans will be applied to
  menteeNewData = menteeKM[menteeMatchCols]

  menteeKmeans = KMeans(n_clusters=num_clusters, n_init=500)
  menteeKmeans = menteeKmeans.fit(menteeNewData)
  menteeLabels = menteeKmeans.predict(menteeNewData)

  familyToMentees = dict()
  menteeClusterData = dict()

  for i in range(0, len(menteeLabels)):
      if menteeLabels[i] in familyToMentees:
          familyToMentees[menteeLabels[i]].append(menteeKM.iloc[i]['Username'])
          menteeClusterData[menteeLabels[i]].append(menteeKM.iloc[i][menteeMatchCols])
      else:
          newList = [menteeKM.iloc[i]['Username']]
          newData = [menteeKM.iloc[i][menteeMatchCols]]
          familyToMentees.update( { menteeLabels[i] : newList })
          menteeClusterData.update( { menteeLabels[i] : newData})
          
  return familyToMentees, menteeClusterData
  
if __name__ == '__main__':
  menteeData=preprocess_mentors("2020-21 MentorSEAS Mentee Form.csv")
  print(menteeData)
  preprocess_mentee_masterlist("New-Transfers.csv")
  



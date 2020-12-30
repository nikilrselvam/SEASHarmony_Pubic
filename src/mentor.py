import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
from constants import *
from family_requests import *
from util import splitByMajor

"""
Preprocess mentor data.
Read into dataframe.
One-hot encode activity preferences.
Convert other categorical reponses to numerical.

Parameters
--------------------
    filename          -- string, path to mentor csv

Returns
--------------------
    mentorData        -- pandas df, parsed mentor data
"""
def preprocess_mentors(filename):
  originalMentorData = pd.read_csv(filename)
  mentorData = originalMentorData.copy()

  n_mentorEntries = mentorData.shape[0]

  mentorFamilyQuestion = 'Follow the instructions below to join a family'
  for i in range (0, n_mentorEntries):
      family = mentorData.iloc[i][mentorFamilyQuestion]


  zeroArray = np.zeros(n_mentorEntries)
  for i in range (0, len(categoryChoices['Activities'])):
      mentorData[(categoryChoices.get('Activities'))[i]] = zeroArray

  for i in range (0, n_mentorEntries):
      for j in range (0, len(categoryChoices['ActivitiesRank'])):
          activity = mentorData.iloc[i][(categoryChoices.get('ActivitiesRank'))[j]]
          email = mentorData.iloc[i]['Username']
          mentorData.loc[mentorData['Username']==email, activity]=5-j

  for i in range (1, len(categoryChoices['FridaysResponse']) + 1):
      mentorData.loc[mentorData[categoryChoices['FridaysQuestion']].astype('str')==categoryChoices.get('FridaysResponse')[i-1], categoryChoices['FridaysQuestion']] = i

  mentorData.loc[mentorData[categoryChoices['MentorTypeQuestion']].astype('str') ==categoryChoices.get('MentorTypeResponse')[0], categoryChoices['MentorTypeQuestion']] = 0
  mentorData.loc[mentorData[categoryChoices['MentorTypeQuestion']].astype('str') ==categoryChoices.get('MentorTypeResponse')[1], categoryChoices['MentorTypeQuestion']] = 1

  for i in range (1, len(categoryChoices['Majors']) + 1):
      mentorData.loc[mentorData[categoryChoices['MajorsQuestion']].astype('str')==categoryChoices.get('Majors')[i-1], categoryChoices['MajorsQuestion']] = majorToNums[categoryChoices.get('Majors')[i-1]]

  mentorData.loc[mentorData[categoryChoices['TransferQuestion']].astype('str')==categoryChoices.get('TransferResponse')[0], categoryChoices['TransferQuestion']] = 0
  mentorData.loc[mentorData[categoryChoices['TransferQuestion']].astype('str')==categoryChoices.get('TransferResponse')[1], categoryChoices['TransferQuestion']] = 1

  for i in range (0, len(categoryChoices['Mentorship'])):
      mentorData[categoryChoices['Mentorship'][i]] = zeroArray

  mentorData[categoryChoices['MentorshipQuestion']] = mentorData[categoryChoices['MentorshipQuestion']].fillna("")

  for i in range (0, n_mentorEntries):
      # mentorships finds the specific areas that a given mentor can offer mentorship in
      mentorships = mentorData.iloc[i][categoryChoices['MentorshipQuestion']]
      mentorships = mentorships.split(';')
      email = mentorData.iloc[i]['Username']
      for j in range (0, len(mentorships)):
          mentorData.loc[mentorData['Username']==email, categoryChoices['Mentorship'][j]] = 1

  return mentorData
  

"""
Cluster mentors into families with given cluster size constraint.
If the number of mentors is not a multiple of cluster size, at most one returned family has an imperfect size of num_mentors%cluster_size.

Parameters
--------------------
    mentorData           -- pandas df, mentor data
    mentorMatchCols      -- list, columns (names) relevant for clustering
    cluster_size         -- int, desired size of clusters
    familyToMentors      -- dictionary to be updated with new family to email pairings

Returns
--------------------
    None (note, however, that the familyToMentors dictionary is modified to include new pairings)
"""

def constrained_cluster_mentors(mentorData, mentorMatchCols, cluster_size, familyToMentors):

  # mentorNewData is what KMeans will be applied to
  mentorNewData = mentorData[mentorMatchCols].copy()
  num_mentors = len(mentorData)

  start_family_num=len(familyToMentors)

  # base case
  if num_mentors<2*cluster_size:
    for i in range(num_mentors):
      family_num=i//cluster_size+start_family_num
      if family_num in familyToMentors:
        familyToMentors[family_num].append(mentorData.iloc[i]['Username'])
      else:
        newList = [mentorData.iloc[i]['Username']]
        familyToMentors.update( { family_num : newList })

    return

  kmeans = KMeans(n_clusters=int(num_mentors/cluster_size), n_init=500)
  kmeans = kmeans.fit(mentorNewData)
  labels = kmeans.predict(mentorNewData)
  centroids = kmeans.cluster_centers_

  label_count=defaultdict(int)
  for label in labels:
    label_count[label]+=1

  # dict: size of family -> number of families (useful to check performance)
  family_size=defaultdict(int)
  for label in label_count:
    family_size[label_count[label]]+=1

#  print(family_size)

  perfect_mentors=set() #mentors who belong to perfect families (multiples of cluster size)
  for i in range(len(labels)):
    if label_count[labels[i]]%cluster_size==0:
      perfect_mentors.add(i)

  perfect_mentor_indices=[]
  for mentor in perfect_mentors:
    perfect_mentor_indices.append( (mentorData[mentorData['Username'] == mentorData.iloc[mentor]['Username']].index.values)[0])

  label_to_family_num=[None for i in range(len(labels))]

  for mentor in perfect_mentors:
    family_num=label_to_family_num[labels[mentor]]
    if family_num==None:
      family_num=len(familyToMentors)
      label_to_family_num[labels[mentor]]=family_num
      newList = [mentorData.iloc[mentor]['Username']]
      familyToMentors.update( { family_num : newList })
    else:
      familyToMentors[family_num].append(mentorData.iloc[mentor]['Username'])

  # chop up families which are bigger multiples of cluster size
  for i in range(len(familyToMentors)-start_family_num):
    family_num=start_family_num+i;
    family=familyToMentors[family_num]
    if len(family)>cluster_size:
      for i in range(len(family)//cluster_size):
        if i==0:
          continue
        new_family_num=len(familyToMentors)
        newList = family[i*cluster_size:(i+1)*cluster_size]
        familyToMentors.update( { new_family_num : newList })
      newList=family[:cluster_size]
      familyToMentors.update( { family_num : newList })

  scraped_mentor_indices=[]
  # scrape families from imperfect clusters
  for i in range(len(labels)):
    if label_count[labels[i]]%cluster_size!=0 and label_count[labels[i]]>cluster_size:
      family_num=label_to_family_num[labels[i]]
      if family_num==None:
        family_num=len(familyToMentors)
        label_to_family_num[labels[i]]=family_num
        newList = [mentorData.iloc[i]['Username']]
        familyToMentors.update( { family_num : newList })
        scraped_mentor_indices.append((mentorData[mentorData['Username'] == mentorData.iloc[i]['Username']].index.values)[0])
      else:
        if len(familyToMentors[family_num])<cluster_size:
          familyToMentors[family_num].append(mentorData.iloc[i]['Username'])
          scraped_mentor_indices.append((mentorData[mentorData['Username'] == mentorData.iloc[i]['Username']].index.values)[0])

  # remove the mentors who have now been assigned families
  mentorData = mentorData.drop(perfect_mentor_indices)
  mentorData = mentorData.drop(scraped_mentor_indices)

  #recurse on the remaining mentors
  constrained_cluster_mentors(mentorData, mentorMatchCols, cluster_size, familyToMentors)


"""
Cluster mentors into families.

Parameters
--------------------
    mentorData         -- pandas df, parsed mentor data

Returns
--------------------
    familyToMentors    -- dict, family# -> [mentor emails]
    mentor_tables      -- dict, major_category_# -> corresponding split df
"""
def cluster_mentors(mentorData):

  n_mentorEntries = mentorData.shape[0]
  
  # mentorKM is a copy of mentorData
  mentorKM = mentorData.copy()

  # preferredFamilyToMentors is a dictionary mapping family string to members' emails for people with 3-person families
  preferredFamilyToMentors = dict()

  # removeMentors is a list of indexes of people (in mentorKM dataframe) that will need to be removed from mentorKM before performing KMeans
  removeMentors = []

  # twoMentorFams is a dictionary mapping family string to members' emails for people with 2-person families
  twoMentorFams = dict()

  # for people who didn't put down families, fill their mentorFamilyQuestion column with empty string
  mentorFamilyQuestion = 'Follow the instructions below to join a family'
  mentorKM[mentorFamilyQuestion] = mentorKM[mentorFamilyQuestion].fillna("")

  # get inconsistent families to ignore
  inconsistent_emails, _ = get_inconsistencies(write_to_file=False, preferred_email=False)
  inconsistent_emails=set(inconsistent_emails)

  # figure out the family string, and continue adding key-value pairs between family string and members' email to preferredFamilyToMentors and twoMentorFams
  for i in range (0, n_mentorEntries):
      if mentorKM.iloc[i]['Username'] in inconsistent_emails:
        continue
      familyString = mentorKM.iloc[i][mentorFamilyQuestion]
      familyString=standardize_family_string(familyString)
      splitFamString = familyString
      if (familyString != ""):
          splitFamString = splitFamString.split('-')
          if (len(splitFamString) == 3):
              if familyString in preferredFamilyToMentors:
                  preferredFamilyToMentors[familyString].append(mentorKM.iloc[i]['Username'])
              else:
                  newList = [mentorKM.iloc[i]['Username']]
                  preferredFamilyToMentors.update( { familyString : newList } )
              indexToErase = mentorKM[mentorKM['Username'] == mentorKM.iloc[i]['Username']].index.values
              removeMentors.append(indexToErase[0])
          elif (len(splitFamString) == 2):
              if familyString in twoMentorFams:
                  twoMentorFams[familyString].append(mentorKM.iloc[i]['Username'])
              else:
                  newList1 = [mentorKM.iloc[i]['Username']]
                  twoMentorFams.update( { familyString : newList1 })



  mentorKMData = []

  for i in range(0, n_mentorEntries):
      mentorKMData.append(mentorData.iloc[i][mentorMatchCols])

  # if family name is only 2 people, alter the data in mentorKM so that both people have the exact same data, meaning they are guaranteed to get matched through KMeans
  for key in twoMentorFams:
      mentor1 = twoMentorFams[key][0]
      mentor2 = twoMentorFams[key][1]
      for i in range (0, len(mentorMatchCols)):
          mentorKM.loc[mentorKM['Username']==mentor2,mentorMatchCols] = mentorKM.loc[mentorKM['Username']==mentor1, mentorMatchCols].values
  # delete all the 3-family mentors from mentorKM so KMeans is only applied for 2-fam or 0-fam mentors
  mentorKM = mentorKM.drop(removeMentors)
  mentorRecursiveKM=mentorKM.copy()
  num_mentors = len(mentorKM)

  familyToMentors = dict()
  constrained_cluster_mentors(mentorRecursiveKM, mentorMatchCols,3, familyToMentors)
#  print(familyToMentors)

  for key in preferredFamilyToMentors:
      familyToMentors[len(familyToMentors)] = preferredFamilyToMentors[key]
  
  return familyToMentors, splitByMajor(mentorData)
  
if __name__ == '__main__':
  mentorData=preprocess_mentors("MentorSEAS Mentor Form.csv")
  cluster_mentors(mentorData)



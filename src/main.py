import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from collections import defaultdict
from mentor import *
from mentee import *
from stable_match import *
from export import *


mentorData=preprocess_mentors(mentors_filename)
familyToMentors, mentor_tables = cluster_mentors(mentorData)
num_mentors_in_category=dict()
for category in mentor_tables.keys():
  num_mentors_in_category[category]=mentor_tables[category].shape[0]

mentee_tables=preprocess_mentee_responses(mentee_responses_filename)
mentee_master_tables=preprocess_mentee_masterlist(mentees_master_filename)

mentorEmailToMenteesEmails = defaultdict(list)

for category in mentor_tables.keys():
  
  master_mentee_emails=set(mentee_master_tables[category])
  
  # filter out unmatchable responses
  mentee_tables[category]=mentee_tables[category][mentee_tables[category]['Username'].isin(master_mentee_emails)]
  matched_mentee_emails=set(mentee_tables[category]['Username'].to_list())
  master_mentee_emails=master_mentee_emails.difference(matched_mentee_emails)
  
  # proportion of mentors to be matched
  p=len(matched_mentee_emails)/(len(matched_mentee_emails)+len(master_mentee_emails))
  num_match_mentors=int(p * num_mentors_in_category[category])
  
  familyToMentees, menteeClusterData=cluster_mentees(mentee_tables[category], num_match_mentors)

  # -------------------------------------------
  # -Assign respresentative mentees to mentors-
  # -------------------------------------------

  # mentorNums keeps track of only the numerical values for each mentor in each column
  mentorNums = mentor_tables[category][mentorMatchCols].to_numpy()
  mentorNums = mentorNums[:num_match_mentors]
  
  # repMentees is a matrix of representative mentees for each mentee cluster to be KMeansed with mentors
  representativeMentees = []

  for key in range (0, len(menteeClusterData)):
      representative = np.zeros(len(mentorMatchCols))
      for mentee in menteeClusterData[key]:
          representative = representative + mentee[mentorMatchCols]
      representative /= len(menteeClusterData[key])
      representativeMentees.append(representative)
  representativeMentees = np.array(representativeMentees)


  # Calculate pairwise distance for every pair of mentor and representative mentee

  mentorToPref = dict()
  menteeToPref = dict()

  mentorPrefs = euclidean_distances(mentorNums, representativeMentees)
  menteePrefs = euclidean_distances(representativeMentees, mentorNums)

  # Create the mentor preferences matrix by sorting each row of the pairwise distance matrix
  # Create the mentee preferences matrix in a similar fashion

  for i,mentor in enumerate(mentorPrefs):
    mentorPrefs[i]=sorted(range(mentorPrefs.shape[1]), key=lambda x: mentor[x])
  for i,mentee in enumerate(menteePrefs):
    menteePrefs[i]=sorted(range(menteePrefs.shape[1]), key=lambda x: mentee[x])

  mentorPrefs=np.array(mentorPrefs).astype(int)
  menteePrefs=np.array(menteePrefs).astype(int)

  stableMatchResult = stable_match(num_match_mentors, mentorPrefs, menteePrefs)

  for i in range(0, len(stableMatchResult)):
      menteeEmails = familyToMentees[i]
      mentor = mentor_tables[category].iloc[stableMatchResult[i]]['Username']
      mentorEmailToMenteesEmails[mentor] = menteeEmails
      
  mentor_index=0
  for mentee in master_mentee_emails:
    mentor = mentor_tables[category].iloc[num_match_mentors+mentor_index]['Username']
    mentorEmailToMenteesEmails[mentor].append(mentee)
    mentor_index=(mentor_index+1)%(num_mentors_in_category[category]-num_match_mentors)
                                                                   
  
  
# -------------------------------------------
# ---------------Export data-----------------
# -------------------------------------------

generate_csvs(familyToMentors, mentorEmailToMenteesEmails, mentors_filename, mentees_master_filename)

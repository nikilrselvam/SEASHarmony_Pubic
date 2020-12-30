import pandas as pd
import numpy as np
from constants import *

"""
Split df by major group.

Parameters
--------------------
    data           -- pandas df, mentor/mentee data

Returns
--------------------
    majorMap       -- dict, major_group_no->corresponding_df
"""

def splitByMajor(data):
    majorMap = dict();
    for i in range(1,num_major_categories+1):
        majorMap[i]=data.loc[data[categoryChoices['MajorsQuestion']]==i].reset_index(drop=True)
    return majorMap

"""
Process mentor data to get relevant contact details

Parameters
--------------------
    filename          -- string, path to mentor csv

Returns
--------------------
    mentor_contact     -- dict, ucla email -> (name,preferred email,phone)
"""
def get_mentor_contact(filename):
  mentor_data = pd.read_csv(filename)
  contact_columns=["Username", "Full Legal Name (First and Last)", "Preferred Email (We will use this email for all future communication)", "Phone Number (##########)"]
  mentor_data=mentor_data[contact_columns]
  
  mentor_contact=dict()
  
  for i in range(len(mentor_data)):
    mentor=mentor_data.iloc[i]
    if np.isnan(mentor[3]):
      contact_info=(mentor[1], mentor[2], "")
    else:
      contact_info=(mentor[1], mentor[2], int(mentor[3]))
    mentor_contact[mentor[0]]=contact_info
    
  return mentor_contact
  
"""
Process mentee data to get relevant contact details

Parameters
--------------------
    filename          -- string, path to mentee csv

Returns
--------------------
    mentee_contact     -- dict, email -> (name)
"""
def get_mentee_contact(filename):
  mentee_data = pd.read_csv(filename)
  contact_columns=["Name", "Email"]
  mentee_data=mentee_data[contact_columns]
  
  mentee_contact=dict()
  
  for i in range(len(mentee_data)):
    mentee=mentee_data.iloc[i]
    contact_info=(mentee[0])
    mentee_contact[mentee[1]]=contact_info
    
  return mentee_contact


if __name__ == '__main__':
  mentor_contact=get_mentor_contact("MentorSEAS Mentor Form.csv")
  print(mentor_contact)
  mentee_contact=get_mentee_contact("New-Transfers.csv")
  print(mentee_contact)


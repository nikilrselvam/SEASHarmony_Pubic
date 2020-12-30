import pandas as pd
import re
import csv

# function to split, alphebetize, and rejoin dash-separated groupname
def standardize_family_string(str):
  str=str.lower().strip()
  # to standardize groupnames
  regex = re.compile('[^a-zA-Z\-]')
  str = regex.sub('', str)
  str = str.split('-')
  ret = '-'.join(sorted(str))
  return ret

def get_inconsistencies(write_to_file=False, preferred_email=False):

  # this path name should be CHANGED depending on where the csv is stored #
  data = pd.read_csv('MentorSEAS Mentor Form.csv', quotechar='"', skipinitialspace=True)
  email_column_no=3 if preferred_email else 1
  family_column_no=21
  name_column_no=2

  # dictionary that maps groupnames to list of emails
  group_names = {}

  # number of rows in csv
  rows = len(data)

  # email to name mapping
  email_to_name={}
  for i in range(0, rows):
    email_to_name[data.iloc[i,email_column_no]]=data.iloc[i,name_column_no]

  # parse through csv and create/add to dictionary defintions, mapping groupnames to lists of emails
  for i in range(0, rows):
    if data.iloc[i,family_column_no] == data.iloc[i,family_column_no]:
      key = standardize_family_string(data.iloc[i,family_column_no])
      if key in group_names:
        ls = group_names[key]
        ls.append(data.iloc[i,email_column_no])
        group_names[key] = ls
      else:
        ls = [data.iloc[i,email_column_no]]
        group_names[key] = ls


  inconsistent_families=[]
  inconsistent_emails=[]
  consistent_emails=[]
  
  if write_to_file:
    # write out inconsistent families to csv
    with open('inconsistent_families.csv', 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      headers=['Submitted Family String', 'Member 1', 'Member 2', 'Member 3']
      csvwriter.writerow(headers)
      for g in group_names:
        names = g.split('-')
        ls = group_names[g]
        if len(names) != len(ls):
          inconsistent_families.append(g)
          family_members=[email_to_name[email] for email in ls]
          family_data=[g]
          family_data= family_data+family_members
          inconsistent_emails=inconsistent_emails+ls
          csvwriter.writerow(family_data)

    # write out consistent families to csv
    with open('consistent_families.csv', 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      headers=['Member 1', 'Member 2', 'Member 3']
      csvwriter.writerow(headers)
      for family in group_names.keys():
        if family not in inconsistent_families:
          family_members=[email_to_name[email] for email in group_names[family]]
          consistent_emails=consistent_emails+group_names[family]
          csvwriter.writerow(family_members)
            
  else:
    for g in group_names:
      names = g.split('-')
      ls = group_names[g]
      if len(names) != len(ls):
        inconsistent_families.append(g)
        family_members=[email_to_name[email] for email in ls]
        family_data=[g]
        family_data= family_data+family_members
        inconsistent_emails=inconsistent_emails+ls
    
    for family in group_names.keys():
      if family not in inconsistent_families:
        family_members=[email_to_name[email] for email in group_names[family]]
        consistent_emails=consistent_emails+group_names[family]
        
#  print("Inconsistent Emails")
#  print(inconsistent_emails)
#  print("Consistent Emails")
#  print(consistent_emails)
  
  return inconsistent_emails, consistent_emails
  
if __name__ == '__main__':
  get_inconsistencies(write_to_file=True, preferred_email=True)


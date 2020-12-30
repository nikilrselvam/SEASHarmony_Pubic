import pandas as pd
import numpy as np
import csv
from util import get_mentor_contact, get_mentee_contact


"""
Export data to csvs.

Parameters
--------------------
    familyToMentors              -- dict, family# -> [mentor emails]
    mentorEmailToMenteesEmails   -- dict, mentor_email -> [mentee_emails]

Returns
--------------------
    42
"""
def generate_csvs(familyToMentors, mentorEmailToMenteesEmails, mentors_filename, mentees_filename):
  
  mentor_contact=get_mentor_contact(mentors_filename)
  mentee_contact=get_mentee_contact(mentees_filename)
  
  
  mentor_email_list=[]
  with open('mentor_families.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    headers=['Family Number', 'Mentor 1', 'Mentor 2', 'Mentor 3']
    csvwriter.writerow(headers)
    for family in sorted(familyToMentors.keys()):
      names = [mentor_contact[email][0] for email in familyToMentors[family]]
      preferred_emails=[mentor_contact[email][1] for email in familyToMentors[family]]
      family_data=[family] +names
      csvwriter.writerow(family_data)
      mentor_email_list+=preferred_emails
      
  with open('mentee_to_mentor.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    headers=['Mentee', 'Family Number', 'Mentor']
    csvwriter.writerow(headers)
    for family in sorted(familyToMentors.keys()):
        for mentor in familyToMentors[family]:
          for mentee in mentorEmailToMenteesEmails[mentor]:
            mentee_data=[mentee_contact[mentee],family, mentor_contact[mentor][0]]
            csvwriter.writerow(mentee_data)
            
  with open('mentor_to_mentees.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    headers=['Mentor', 'Family Number', 'Mentees']
    csvwriter.writerow(headers)
    for family in sorted(familyToMentors.keys()):
        for mentor in familyToMentors[family]:
          mentees=[mentee_contact[mentee] for mentee in mentorEmailToMenteesEmails[mentor]]
          mentor_data=[mentor_contact[mentor][0],family, mentees]
          csvwriter.writerow(mentor_data)
    
  return 42


if __name__ == '__main__':
  print("Good job! End of pipeline :)")


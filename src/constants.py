mentors_filename="MentorSEAS Mentor Form.csv"
mentee_responses_filename="2020-21 MentorSEAS Mentee Form.csv"
mentees_master_filename="New-Freshmen.csv"

categoryChoices = {
    'ActivitiesRank': [
        'Select your 5 favorite activities out of 10 listed below! [1st]',
        'Select your 5 favorite activities out of 10 listed below! [2nd]',
        'Select your 5 favorite activities out of 10 listed below! [3rd]',
        'Select your 5 favorite activities out of 10 listed below! [4th]',
        'Select your 5 favorite activities out of 10 listed below! [5th]'],
    'Activities': [
        "Art/Theater",
        "Hiking/Outdoors",
        "Community Service",
        "Gym",
        "Greek Life",
        "Sports",
        "Video Games",
        "Watching TV/Movies",
        "Music" ],
    'FridaysQuestion': 'Which of the following best describes an ideal Friday night for you?',
    'FridaysResponse': [
        'Catch up on sleep',
        'Get ahead in class/Finish up homework',
        'Hang out with your best friend',
        'Hang out in a big group of friends',
        'Party' ],
    'MentorTypeQuestion': 'What kind of mentor would you be?',
    'MenteeTypeQuestion': 'What kind of mentor would you prefer?',
    'MentorTypeResponse': [
        'One that primarily provides emotional support',
        'One that primarily provides academic support'],
    'MajorsQuestion': 'What is your major?',
    'Majors': [
        'Aerospace Engineering',
        'Bioengineering',
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Computer Engineering',
        'Computer Science',
        'Computer Science and Engineering',
        'Electrical Engineering',
        'Material Science and Engineering',
        'Mechanical Engineering',
        'Undeclared Engineering' ],
    'TransferQuestion': 'Did you enter UCLA as a transfer student?',
    'MenteeTransferQuestion': 'Are you entering UCLA as a transfer student?',
    'TransferResponse': ['Yes', 'No'],
    'MentorshipQuestion': 'Could you provide mentorship in any of the following categories? ',
    'MenteeshipQuestion': 'Would you like a mentor in any of the following categories?',
    'Mentorship': [
        "Changing Majors",
        "First Generation",
        "International",
        "LGBTQ",
        "Out of State",
        "Racial Minority in Engineering",
        "Transfer Student",
        "Women in Engineering"],
    'MenteeTimeZoneQuestion': 'What time zone will you be living in this year?',
    'TimeZones' : [
        'GMT +0:00 (Greenwich Mean Time)',
        'GMT +1:00 (European Central Time)',
        'GMT +2:00 (Eastern European Time)',
        'GMT +3:00 (Middle East Time)',
        'GMT +4:00 (Near East Time)',
        'GMT +5:00 (Pakistan Lahore Time)',
        'GMT +5:30 (India Standard Time)',
        'GMT +6:00 (Bangladesh Standard Time)',
        'GMT +7:00 (Vietnam Standard Time)',
        'GMT +8:00 (China Taiwan Time)',
        'GMT +9:00 (Japan Standard Time)',
        'GMT +10:00 (Australia Eastern Time)',
        'GMT +12:00 (New Zealand Standard Time)',
        'GMT -10:00 (Hawaii Standard Time)',
        'GMT -9:00 (Alaska Standard Time)',
        'GMT -8:00 (Pacific Standard Time)',
        'GMT -7:00 (Mountain Standard Time)',
        'GMT -6:00 (Central Standard Time)',
        'GMT -5:00 (Eastern Standard Time)',
        'GMT -4:00 (Puerto Rico and US Virgin Islands Time)',
        'GMT -3:30 (Canada Newfoundland Time)',
        'GMT -3:00 (Argentina Eastern Time)',
        'GMT -1:00 (Central African Time)'
    ]
}


# must strictly use numbers 1 through n
majorToNums = {
    'Aerospace Engineering': 2,
    'Bioengineering': 4,
    'Chemical Engineering': 3,
    'Civil & Environmental Engineering': 3,
    'Computer Engineering': 1,
    'Computer Science': 1,
    'Computer Science and Engineering': 1,
    'Electrical Engineering': 1,
    'Material Science and Engineering': 3,
    'Mechanical Engineering': 2,
    'Undeclared Engineering': 4
}

# tied to the majorToNums, masterMajorToNums dict
num_major_categories = 4

mentorMatchCols = [
  categoryChoices.get('Activities')[0],
  categoryChoices.get('Activities')[1],
  categoryChoices.get('Activities')[2],
  categoryChoices.get('Activities')[3],
  categoryChoices.get('Activities')[4],
  categoryChoices.get('Activities')[5],
  categoryChoices.get('Activities')[6],
  categoryChoices.get('Activities')[7],
  categoryChoices.get('Activities')[8],
  categoryChoices.get('FridaysQuestion'),
  categoryChoices.get('Mentorship')[0],
  categoryChoices.get('Mentorship')[1],
  categoryChoices.get('Mentorship')[2],
  categoryChoices.get('Mentorship')[3],
  categoryChoices.get('Mentorship')[4],
  categoryChoices.get('Mentorship')[5],
  categoryChoices.get('Mentorship')[6],
  categoryChoices.get('Mentorship')[7],
  categoryChoices.get('MajorsQuestion'),
]

menteeMatchCols = [
  categoryChoices.get('Activities')[0],
  categoryChoices.get('Activities')[1],
  categoryChoices.get('Activities')[2],
  categoryChoices.get('Activities')[3],
  categoryChoices.get('Activities')[4],
  categoryChoices.get('Activities')[5],
  categoryChoices.get('Activities')[6],
  categoryChoices.get('Activities')[7],
  categoryChoices.get('Activities')[8],
  categoryChoices.get('FridaysQuestion'),
  categoryChoices.get('Mentorship')[0],
  categoryChoices.get('Mentorship')[1],
  categoryChoices.get('Mentorship')[2],
  categoryChoices.get('Mentorship')[3],
  categoryChoices.get('Mentorship')[4],
  categoryChoices.get('Mentorship')[5],
  categoryChoices.get('Mentorship')[6],
  categoryChoices.get('Mentorship')[7],
  categoryChoices.get('MajorsQuestion'),
  categoryChoices.get('MenteeTimeZoneQuestion')
]


master_major_map={
  'AEROSPCE':'Aerospace Engineering',
  'BIOENGR':'Bioengineering',
  'CHM ENGR':'Chemical Engineering',
  'CIV ENGR':'Civil & Environmental Engineering',
  'COM ENGR':'Computer Engineering',
  'COM SCI':'Computer Science',
  'C S&ENGR':'Computer Science and Engineering',
  'ELE ENGR':'Electrical Engineering',
  'MAT ENGR':'Material Science and Engineering',
  'MECHANIC':'Mechanical Engineering',
  'UN-E&AS':'Undeclared Engineering'
}


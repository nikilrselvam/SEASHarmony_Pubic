import numpy as np

"""
Return a stable matching as obtained from Gale Shapley

Parameters
--------------------
    n                       -- int, number of mentors/mentees (must be equal)
    mentor_preferences      -- ndarray of shape (n,n), mentor_preferences[i] is the all the mentee indices in order of preference of mentor i
    mentee_preferences      -- ndarray of shape (n,n), mentee_preferences[i] is the all the mentor indices in order of preference of mentee i

Returns
--------------------
    mentor_matches          -- array of length n, mentor_matches[i] corresponds to index of the mentor matched to mentee i
"""

def stable_match(n, mentor_preferences, mentee_preferences):

    # mentor_matches stores mentee/mentor pairs
    mentor_matches = [-1 for i in range(n)]

    # last_match[i] stores the index of the last checked mentee for mentor[i]
    last_match = [-1 for i in range(n)]

    # stores availability of mentor
    mentorFree = [True for i in range(n)]

    freeCount = n
    m=0 # current_mentor

    # while there are free mentors
    while (freeCount > 0):

        if(mentorFree[m]):

          # Go through mentees according to m's preferences
          while last_match[m] < n-1:
              last_match[m]+=1
              mentee = mentor_preferences[m][last_match[m]]

              # the preferred mentee is free, so mentee and mentor become matched
              if (mentor_matches[mentee] == -1):
                  mentor_matches[mentee] = m
                  mentorFree[m] == False
                  freeCount -= 1
                  break

              else:
                  # preferred mentee is not free, check current match
                  existing_m = mentor_matches[mentee]

                  # if new match is better, create it
                  if (mentee_preferences[mentee].tolist().index(m) < mentee_preferences[mentee].tolist().index(existing_m)):
                      mentor_matches[mentee] = m
                      mentorFree[m] = False
                      mentorFree[existing_m] = True
                      break

                  # otherwise, do nothing
                  pass

        # cycle through the mentors
        m=(m+1)%n

    return mentor_matches




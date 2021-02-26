import numpy as np
from helper import rSubset

def PassOne(data, support):
  occurences = {}           # Save the number of times an item has occured in the data 
  # Loop through every line in the data
  for line in data:
    # Loop through every item in that line
    for item in line:
      # If the item is not currently accounted for, set its counter to 1
      if item not in occurences:
        occurences[item] = 1
      # If it is accoutned for, add one to its counter
      else:
        occurences[item] += 1
  # Return a list of frequent items
  return GetFrequentItems(occurences, support * len(data))

def PassTwo(data, frequent_list, support):
  occurences = {}
  temp_ = []
  for line in data:
    if(len(line) >= 2):
      temp_ = rSubset(line, 2)
      for item_set in temp_:
        is_frequent = True
        for item in item_set:
          if item not in frequent_list:
            is_frequent = False
        if is_frequent == True:
          if item_set not in occurences:
            occurences[item_set] = 1
          else:
            occurences[item_set] += 1
  return occurences, GetFrequentItems(occurences, support * len(data))

# Function to get a list of frequent items from passed data depending on support value
def GetFrequentItems(occurences, support):
  frequent_items = []
  for item in occurences:
    if occurences[item] >= support:
      frequent_items.append(item)
  return frequent_items

def CreateCandidates(prev_freq_items, k):
  candidates = JoinStep(prev_freq_items, k)
  return PruneStep(candidates, prev_freq_items, k)

def JoinStep(items, k):
  joined = []
  n = len(items)
  for i in range(n):
    for j in range(i+1, n):
      L1 = list(items[i])[:0] # get everything up until index [k-2]
      L2 = list(items[j])[:0]
      L1.sort()
      L2.sort()
      if L1 == L2 and (list(set(items[i]) | set(items[j])) not in joined):
        joined.append(list(set(items[i]) | set(items[j])))
  print("Joined list: " + str(joined))
  return joined


def PruneStep(candidates_list, freq_items, k):
  new_freq_items = []
  temp_ = []
  for candidates in candidates_list:
    print("Candidates: " + str(candidates))
    is_frequent = True
    temp_ = rSubset(candidates, k - 1)
    for candidate in temp_:
      if candidate not in freq_items:
        print(str(candidate) + " is not in frequent items: " + str(freq_items))
        is_frequent = False
    if is_frequent:
      new_freq_items.append(candidates)
  return new_freq_items
    
# Run apriori algorithm
# ARGUMENTS
# data: The data to parse through
# support: Array of support threshholds to check
# k: How many items we want in a set
def Apriori(data, support, k):
  freq = PassOne(data, support)
  occ2, freq2 = PassTwo(data, freq, support)
  if k > 2:
    return CreateCandidates(freq2, k)
  return freq2

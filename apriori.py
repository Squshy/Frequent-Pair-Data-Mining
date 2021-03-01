import numpy as np
from helper import rSubset, GetFrequentItems

# First pass of data
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
  return GetFrequentItems(occurences, support)

# Second pass of data
def PassTwo(data, frequent_list, support):
  occurences = {} # Save the number of times an item has occured in the data 
  temp_ = []      # Temporary array used to save the current subset we are looking at
  # Loop through every line in the data
  for line in data:
    # If the length of the line is greater than 2
    # Checking for lines that only have 1 data item in it
    # If there is only one item, then there cant be any pairs here
    if(len(line) >= 2):
      temp_ = rSubset(line, 2)  # Create sets of pairs from the line
      # For every pair of items in the current list of item pairs
      for item_set in temp_:
        item_set = tuple(sorted(item_set))  # sort the tuple
        is_frequent = True  # set a frequent flag to true
        # For every individual item in the pear
        for item in item_set:
          # If the item is not in the previously counted frequent list
          if item not in frequent_list:
            is_frequent = False     # Set the frequent flag to false
        # If the pair is frequent
        if is_frequent == True:
          # If the pair isn't already accounted for in the occurences
          # Initialize that pairs count to 1
          if item_set not in occurences:
            occurences[item_set] = 1
          # If the pair has been accounted for already
          # Add one to that pairs count
          else:
            occurences[item_set] += 1
  # Return the dictionary of occurences and also the frequent items
  return GetFrequentItems(occurences, support)

# Attempt at creating candidates
def CreateCandidates(prev_freq_items, occurences, k):
  candidates = JoinStep(prev_freq_items, k)
  return PruneStep(candidates, prev_freq_items, occurences, k)

# Attempt at join step
def JoinStep(items, k):

  joined = []
  n = len(items)
  for i in range(n):
    for j in range(i+1, n):
      itemset_1 = list(items[i])  # Get the first item list to check
      itemset_2 = list(items[j])  # Get the second item list to check
      # Sort the item lists
      itemset_1.sort()
      itemset_2.sort()
      # If the first [k-1] items of the lists are the same, append them to a candidate list
      if itemset_1[:k-1] == itemset_2[:k-1]:
        candidate = list(set(itemset_1) | set(itemset_2))
        candidate.sort()  # Sort the candidate list
                          # This helps solve problems in the pruning step
        joined.append(candidate)
  # Return the list of joined candidates
  return joined

# Attempt at pruning items
def PruneStep(candidates_list, freq_items, occurences, k):
  new_freq_items = []     # list of new frequent items
  temp_ = []              # Temp list used to hold current subset of items

  # For every candidate in the candidate list 
  for candidates in candidates_list:
    is_frequent = True    # Set a frequent flag to true
    temp_ = rSubset(np.asarray(candidates), k)  # Create a subset of items equal to the length of k
                                                # This is used for checking if all previous subsets are frequent
                                                # The new set must be frequent then
    # For every candidate set of items in the temp list just created
    for candidate in temp_:
      candidate = tuple(candidate)  # Sort the tuple 
      # If the candidate grouping is not in the frequent items
      # We know the current merged set cannot be frequent
      if candidate not in freq_items:
        is_frequent = False   # Set the frequent flag to false

    # If the candidate is frequent 
    # Add it to the frequent items
    if is_frequent:
      candidates = tuple(candidates)
      new_freq_items.append(candidates)  # Save candidates as tuple
  return new_freq_items
    
# Run apriori algorithm
# ARGUMENTS
# data: The data to parse through
# k: How many items we want in a set
def Apriori(data, support, k):
  min_support = support * len(data)
  occ, freq = PassOne(data, min_support)
  occ, freq = PassTwo(data, freq, min_support)
  if k > 2:
    for i in range(2, k):
      candidates = CreateCandidates(freq, occ, i)
      freq = candidates
    return candidates
  return occ, freq
  

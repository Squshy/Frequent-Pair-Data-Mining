import numpy as np
import math
from helper import rSubset, GetFrequentItems

# Hash function for mapping data to buckets
def HashFunction(pair, data_size):
  # pair[0] is the first item in the pair
  # pair[1] is second item in the pair
  # Multiply their integer values together
  # Get the modulous of that scalar of the length of data * 30%
  return math.floor((int(pair[0]) * int(pair[1])) % (data_size * .3))

# First pass of data
def PassOne(data, support):
  occurences = {}   # Save the number of times an item has occured in the data 
  hash_table = {}   # Hash table to save data of pairs hashed to a bucket 
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
    #
    # Everything till now was same as Apriori
    # NEW TO PCY
    #
    pairs_of_items = rSubset(line, 2)  # Want to get pairs of items
    for pair in pairs_of_items:
      # Hash the pair to a bucket
      key = HashFunction(pair, len(data))
      # If the key has not already been instered in the dictionary add it
      # If it has, add one to the count
      if key not in hash_table:
        hash_table[key] = 1
      else: 
        hash_table[key] += 1
  # Get the occurences and frequent items from the first pass
  occurences, frequent_items = GetFrequentItems(occurences, support * len(data))
  # Return the hash table, occurences, and frequent items
  return hash_table, occurences, frequent_items

# Determine if a bucket is frequent or not in a hashtable
def DetermineFrequentBuckets(hash_table, support):
  freq_buckets = np.zeros(len(hash_table))   # New vector that will only have possible frequent items
  # Look through all buckets
  for bucket in hash_table:
    # If the occurrences of hashed items is greater than the support
    # Should add a bit vector here?  Not sure how
    if hash_table[bucket] >= support:
      freq_buckets[bucket] = 1
  return freq_buckets

# Second pass of PCY algorithm
def PassTwo(data, frequent_items, support, bitmap):
  frequent_candidates = {}
  # Loop through all lines in the data
  for line in data:
    # If the line has enough items to make a pair
    if(len(line) >= 2):
      temp_ = rSubset(line, 2)  # Create sets of pairs from the line
      # For every pair of items in the current list of item pairs
      for item_set in temp_:
        item_set = tuple(sorted(item_set))  # sort the tuple
        is_frequent = True  # set a frequent flag to true
        # For every individual item in the pear
        for item in item_set:
          # If the item is not in the previously counted frequent list
          if item not in frequent_items:
            is_frequent = False     # Set the frequent flag to false
        # If the pair is frequent
        if is_frequent == True:
          # Get the key from the hash function relating this pair
          key = HashFunction(item_set, len(data))
          # If the pair is in the bit map
          if bitmap[key] == 1:
            # If the pair is not currently in the occurences list
            if item_set not in frequent_candidates:
              frequent_candidates[item_set] = 1
            else: 
              frequent_candidates[item_set] += 1
  return GetFrequentItems(frequent_candidates, support * len(data))

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

def PCY(data, support, k):
  hash_table, occurences, freq_items = PassOne(data, support)
  bitmap = DetermineFrequentBuckets(hash_table, support)
  occ, freq = PassTwo(data, freq_items, support, bitmap)
  if k > 2:
    for i in range(2, k):
      candidates = CreateCandidates(freq, occ, i)
      freq = candidates
    return candidates
  return occ, freq

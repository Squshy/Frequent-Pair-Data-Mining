import numpy as np
import math
from helper import rSubset, GetFrequentItems

# Hash function for mapping data to buckets
def HashFunction(pair, data_size):
  return math.floor((int(pair[0]) * int(pair[1])) % (data_size * .3))

# First pass of data
def PassOne(data, support):
  occurences = {}   # Save the number of times an item has occured in the data 
  hash_table = {}   # Hash table to save data of pairs hashed to a bucket 
  i = 0
  # Loop through every line in the data
  for line in data:
    if i % 50000 == 0:
      print("Reading line %d of %d" % (i, len(data)))
    # Loop through every item in that line
    for item in line:
      # If the item is not currently accounted for, set its counter to 1
      if item not in occurences:
        occurences[item] = 1
      # If it is accoutned for, add one to its counter
      else:
        occurences[item] += 1
    i +=1
    #
    # Everything till now was same as Apriori
    # NEW TO PCY
    #
    pairs_of_items = rSubset(line, 2)  # Want to get pairs of items
    for pair in pairs_of_items:
      # Hash the pair to a bucket
      key = HashFunction(pair, len(data))
      if key not in hash_table:
        hash_table[key] = 1
      else: 
        hash_table[key] += 1
  occurences, frequent_items = GetFrequentItems(occurences, support * len(data))
  return hash_table, occurences, frequent_items

def DetermineFrequentBuckets(hash_table, support):
  freq_buckets = {}
  for bucket in hash_table:
    if hash_table[bucket] >= support:
      freq_buckets[bucket] = 1
  return freq_buckets

def PassTwo(data, frequent_items, support, bitmap):
  frequent_candidates = {}

  for line in data:
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
          key = HashFunction(item_set, len(data))
          if key in bitmap:
            if item_set not in frequent_candidates:
              frequent_candidates[item_set] = 1
            else: 
              frequent_candidates[item_set] += 1
  return GetFrequentItems(frequent_candidates, support * len(data))

def PCY(data, support, k):
  hash_table, occurences, freq_items = PassOne(data, support)
  bitmap = DetermineFrequentBuckets(hash_table, support)
  pair_occurences, freq_pairs = PassTwo(data, freq_items, support, bitmap)
  return freq_pairs

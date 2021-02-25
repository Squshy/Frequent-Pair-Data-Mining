# Authors: Calvin Lapp, Hooria Hajiyan

# Pass 1
# Read dataset and find individual items
# Find frequent Items
# cK : list of candidate those might be frequent items
# lK : The set of truly frequent items
def GetDataItems(baskets_data):
  print("Getting unique items in baskets...")
  Ck = [] 
  i = 0
  for basket in baskets_data:
    if(i % 10000) == 0: # print every 10,000 iterations
      print("Checking line %d in first pass" % i)
    for item in basket:
      if not [item] in Ck:
        Ck.append([item])
    i += 1
  return [set(x) for x in Ck]

# calculate the support
# scan through transaction data and return a list of candidates that meet the support threshold 
# and support data about the current candidates
#
# arguments:
# count: a dictionary
# freq_item: a list to return the frequent items and supports
# l1 = list of frequent items for next step
# Prune step
def DetermineFrequentItems(baskets_data, Ck, min_support):
  print("Determining Frequent Items...")
  count = {}
  freq_items = []
  Lk = []
  min_support = min_support
  # Loop through baskets
  for basket in baskets_data:
    # Check each item in the basket
    for item in Ck:
      # If the item is a subset of the basket (if the item is in the basket)
      if item.issubset(basket):
        candidate = frozenset(item)
        # If the candidate is not in count, then create it and initialize its count to 1
        if candidate not in count:
          count[candidate] = 1
        # Otherwise add to its count
        else:
          count[candidate] += 1
  # calc support for each item in c1
  for item in count:
    support = count[item] / len(baskets_data)
    if support >= min_support:
      freq_items.insert(0, support)
      Lk.insert(0, item)
  return Lk, freq_items

# Pass 2
# Given Lk, generate Ck+1 in two steps
# Join Step - Join Lk with Lk by joining tow k itemsets in Lk
# Pruning step - Delete all candidates in Ck+1 that are non-frequent subsets
# CreateCk - Takes a list of frequent items Lk, and size of the itemsets, k, and complete this with two for loops
# Join Step
def CreateCK(Lk, k):
  print("Creating Ck...")
  cand_list = []
  n = len(Lk)
  for i in range(n):
    for j in range(i+1, n):
      L1 = list(Lk[i])[:k-2] # get everything up until index [k-2]
      L2 = list(Lk[j])[:k-2]
      L1.sort()
      L2.sort()
      if L1 == L2:
        cand_list.append(Lk[i] | Lk[j])
  return cand_list

# Runs Apriori algorithm on the data set passed, granting k sized item groupings that pass support of min_support
# Returns final frequent list
def Apriori(baskets_data, k, min_support):
  Lk, CK, freq_items = [], [], []
  for i in range(k):
    if(i == 0): # First run of loop
      Ck = GetDataItems(baskets_data)
    else:
      Ck = CreateCK(Lk, k)
    Lk, freq_items = DetermineFrequentItems(baskets_data, Ck, min_support)
  return Lk, freq_items
    
import os
import pandas as pd
import numpy as np
from itertools import combinations

# Reads a test file and returns its data in an array
def GetItemsetFromFile(file):
  return np.asarray([i.strip().split() for i in open(file, 'r').readlines()])

# Takes an array of support values and the data values and appends them together
def CreateSupportList(data, support):
  i = 0
  new_list = []
  for clump in data:
    current_list = []
    for item in clump:
      current_list.append(item)
    current_list.append(support[i])
    new_list.append(current_list)
    i+=1
  return new_list

# Saves a Pandas DataFrame to an html file
def SaveDataFrameToHTMLFile(df, filename):
  html = df.to_html()
  filepath = "./report/table_files/" + filename + ".html"
  try:
    os.remove(filepath)
  except OSError:
    pass
  file = open(filepath, 'a')
  file.write(html)
  file.close()

# Get subsets of data
def rSubset(data, r):
  return list(combinations(data, r))

# Gets x % of data from the data passed
# If you pass 0.2, you get 20% of the data returned starting from the beginning of the data
def GetSubsectionOfData(data, percent):
  data_len = len(data)
  amount_of_data = round(data_len * percent)
  return data[:amount_of_data]

def SplitDataIntoChunks(data, chunk_size):
  data_fragments = []
  data_len = len(data)

  data_size = chunk_size
  while data_size < 1:
    prev_data = GetSubsectionOfData(data, data_size)
    print(len(prev_data))
    data_size += data_size

  amount_of_data = round(data_len * percent)
  return data[:amount_of_data]

# Function to get a list of frequent items from passed data depending on support value
def GetFrequentItems(occurences, support):
  frequent_items = [] # list of frequent items to be returned
  items_occurences = []  # list of support values for the items
  # Loop through every item in the occurences
  for item in occurences:
    # If that item has occured more than support threshold append it to frequent items
    if occurences[item] >= support:
      frequent_items.append(item)
      items_occurences.append(occurences[item])
  return items_occurences, frequent_items

# Returns a dataframe of pair occurrences and frequency
def CreatePairDataFrame(occurences, frequency_list, length_of_data):
  data = np.asarray(list((zip(frequency_list, occurences))))
  data1 = np.array([item[0] for item in data[:,0]])
  data2 = np.array([item[1] for item in data[:,0]])
  return pd.DataFrame({'Item 1': data1, 'Item 2': data2, 'Support': data[:,-1] / length_of_data})

# Returns a dataframe of triple occurences
def CreateTripleDataFrame(frequency_list):
  triple_array = np.asarray([np.array(x) for x in frequency_list])
  return pd.DataFrame({'Item 1': triple_array[:,0], 'Item 2': triple_array[:,1], 'Item 3': triple_array[:,-1]})

def PrintTimeInfo(algo, percent_of_data, time, support, word):
  print("Time taken to complete %s on %d%% of data using %s of retail data: %.2f seconds with support: %d%%" % (algo, percent_of_data, word, time, (support * 100)))
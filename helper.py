import os
import pandas as pd
import numpy as np
from itertools import combinations

def GetItemsetFromFile(file):
  return np.asarray([i.strip().split() for i in open(file, 'r').readlines()])

def SaveDataToFile(data, support, filename):
  try:
    os.remove(filename)
  except OSError:
    pass
  file = open(filename, "w")
  i = 0
  for clump in data:
    file.write("{")
    first = True
    for item in clump:
      if first:
        first = False
        file.write(str(item))
      else:
        file.write(", ")
        file.write(str(item))
    file.write("} Support: %.2f\n" % support[i])
    i += 1
  file.close()

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

def SaveDataFrameToHTMLFile(df, filename):
  html = df.to_html()
  try:
    os.remove(filename)
  except OSError:
    pass
  filepath = "./report/table_files/" + filename + ".html"
  file = open(filepath, 'a')
  file.write(html)
  file.close()

def rSubset(data, r):
  return list(combinations(data, r))

def GetSubsectionOfData(data, percent):
  data_len = len(data)
  amount_of_data = round(data_len * percent)
  print("%d%% of %d is %d" % ((percent * 100), data_len, len(data[:amount_of_data])))
  return data[:amount_of_data]

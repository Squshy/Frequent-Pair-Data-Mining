from apriori import GetDataItems, CreateCK, DetermineFrequentItems, Apriori
from helper import GetItemsetFromFile, SaveDataToFile
import pandas as pd
from time import time

baskets_data = [
  ['bear', 'apple'],
  ['bear', 'orange', 'onion'],
  ['apple', 'orange', 'onion'],
  ['bear', 'apple', 'orange', 'onion'],
  ['bear', 'apple', 'orange'],
  ['apple', 'orange'],
  ['orange'],
  ['apple', 'onion', 'orange'],
  ['orange', 'onion'],
  ['apple', 'orange', 'onion']
]

#print("Filtering data into buckets...")
#s_t = time()
#data = GetItemsetFromFile("netflix.data")
#f_t = time()
#print("Done filtering data into buckets after %.2f seconds" % (f_t - s_t))
min_support = 0.5

data, supp = Apriori(baskets_data, 2, min_support)
SaveDataToFile(data, supp, "apri_test.data")
df = pd.DataFrame(list(data), columns=['Item 1', 'Item 2'])
#print("Running Apriori")
#s_t = time()
#apri = Apriori(data, 2, min_support)
#f_t = time()
#print("Finished running Apriori on Netflix data after %.2f seconds" % (f_t - s_t))
#print(apri)

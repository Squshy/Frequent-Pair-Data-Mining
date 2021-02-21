from apriori import GetDataItems, CreateCK, DetermineFrequentItems, Apriori
from helper import GetItemsetFromFile

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
min_support = 0.5

print("Support threshold for data: %f" % min_support)
C1 = GetDataItems(baskets_data)
print("\nUnique Items: \n" + str(C1))
L1 = DetermineFrequentItems(baskets_data, C1, min_support)
print("\nCurrent frequent items after pass 1: \n" + str(L1))
print("\nPrinting candidate list:")
C2 = CreateCK(L1, 2)
print(C2)
L2 = DetermineFrequentItems(baskets_data, C2, min_support)
print("\nCurrent frequent item pairs after pass 2: \n" + str(L2))

apri = Apriori(baskets_data, 2, min_support)

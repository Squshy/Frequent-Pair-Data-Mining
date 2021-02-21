# Helper functions used through multiple lab folders

def GetItemsetFromFile(file):
  return [i.strip().split() for i in open(file, 'r').readlines()]
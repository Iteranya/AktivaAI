import csv

import pandas as pd

def get_names_from_csv_pandas(filename, chunksize=100):
  names_list = []
  for chunk in pd.read_csv(filename, chunksize=chunksize):
    names_list.extend(chunk.iloc[:, 0].tolist())  # Assuming names are in first column
  return names_list

names = get_names_from_csv_pandas("stabdiff/danbooru_tags.csv")

count = 0
for name in names:
  if count < 600:
    print(f"\"{name}\"|",end="")
    count += 1
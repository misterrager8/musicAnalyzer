import pandas as pd
import matplotlib.pyplot as plt

dataframe = pd.read_csv("data.csv")

sums = dataframe.groupby("albumTitle").mean()
#print(sums)
#
sums2 = sums.sort_values(by = "plays", ascending=False)[:10]
print(sums2)
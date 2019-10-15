import pandas as pd

dataframe = pd.read_csv("data.csv")

avgPlays = dataframe.groupby("albumTitle").mean().sort_values(by = "plays", ascending=False)[:10]

print(avgPlays)
import pandas as pd

dataframe = pd.read_csv("data.csv")

avgPlays = dataframe.groupby("albumTitle").mean().sort_values(by = "plays", ascending=False)[:50]

statsList = open("stats.txt", "w")
statsList.write(avgPlays.to_string())
statsList.close

print("done")
import pandas as pd
import os  
import numpy as np

path = "compilier_fuzzing/data/github/github_issues.feather"
df = pd.read_feather(path=path)

number_of_chunks = 5
for idx, chunk in enumerate(np.array_split(df, number_of_chunks)):
    chunk.to_csv(f'compilier_fuzzing/data/github/issues_{idx}.csv')
# df.to_csv('compilier_fuzzing/data/github/issues.csv') 
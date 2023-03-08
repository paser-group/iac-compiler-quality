import pandas as pd
import os  
import numpy as np

path = "compilier_fuzzing/data/chatgpt/chatgpt_short_yaml.feather"
df = pd.read_feather(path=path)
df2 = pd.DataFrame()

# copy the 'A' column from df1 to df2
df2['title'] = df.loc[:, 'title']
df2['prompt'] = ''
df2['output'] = ''


# number_of_chunks = 1
# for idx, chunk in enumerate(np.array_split(df, number_of_chunks)):
#     chunk.to_csv(f'compilier_fuzzing/data/chatgpt/prompts.csv')
df2.to_csv(f'compilier_fuzzing/data/chatgpt/prompts.csv')
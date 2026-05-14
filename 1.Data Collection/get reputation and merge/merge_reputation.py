import pandas as pd
from pandas import Series

data = pd.read_csv('./sample_Serialized.csv')



repdata = pd.read_csv('./reputation_output.csv')

i=0
for index,row in repdata.iterrows():
    if(row['link'] in data['link'].tolist()):
        i+=1
        data.loc[data[data['link'] == row['link']].index,['reputation']] = [row['reputation']]

print(i)
data.to_csv("newdata.csv", index=True, sep=',')
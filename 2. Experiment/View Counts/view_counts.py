import pandas as pd
from pandas import Series

data = pd.read_csv('../../sample_Serialized.csv')

viewcounts = pd.read_csv('./viewed_counts.csv')


i=0
for index,row in viewcounts.iterrows():
    if(row['link'] in data['link'].tolist()):
        i+=1
        data.loc[data[data['link'] == row['link']].index,['viewed_counts']] = [row['viewed_counts']]

print(i)
data.to_csv("newdata.csv", index=True, sep=',')
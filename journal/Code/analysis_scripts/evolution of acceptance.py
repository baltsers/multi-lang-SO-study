import pandas as pd
from pandas import Series

#Use pandas to read data
data = pd.read_csv('../../sample_Serialized.csv')
#print(data)


date_sym = data.reset_index(drop=True)[['active time','accepted']]
date_sym['active time'] = pd.to_datetime(date_sym['active time'])
date_sym = date_sym.set_index('active time')

df = date_sym['2008']
df = df.groupby(by=['accepted']).size()
df = df.to_frame()
df.columns=['values']
df = df.reset_index()
df.insert(df.shape[1],'year',2008)
new_df = pd.pivot(df,index='year',columns='accepted',values='values')
# print(new_df)
for year in range(2009,2022):
    df = date_sym[str(year)]
    df = df.groupby(by=['accepted']).size()
    df = df.to_frame()
    df.columns = ['values']
    df = df.reset_index()
    df.insert(df.shape[1], 'year', year)
    df = pd.pivot(df, index='year', columns='accepted', values='values')
    # print(df)
    new_df = pd.concat([new_df,df])
new_df = new_df.fillna(0)
new_df.to_csv("output2.csv",index=True,sep=',')

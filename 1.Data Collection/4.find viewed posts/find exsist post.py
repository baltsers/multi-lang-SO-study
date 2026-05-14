import pandas as pd
from pandas import Series

data1 = pd.read_csv('./SO-2-tuple.csv')
data2 = pd.read_csv('./SO-3-tuple.csv')
data3 = pd.read_csv('./SO-4-tuple.csv')
olddata = pd.concat([data1,data2,data3])
olddata = olddata.reset_index()


data = pd.read_csv('./data.csv',encoding='ANSI')

# newdata = pd.merge(data, olddata, how='inner', on=['link'])
i=0
for index,row in olddata.iterrows():
    if(row['link'] in data['link'].tolist()):
        i+=1
        data.loc[data[data['link'] == row['link']].index,['question contain code','Solution type','answer or highest vote','Symptoms ','SDLC','Special case','Taxonomy_Second','Taxonomy_Third']] = [row['question contain code'],row['Solution type'],row['answer or highest vote'],row['Symptoms '],row['SDLC'],row['Special case'],row['Taxonomy_Second'],row['Taxonomy_Third']]



# newdata = pd.merge(data, olddata, how='inner', on=['link'])
# newdata.to_csv("repeat.csv",index=True,sep=',')



#remove data that lian wei le have viewed

print(i)
data.to_csv("newdata.csv", index=True, sep=',')
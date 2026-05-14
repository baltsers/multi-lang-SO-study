import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



from mlxtend.frequent_patterns import apriori, association_rules

def encoder(x):
    if x<= 0:
        return 0
    else:
        return 1



data = pd.read_csv('./sample_Serialized.csv')

#Filter the language combination
comb = data['combination']
comb = pd.Series(comb)
lans = set(['javascript','php','java','c++','c','c#','python','shell'])
#convert data to set
comb_list = []
for cb in comb:
    str = cb.split(",")
    str_set = (set(str) & lans)
    comb_list.append(','.join(str_set))

sym_comb = pd.DataFrame({'Symptoms':data['Symptoms'],
                         'combination':comb_list})

# sym_comb = data.reset_index(drop=True)[['Symptoms', 'combination']]
sym_comb = sym_comb.reset_index(drop=True)[['Symptoms', 'combination']]
sym_comb = sym_comb.reset_index()

#split the dataframe
df1 = sym_comb[['index','Symptoms']]
df2 = sym_comb[['index','combination']]
df1.columns = ['index','item']
df2.columns = ['index','item']
df=pd.concat([df1,df2])
df['qty']=1


df = df.groupby(by=['index', 'item'])['qty'].sum().unstack().reset_index().fillna(0).set_index('index')
df = df.applymap(encoder)

print(df)

items_together = apriori(df, min_support=0.001, use_colnames=True)
#print(items_together.head())

rules = association_rules(items_together, metric='lift', min_threshold=1)
#print(rules.head(10))
rules.to_csv("RQ3_association.csv",index=True,sep=',')

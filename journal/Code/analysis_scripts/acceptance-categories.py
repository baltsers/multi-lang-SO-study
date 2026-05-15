import pandas as pd
from pandas import Series

#Use pandas to read data
data = pd.read_csv('../../sample_Serialized.csv')

sym = data['Symptoms']
sym = Series(sym)

second = data['Taxonomy_Second']
second = Series(second)

# print(second.value_counts())

third = data['Taxonomy_Third']
third = Series(third)



sym_list = []
for _sym in sym:
    sym_list.append(_sym)

second_list = []
for _second in second:
    second_list.append(_second)

third_list = []
for _third in third:
    third_list.append(_third)

sol = data['accepted']
sol = Series(sol)
sol_result = pd.value_counts(sol)

sol = sol.reset_index(drop=True)
comb_sol = pd.DataFrame({'Symptoms': sym_list,
                         'acceptance': sol})
comb_sol.groupby(by=['Symptoms','acceptance']).size().to_csv("acceptance-symptoms.csv",index=True,sep=',')

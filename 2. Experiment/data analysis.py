import pandas as pd
from pandas import Series

#Use pandas to read data
# data = pd.read_csv('../sample_Serialized.csv')
data = pd.read_csv('../for_view_count.csv')
#print(data)
#RQ1
#Got the Taxonomy type of all questions
sym = data['Symptoms']
sym = Series(sym)

# print(sym.value_counts())
#print(len(sym.value_counts()))

second = data['Taxonomy_Second']
second = Series(second)

# print(second.value_counts())

third = data['Taxonomy_Third']
third = Series(third)

# print(third.value_counts())

sdlc = data['SDLC']
sdlc = Series(sdlc)

# print(sdlc.value_counts())

date_sym = data.reset_index(drop=True)[['create time','Symptoms']]
date_sym['create time'] = pd.to_datetime(date_sym['create time'])
date_sym = date_sym.set_index('create time')

df = date_sym['2008']
df = df.groupby(by=['Symptoms']).size()
df = df.to_frame()
df.columns=['values']
df = df.reset_index()
df.insert(df.shape[1],'year',2008)
new_df = pd.pivot(df,index='year',columns='Symptoms',values='values')
# print(new_df)
for year in range(2009,2022):
    df = date_sym[str(year)]
    df = df.groupby(by=['Symptoms']).size()
    df = df.to_frame()
    df.columns = ['values']
    df = df.reset_index()
    df.insert(df.shape[1], 'year', year)
    df = pd.pivot(df, index='year', columns='Symptoms', values='values')
    # print(df)
    new_df = pd.concat([new_df,df])
new_df = new_df.fillna(0)
# new_df.to_csv("RQ1_2_data.csv",index=True,sep=',')




#RQ2
comb = data['combination']
comb = Series(comb)
lans = set(['javascript','php','java','c++','c','c#','python','shell'])
#convert data to set
comb_list = []
for cb in comb:
    str = cb.split(",")
    str_set = (set(str) & lans)
    comb_list.append(str_set)

comb_result = pd.value_counts(comb_list)
#print(len(comb_result))
#print(comb_result)
#comb_result.to_csv("RQ2_data.csv",index=True,sep=',')


#RQ3
sym_list = []
for _sym in sym:
    sym_list.append(_sym)

# ---------------------------------------for view counts----------------------
#convert set to str
new_comb_list = []
for _comb in comb_list:
    str1 = ""
    for _str in _comb:
        str1 = str1 + _str
        str1 = str1 + ","
    str1 = str1[:-1] #delete last symbol ","
    new_comb_list.append(str)


viewed_counts = data['viewed_counts'].to_list()
new_viewed_counts = []

for count in viewed_counts:
    new_viewed_counts.append(int(count.replace(',','')))


sym_comb = pd.DataFrame({#'Symptoms':sym_list,
                         'Combination':[','.join(lans) for lans in comb_list],
                         'viewedcounts':new_viewed_counts})

# sym_comb.groupby(by=['Symptoms','Combination']).size().to_csv("RQ3_data.csv",index=True,sep=',')
# sym_comb.groupby(['Symptoms','Combination'])['viewedcounts'].sum().to_csv('view_counts.csv',index=True,sep=',')
sym_comb.groupby(['Combination'])['viewedcounts'].sum().to_csv('view_counts.csv',index=True,sep=',')
#---------------------------normal------------------------------------------
# #convert set to str
# new_comb_list = []
# for _comb in comb_list:
#     str1 = ""
#     for _str in _comb:
#         str1 = str1 + _str
#         str1 = str1 + ","
#     str1 = str1[:-1] #delete last symbol ","
#     new_comb_list.append(str)
#
#
# sym_comb = pd.DataFrame({'Symptoms':sym_list,
#                          'Combination':comb_list})
#
# # sym_comb.groupby(by=['Symptoms','Combination']).size().to_csv("RQ3_data.csv",index=True,sep=',')


#RQ4
sol = data['accepted']
sol = Series(sol)
sol_result = pd.value_counts(sol)
# sol_result.to_csv("RQ4_data.csv",index=True,sep=',')

sol = sol.reset_index(drop=True)
comb_sol = pd.DataFrame({'Combination':new_comb_list,
                         'solved':sol})
# comb_sol.groupby(by=['Combination','solved']).size().to_csv("RQ4_2_data.csv",index=True,sep=',')

# left = sym_comb.groupby(by=['Symptoms','Combination']).size()
# left = left.rename('Value').reset_index()
# left.sort_values(['Value'],ascending=False,inplace=True)
# left = left.groupby(by=['Symptoms']).head(3)
#
# left = left[['Symptoms','Combination']]
# right = pd.DataFrame({'Symptoms':sym_list,
#                     'Combination':new_comb_list,
#                          'solved':sol})
#
# result = left.merge(right,how='left')
# result.groupby(by=['Symptoms','Combination','solved']).size().to_csv("RQ4_3_data.csv",index=True,sep=',')
#print(result)

#RQ5
rep = data['reputation']
rep = rep.fillna(value=0)

rep_list = []
for _rep in rep:
    if(not isinstance(_rep,int)):
        _rep = _rep.replace(',', '')
        if('k' in _rep):
            _rep = int(float(_rep.strip('k'))*1000)
    rep_list.append(_rep)
rep = Series(rep_list)
rep_sol = pd.DataFrame({'reputation': rep,'solved':sol})
rep_sol[['reputation']] = rep_sol[['reputation']].astype(int)

count0 = rep_sol[rep_sol['reputation'] == 0]
count1 = rep_sol[(rep_sol['reputation'] > 0) & (rep_sol['reputation'] <=3000)]
count2 = rep_sol[(rep_sol['reputation'] >3000) & (rep_sol['reputation'] <=6000)]
count3 = rep_sol[(rep_sol['reputation'] >6000) & (rep_sol['reputation'] <=9000)]
count4 = rep_sol[(rep_sol['reputation'] >9000) & (rep_sol['reputation'] <=12000)]
count5 = rep_sol[rep_sol['reputation'] > 12000]


group0 = count0.groupby(by=['solved']).size()
group1 = count1.groupby(by=['solved']).size()
group2 = count2.groupby(by=['solved']).size()
group3 = count3.groupby(by=['solved']).size()
group4 = count4.groupby(by=['solved']).size()
group5 = count5.groupby(by=['solved']).size()

group = pd.concat([group0.to_frame(),group1.to_frame(), group2.to_frame(), group3.to_frame(), group4.to_frame(), group5.to_frame()],axis=1, sort=True)
group = group.fillna(value=0)

#group.to_csv("RQ5_data.csv",index=True,sep=',')


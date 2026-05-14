import pandas as pd
from pandas import Series

#Use pandas to read data
data = pd.read_csv('./sample_Serialized.csv')

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
sol = data['accepted']
sol = Series(sol)
sol = sol.reset_index(drop=True)
rep_sol = pd.DataFrame({'reputation': rep,'solved':sol})
rep_sol[['reputation']] = rep_sol[['reputation']].astype(int)

# count0 = rep_sol[rep_sol['reputation'] == 0]
# count1 = rep_sol[(rep_sol['reputation'] > 0) & (rep_sol['reputation'] <=3000)]
# count2 = rep_sol[(rep_sol['reputation'] >3000) & (rep_sol['reputation'] <=6000)]
# count3 = rep_sol[(rep_sol['reputation'] >6000) & (rep_sol['reputation'] <=9000)]
# count4 = rep_sol[(rep_sol['reputation'] >9000) & (rep_sol['reputation'] <=12000)]
# count5 = rep_sol[rep_sol['reputation'] > 12000]

count0 = rep_sol[(rep_sol['reputation'] >= 0) & (rep_sol['reputation'] <=155)]
count1 = rep_sol[(rep_sol['reputation'] > 155) & (rep_sol['reputation'] <=450)]
count2 = rep_sol[(rep_sol['reputation'] >450) & (rep_sol['reputation'] <=1220)]
count3 = rep_sol[(rep_sol['reputation'] >1220) & (rep_sol['reputation'] <=3600)]
count4 = rep_sol[(rep_sol['reputation'] >3600) & (rep_sol['reputation'] <=11000)]
count5 = rep_sol[rep_sol['reputation'] > 11000]

group0 = count0.groupby(by=['solved']).size()
group1 = count1.groupby(by=['solved']).size()
group2 = count2.groupby(by=['solved']).size()
group3 = count3.groupby(by=['solved']).size()
group4 = count4.groupby(by=['solved']).size()
group5 = count5.groupby(by=['solved']).size()

group = pd.concat([group0.to_frame(),group1.to_frame(), group2.to_frame(), group3.to_frame(), group4.to_frame(), group5.to_frame()],axis=1, sort=True)
group = group.fillna(value=0)

group.to_csv("reputation_result2.csv",index=True,sep=',')
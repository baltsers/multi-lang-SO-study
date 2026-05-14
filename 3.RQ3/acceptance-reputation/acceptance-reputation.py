import pandas as pd
import scipy.stats
from pandas import Series

#Use pandas to read data
data = pd.read_csv('./answer.csv')


datasize = len(data['rep'].to_list())


accepted = []
unaccepted = []
for i in range(datasize):
    rep_list = data['rep'].to_list()[i].split(",")
    crt_ans = data['crt_ans'].to_list()[i]

    for i in range(len(rep_list)):
        if 'k' in rep_list[i]:
            rep_list[i] = rep_list[i].replace('k','000')
        if rep_list[i] == 'none':
            rep_list[i] = 0

    if (crt_ans == "no"):
        unaccepted = unaccepted + rep_list
    else:
        accepted.append(rep_list[int(crt_ans)-1])
        del rep_list[int(crt_ans)-1]
        unaccepted = unaccepted + rep_list

# accepted = list(map(int, accepted))
# unaccepted = list(map(int, unaccepted))

pd.core.frame.DataFrame(accepted).to_csv('accepted.csv')
pd.core.frame.DataFrame(unaccepted).to_csv('unaccepted.csv')

unacc_rep = pd.DataFrame({
    'acceptance':'0',
    'reputation': unaccepted
})

acc_rep = pd.DataFrame({
    'acceptance':'1',
    'reputation': accepted
})

acceptance_df = pd.concat([unacc_rep, acc_rep])
# acceptance_df.to_csv('test.csv')

# --------------
# The value in the daraframe should be object make the df.corr() get empty result
# --------------
# print(acceptance_df.info())
# acceptance_df = acceptance_df.apply(lambda x:x.astype(float))
acceptance_df['acceptance'] = acceptance_df['acceptance'].astype('int')
acceptance_df['reputation'] = acceptance_df['reputation'].astype('int')
# for i in range(len(acceptance_df['reputation'].to_list())):
#     if acceptance_df['reputation'].to_list()[i].isdigit():
#         acceptance_df['reputation'].to_list()[i] = acceptance_df['reputation'].to_list()[i]
#     else:
#         print("string value is not a digit:" + acceptance_df['reputation'].to_list()[i])
#         print("index:" + str(i))

result = acceptance_df.corr('spearman')
print(result)

print(scipy.stats.spearmanr(acceptance_df['reputation'], acceptance_df['acceptance']))
print(scipy.stats.pearsonr(acceptance_df['reputation'], acceptance_df['acceptance']))
print(scipy.stats.kendalltau(acceptance_df['reputation'], acceptance_df['acceptance']))


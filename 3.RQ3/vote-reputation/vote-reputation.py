import pandas as pd
import numpy as np
import scipy.stats


data = pd.read_csv('./answers-reputation.csv')

vote = data['answers_vote'].to_list()
reputation = data['answers_reputation'].to_list()

vote_output = []
reputation_output = []

need_del_index = []
for i in range(len(vote)):
    if str(vote[i]) == "nan" and str(reputation[i]) == "nan":
        need_del_index.append(i)
print(need_del_index)
for index in reversed(need_del_index):
    reputation.pop(index)
    vote.pop(index)

for i in range(len(vote)):
    vote_list = str(vote[i]).split(',')
    reputation_list = str(reputation[i]).split(',')
    vote_output += vote_list
    reputation_output += reputation_list

newdata = {
    'vote': vote_output,
    'reputation': reputation_output
}
df = pd.DataFrame(newdata)
# df.to_csv('vote-reputation.csv')

df['vote'] = df['vote'].astype('int')
df['reputation'] = df['reputation'].astype('int')

print(scipy.stats.spearmanr(df['vote'], df['reputation']))
print(scipy.stats.pearsonr(df['vote'], df['reputation']))
print(scipy.stats.kendalltau(df['vote'], df['reputation']))

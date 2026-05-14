import pandas as pd
from pandas import Series

data1 = pd.read_csv('./SO-2-tuple.csv')
data2 = pd.read_csv('./SO-3-tuple.csv')
data3 = pd.read_csv('./SO-4-tuple.csv')
olddata = pd.concat([data1,data2,data3])
olddata = olddata.reset_index()

liandata = pd.read_csv('./data_lian.csv',encoding='ANSI')


data = pd.read_csv('dataAllInfo.csv',encoding='ANSI')
max = 0
maxSample = data
for i in range(100):
    count = 0
    temp_sample = data.sample(frac=0.2)
    for index,row in liandata.iterrows():
        if (row['link'] in temp_sample['link'].tolist()):
            count += 1
            temp_sample.loc[temp_sample[temp_sample['link'] == row['link']].index, ['relevant']] = [row['relevant']]

    for index, row in olddata.iterrows():
        if (row['link'] in temp_sample['link'].tolist()):
            i += 1
            temp_sample.loc[temp_sample[temp_sample['link'] == row['link']].index, ['question contain code', 'Solution type',
                                                               'answer or highest vote', 'Symptoms ', 'SDLC',
                                                               'Special case', 'Taxonomy_Second', 'Taxonomy_Third']] = [
                row['question contain code'], row['Solution type'], row['answer or highest vote'], row['Symptoms '],
                row['SDLC'], row['Special case'], row['Taxonomy_Second'], row['Taxonomy_Third']]

    print(count)
    if count > max:
        max = count
        maxSample = temp_sample

print("---------------")
print(max)

maxSample.to_csv('sample_data.csv')
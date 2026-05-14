import pandas as pd

data = pd.read_csv('filterd_data.csv',encoding='ANSI')
print(data.head())
# sample = data.sample(n=50)
sample = data.sample(frac=0.2)
sample.to_csv('sample_data.csv')
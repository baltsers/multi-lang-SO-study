import pandas as pd

data = pd.read_csv('dataset_5,565posts.csv',encoding='latin-1')
print(data.head())
sample = data.sample(frac=0.2)
sample.to_csv('sample_data.csv')
import pandas as pd
from pandas import Series
from datetime import datetime

data = pd.read_csv('./accepted_answer.csv')

create_time_list = data['create time'].to_list()
accepted_time_list = data['accepted_time'].to_list()

create_time_list = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in create_time_list]
accepted_time_list = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in accepted_time_list]

accepted_duration = []

for i in range(len(accepted_time_list)):
    if accepted_time_list[i] >= create_time_list[i]:
        accepted_duration.append((accepted_time_list[i] - create_time_list[i]).seconds/3600)
    else:
        print("error index:"+str(i))


newdata = {
    'link': data['link'].to_list(),
    'accepted duration':accepted_duration,
}
df = pd.DataFrame(newdata)
df.to_csv('accepted answer time.csv')
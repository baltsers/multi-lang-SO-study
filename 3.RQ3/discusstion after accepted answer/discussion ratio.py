import pandas as pd
from datetime import datetime
import time

data = pd.read_csv('./discussion_time.csv')

accepted_time = data['accepted_time'].to_list()
answers_time = data['answers_time'].to_list()
comments_time = data['comments_time'].to_list()


time = []
ratio = []

# for period in [1,3,7,30,365,1825]:
for period in list(range(5,3655,5)):
    # print(period)
    count = 0
    for i in range(len(accepted_time)):
        # print(i)
        accepted_dt = datetime.strptime(str(accepted_time[i]),'%Y-%m-%d %H:%M:%SZ')

        discus = []

        if str(answers_time[i]) != "nan":
            answers_list = str(answers_time[i]).split(',')
            discus = discus + answers_list
            answers_list = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in answers_list]

        if str(comments_time[i]) != "nan":
            comments_list = str(comments_time[i]).split(',')
            discus = discus + comments_list
            comments_list = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in comments_list]

        discus = [datetime.strptime(dt, '%Y-%m-%d %H:%M:%SZ') for dt in discus]
        for dt in discus:
            if dt > accepted_dt and (dt - accepted_dt).days<period:
                count +=1
                break

    # print(count)
    time.append(period)
    ratio.append(count/(422-count))

newdata = {
    'time': time,
    'ratio':ratio
}
df = pd.DataFrame(newdata)
df.to_csv('ratio_bytime.csv')


import pandas as pd
from datetime import datetime
import time

data = pd.read_csv('./discussion_time.csv')

accepted_time = data['accepted_time'].to_list()
answers_time = data['answers_time'].to_list()
comments_time = data['comments_time'].to_list()



total_discus = []
after_accepted_discus = []
before_accepted_discus = []
active_period = []
after_accepted_comments = []
after_accepted_answers = []

for i in range(len(accepted_time)):
    print(i)
    accepted_dt = datetime.strptime(str(accepted_time[i]),'%Y-%m-%d %H:%M:%SZ')

    before = 0
    after = 0
    discus = []
    answers_after = 0
    comments_after = 0
    if str(answers_time[i]) != "nan":
        answers_list = str(answers_time[i]).split(',')
        discus = discus + answers_list
        answers_list = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in answers_list]
        for ans_date in answers_list:
            if ans_date >accepted_dt:
                answers_after += 1
    if str(comments_time[i]) != "nan":
        comments_list = str(comments_time[i]).split(',')
        discus = discus + comments_list
        comments_list = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in comments_list]
        for com_date in comments_list:
            if com_date > accepted_dt:
                comments_after += 1


    discus = [datetime.strptime(dt,'%Y-%m-%d %H:%M:%SZ') for dt in discus]
    for date in discus:
        if date > accepted_dt:
            after += 1
        else:
            before += 1

    total_discus.append(after+before)
    after_accepted_discus.append(after)
    before_accepted_discus.append(before)
    after_accepted_answers.append(answers_after)
    after_accepted_comments.append(comments_after)


    if after > 0:
        period = max(discus) -  accepted_dt
        active_period.append(period.days)
    else:
        active_period.append(0)

newdata = {
    'link': data['link'].to_list(),
    # 'comments time':comments_time,

    'total discus': total_discus,
    'after accepted discus': after_accepted_discus,
    'after accepted answers': after_accepted_answers,
    'after accepted comments': after_accepted_comments,
    # 'before accepted discus': before_accepted_discus,
    'active period': active_period
}
df = pd.DataFrame(newdata)
df.to_csv('discus_time_count.csv')



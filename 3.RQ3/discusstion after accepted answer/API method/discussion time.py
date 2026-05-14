from pprint import pprint
from stackapi import StackAPI
import pandas as pd
from datetime import datetime
import time

import json


data = pd.read_csv('../../discussion_time_miss_comment.csv')

postid_list = data['posts_id'].to_list()

link = []
accepted_ans_time = []
comments_time = []
total_comments = []
after_accepted_comments = []
before_accepted_comments = []
active_period = []

count = 1
no_comment_count = 0
datasize = len(postid_list)

SITE = StackAPI('stackoverflow')
for post_ids in postid_list:
    ids = post_ids.split(',')

    comments_json = SITE.fetch('posts/{ids}/comments', ids=ids, filter='withbody')
    answers_json = SITE.fetch('questions/{ids}/answers', ids=ids[0], filter='withbody')

    # qustion_json = SITE.fetch('questions/{ids}', ids=ids[0], filter='withbody')
    # question_stamp = qustion_json['items'][0]['creation_date']
    # question_creat_time = datetime.fromtimestamp(question_stamp)


    comments_list = []
    print("backoff:")
    print(comments_json['backoff'])
    print(answers_json['backoff'])
    for dic in comments_json['items']:
        comment_stamp = dic['creation_date']
        comment_creat_time = datetime.fromtimestamp(comment_stamp)
        comments_list.append(comment_creat_time)
    if len(comments_list) == 0:
        no_comment_count +=1
        print("no comment number:%d" % (no_comment_count))
        count += 1
        continue

    for dic in answers_json['items']:
        if dic['is_accepted'] == True:
            accepted_ans_time.append(datetime.fromtimestamp(dic['creation_date']))

    total_comments.append(len(comments_list))

    before = 0
    after = 0
    for dt in comments_list:
        if dt > accepted_ans_time[-1]:
            after += 1
        else:
            before += 1

    after_accepted_comments.append(after)
    before_accepted_comments.append(before)
    period = comments_list[0] - accepted_ans_time[-1]
    active_period.append(period.days)

    comments_list = [date_obj.strftime('%Y-%m-%d %H:%M:%S') for date_obj in comments_list]
    comments_time.append(comments_list)

    link.append(data['link'].to_list()[count-1])

    print("%d/%d"% (count, datasize))
    print('-----------------------')
    count +=1
    time.sleep(max(comments_json['backoff'], answers_json['backoff']) + 2)


newdata = {
    'link': link,
    'accepted ans time':accepted_ans_time,
    'comments time':comments_time,
    'total comments': total_comments,
    'after accepted comments': after_accepted_comments,
    'before accepted comments': before_accepted_comments,
    'active period': active_period
}
df = pd.DataFrame(newdata)
df.to_csv('comment_time.csv')
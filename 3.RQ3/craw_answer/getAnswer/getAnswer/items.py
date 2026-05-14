# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetanswerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # ans_num = scrapy.Field()
    # link = scrapy.Field()
    # accepted = scrapy.Field()
    # crt_ans = scrapy.Field()
    # rep = scrapy.Field()
    # time = scrapy.Field()
    # --------------------------- discussion time
    # link = scrapy.Field()
    # accepted_time = scrapy.Field()
    # comments_time = scrapy.Field()
    # answers_time = scrapy.Field()
    # posts_id = scrapy.Field()
    # ---------------------------vote-reputation
    # link = scrapy.Field()
    # answers_vote = scrapy.Field()
    # answers_reputation = scrapy.Field()
    #----------------------------viewed counts
    link = scrapy.Field()
    viewed_counts = scrapy.Field()
    pass

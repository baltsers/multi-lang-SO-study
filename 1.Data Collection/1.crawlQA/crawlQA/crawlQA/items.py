# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlqaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    vote = scrapy.Field()
    ans_num = scrapy.Field()
    viewed = scrapy.Field()
    active = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()
    reputation = scrapy.Field()
    combination = scrapy.Field()
    link = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    accepted = scrapy.Field()
    pass

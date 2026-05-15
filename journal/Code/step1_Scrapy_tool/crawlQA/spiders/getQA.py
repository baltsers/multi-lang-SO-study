import scrapy
import pandas as pd

from crawlQA.items import CrawlqaItem

count = 1
datasize = 0
class GetqaSpider(scrapy.Spider):
    name = 'getQA'

    def start_requests(self):
        # data = pd.read_csv('./filterd_data.csv', encoding='ANSI')
        # data = pd.read_csv('./reputation_list.csv', encoding='ANSI')
        data = pd.read_csv('./raw_data_10,444posts.csv')
        global datasize
        datasize = len(data['link'].to_list())

        for url in data['link'].to_list():
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = CrawlqaItem()
        item['title'] = response.xpath('//*[@id="question-header"]/h1/a/text()').extract()
        item['vote'] = response.xpath('//*[@class="question"]//*[@class="js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title"]/text()').extract()
        item['ans_num'] = response.xpath('//*[@class="answers-subheader d-flex ai-center mb8"]//*[@itemprop="answerCount"]/text()').extract()
        item['viewed'] = response.xpath('//*[@class="d-flex fw-wrap pb8 mb16 bb bc-black-075"]//*[@class="flex--item ws-nowrap mb8"]/text()').extract()[1]
        item['active'] = response.xpath('//*[@class="d-flex fw-wrap pb8 mb16 bb bc-black-075"]//*[@href="?lastactivity"]/@title').extract()
        item['time'] = response.xpath('//*[@class="postcell post-layout--right"]//*[@class="user-action-time"]/span/@title').extract()
        item['author'] = response.xpath('//*[@class="postcell post-layout--right"]//*[@class="post-signature owner flex--item"]//*[@class="user-details"]/a/text()').extract()
        reputation = response.xpath(
            '//*[@class="postcell post-layout--right"]//*[@class="post-signature owner flex--item"]//*[@class="user-details"]//*[@class="reputation-score"]/@title').extract()
        if (reputation[0] == "reputation score "):
            item['reputation'] = response.xpath('//*[@class="postcell post-layout--right"]//*[@class="post-signature owner flex--item"]//*[@class="user-details"]//*[@class="reputation-score"]/text()').extract()
        else:
            item['reputation'] = reputation

        item['combination'] = response.xpath('//*[@class="d-flex ps-relative"]/a/text()').extract()

        item['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()[0]

        question = response.xpath('//*[@class="question"]//*[@class="s-prose js-post-body"]')
        item['question'] = question.xpath('p/text()').extract()

        answers = response.xpath('//*[@id="answers"]')
        if (response.xpath('//*[contains(@class,"no-answers")]')):
            item['accepted'] = 'Undiscussed'
            item['answer'] = ' '
            yield item
        else:
            if (answers.xpath('//*[contains(@class,"answer accepted-answer")]')):
                item['accepted'] = 'Accepted'
            else:
                item['accepted'] = 'Undetermined'

        if (answers.xpath('//*[contains(@class,"answer accepted-answer")]')):
            item['answer'] = answers.xpath(
                '//*[@class="answer accepted-answer"]//*[@class="s-prose js-post-body"]/p/text()').extract()
        else:
            item['answer'] = answers.xpath('//*[@class="answer"][1]/div/div[2]/div[1]/p/text()').extract()

        global count
        print("-----------------------------------")
        print("%d/%d" % (count, datasize))
        print("-----------------------------------")
        count += 1

        yield item
        # pass

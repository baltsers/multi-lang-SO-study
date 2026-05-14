import scrapy
import pandas as pd
import re

from getAnswer.items import GetanswerItem

count = 1
datasize = 1742

class GetqaSpider(scrapy.Spider):
    name = 'getQA'

    def start_requests(self):
        # data = pd.read_csv('./filterd_data.csv', encoding='ANSI')
        data = pd.read_csv('../../../../../sample_Serialized.csv', encoding='ANSI')
        # data = pd.read_csv('../../../../../accepted posts.csv')
        # data = pd.read_csv('../../../../../extra-data.csv')
        global datasize
        datasize = len(data['link'].to_list())

        i = 0

        for url in data['link'].to_list():
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        item = GetanswerItem()
        item['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()[0]
        item['viewed_counts'] = response.xpath('//*[@class="d-flex fw-wrap pb8 mb16 bb bc-black-075"]//*[@class="flex--item ws-nowrap mb8"]/@title').extract()
        # ---------------------------------------------------------------------------------------------------------------------------------------------
        # viewed counts
        # ---------
        # item['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()[0]
        # if response.xpath('//*[@class="answers-subheader d-flex ai-center mb8"]//*[@itemprop="answerCount"]/text()').extract()[0] != 0:
        #     answer_vote = response.xpath('//div[contains(@class,"answer js-answer")]//div[contains(@class,"js-vote-count")]/text()').extract()
        #     for i in range(len(answer_vote)):
        #         answer_vote[i] = re.sub(r'\D','',answer_vote[i])
        #     item['answers_vote'] = answer_vote
        #
        #     reputation = response.xpath('//*[@data-position-on-page]//*[contains(@class,"flex--item fl0")]//*[@itemprop="author"]//*[@class="reputation-score"]/@title').extract()
        #     for i in range(len(item['answers_vote'])):
        #         if response.xpath('//*[@data-position-on-page="'+ str(i+1) +'"]//*[contains(@class,"flex--item fl0")]//*[@itemprop="author"]/div[@class="-flair"][not(span)]').extract() != [] or len(response.xpath('//*[@data-position-on-page="' + str(i + 1) + '"]//*[contains(@class,"flex--item fl0")]//*[@class="user-details"]//*[contains(text(),"community wiki")]').extract())>0 :
        #             reputation.insert(i, "0")
        #         else:
        #             continue
        #
        #     for i in range(len(reputation)):
        #         print(i)
        #         if (reputation[i] == "reputation score "):
        #             rep = response.xpath('//*[@data-position-on-page="'+ str(i+1) +'"]//*[contains(@class,"flex--item fl0")]//*[@itemprop="author"]//*[@class="reputation-score"]/text()').extract()
        #             reputation[i] = rep[0].replace(',','')
        #         else:
        #             reputation[i] = reputation[i].strip("reputation score ")
        #             reputation[i] = reputation[i].replace(',','')
        #             print(reputation[i])
        #
        #         item['answers_reputation'] = ','.join(reputation)
        # else:
        #     item['answers_vote'] = []
        #     item['answers_reputation'] = []

        # ---------------------------------------------------------------------------------------------------------------------------------------------
        # discussion time
        # ---------
        # item['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()[0]
        # item['accepted_time'] = response.xpath('//*[contains(@class,"answer accepted-answer")]//*[@class="user-action-time"]/span/@title').extract()
        # item['answers_time'] = response.xpath('//*[@data-position-on-page]//*[contains(@class,"flex--item fl0")]//*[@class="user-action-time"]/span/@title').extract()
        # # comments_list = response.xpath( '//a[not(contains(@title,"edits"))]//span[contains(@class,"relativetime")]/@title').extract()
        # comments_list = response.xpath('//*[@class="comment-date"]//span[contains(@class,"relativetime")]/@title').extract()
        # print(comments_list)
        # item['comments_time'] =comments_list
        # item['posts_id'] = response.xpath('//*[contains(@class,"gs8")]//*[@data-post-id]//@data-post-id').extract()
        # print(item['comments_time'])
        #---------------------------------------------------------------------------------------------------------------------------------------------
        # origin
        # ---------
        # item['title'] = response.xpath('//*[@id="question-header"]/h1/a/text()').extract()
        # item['vote'] = response.xpath('//*[@class="question"]//*[@class="js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title"]/text()').extract()
        # ans_num = response.xpath('//*[@class="answers-subheader d-flex ai-center mb8"]//*[@itemprop="answerCount"]/text()').extract()[0]
        # ans_num = len(response.xpath('//*[@data-position-on-page]//*[contains(@class,"flex--item fl0")]//*[@class="user-action-time"]/span/@title').extract())
        # item['ans_num'] = str(ans_num)

        # item['viewed'] = response.xpath('//*[@class="d-flex fw-wrap pb8 mb16 bb bc-black-075"]//*[@class="flex--item ws-nowrap mb8"]/text()').extract()[1]
        # item['active'] = response.xpath('//*[@class="d-flex fw-wrap pb8 mb16 bb bc-black-075"]//*[@href="?lastactivity"]/@title').extract()
        # item['time'] = response.xpath('//*[@class="postcell post-layout--right"]//*[@class="user-action-time"]/span/@title').extract()
        # item['author'] = response.xpath('//*[@class="postcell post-layout--right"]//*[@class="post-signature owner flex--item"]//*[@class="user-details"]/a/text()').extract()
        # reputation = response.xpath(
        #     '//*[@class="postcell post-layout--right"]//*[@class="post-signature owner flex--item"]//*[@class="user-details"]//*[@class="reputation-score"]/@title').extract()
        # if (reputation[0] == "reputation score "):
        #     item['reputation'] = response.xpath('//*[@class="postcell post-layout--right"]//*[@class="post-signature owner flex--item"]//*[@class="user-details"]//*[@class="reputation-score"]/text()').extract()
        # else:
        #     item['reputation'] = reputation
        #
        # item['combination'] = response.xpath('//*[@class="d-flex ps-relative"]/a/text()').extract()

        # item['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()[0]

        # question = response.xpath('//*[@class="question"]//*[@class="s-prose js-post-body"]')
        # item['question'] = question.xpath('p/text()').extract()


        # answers = response.xpath('//*[@id="answers"]')
        # if (response.xpath('//*[contains(@class,"no-answers")]')):
        #     item['accepted'] = 'Undiscussed'
        #     yield item
        # else:
        #     if (answers.xpath('//*[contains(@class,"answer accepted-answer")]')):
        #         item['accepted'] = 'Accepted'
        #     else:
        #         item['accepted'] = 'Undetermined'
        #
        #
        # found_crt_ans = False
        # for i in range(ans_num):
        #     if(response.xpath('//*[@data-position-on-page="'+ str(i+1) +'"]/@class').extract()[0] == "answer js-answer accepted-answer"):
        #         item['crt_ans'] = str(i+1)
        #         found_crt_ans = True
        #
        # if(found_crt_ans == False):
        #     item['crt_ans'] = "no"
        #
        # if(int(ans_num) != 0):
        #     # item['time'] = response.xpath('//*[@data-position-on-page]//*[@class="post-signature flex--item fl0"]//*[@class="user-action-time"]/span/@title').extract()
        #     item['time'] = response.xpath('//*[@data-position-on-page]//*[contains(@class,"flex--item fl0")]//*[@class="user-action-time"]/span/@title').extract()
        #
        #
        #     reputation = response.xpath('//*[@data-position-on-page]//*[contains(@class,"flex--item fl0")]//*[@itemprop="author"]//*[@class="reputation-score"]/@title').extract()
        #
        #     if(len(reputation) != ans_num):
        #         for i in range(ans_num):
        #             if (len(response.xpath('//*[@data-position-on-page="' + str(i + 1) + '"]//*[contains(@class,"flex--item fl0")]//*[@itemprop="author"]//*[contains(text(),"user")]').extract()) > 0 or len(response.xpath('//*[@data-position-on-page="' + str(i + 1) + '"]//*[contains(@class,"flex--item fl0")]//*[@class="user-details"]//*[contains(text(),"community wiki")]').extract())>0):
        #                 reputation.insert(i, "0")
        #
        #     print(reputation)
        #     for i in range(ans_num):
        #         print(i)
        #         if (reputation[i] == "reputation score "):
        #             rep = response.xpath('//*[@data-position-on-page="'+ str(i+1) +'"]//*[contains(@class,"flex--item fl0")]//*[@itemprop="author"]//*[@class="reputation-score"]/text()').extract()
        #             reputation[i] = rep[0].replace(',','')
        #         else:
        #             reputation[i] = reputation[i].strip("reputation score ")
        #             reputation[i] = reputation[i].replace(',','')
        #             print(reputation[i])
        #
        #     item['rep'] = ','.join(reputation)
        # else:
        #     item['time'] ="none"
        #     item['rep'] ="none"

        # if (answers.xpath('//*[contains(@class,"answer accepted-answer")]')):
        #     item['answer'] = answers.xpath(
        #         '//*[@class="answer accepted-answer"]//*[@class="s-prose js-post-body"]/p/text()').extract()
        # else:
        #     item['answer'] = answers.xpath('//*[@class="answer"][1]/div/div[2]/div[1]/p/text()').extract()

        global count
        print("-----------------------------------")
        print("%d/%d" % (count, datasize))
        print("-----------------------------------")
        count += 1

        yield item
        # pass

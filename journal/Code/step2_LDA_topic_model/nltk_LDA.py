import pandas as pd
from pandas import DataFrame
import re
import nltk
nltk.download('stopwords');nltk.download('brown');nltk.download('punkt');nltk.download('wordnet');nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from gensim import corpora, models

def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def CleanText(Text):
    Text = str(Text)
    Text = re.sub(r'[+|/]', ' and ', Text)
    Text = re.sub(r'[^\w\d,]', ' ', Text)
    Text = Text.lower()
    words = Text.split()
    words = [re.sub(r'[^a-z]', '', word) for word in words if word.isalnum()]
    Text = ' '.join(words)
    return Text

def Cleaning(Text, min_len=4):
    Text = CleanText(Text)
    words = nltk.word_tokenize(Text)
    # print(words)
    # print("--------------")
    # words = [lemmatizer.lemmatize(word) for word in words]
    pos_tagged = nltk.pos_tag(words)
    # print(words)
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
    newwords = []
    for word, tag in wordnet_tagged:
        if tag is None:
            newwords.append(word)
        else:
            # else use the tag to lemmatize the token
            newwords.append(lemmatizer.lemmatize(word, tag))
    words = [word for word in newwords if word not in stopwords.words('english') and len(word) > min_len]
    return words

def StartLDA(df):
    # tp_list = []
    # for index, row in df.iterrows():
    #     text_list = []
    #     text_list.append(Cleaning(row['issues being discuss']))
    #     text_list.append(Cleaning(row['solution']))
    #     tp_lda = LdaProc(text_list)
    #     tp_list.append(tp_lda)
    # df['Topics'] = tp_list
    # df.to_csv('Topics_rate0.05.csv')
    text_list = []
    print("Cleaning")
    for index, row in df.iterrows():
        text_list.append(Cleaning(row['question']))
        # text_list.append(Cleaning(row['solution']))
    print("Clean Finished")
    Rate_list, Tp_list = LdaProc(text_list)
    tpdf = {
        'rate':Rate_list,
        'topic':Tp_list
    }
    DataFrame(tpdf).to_csv('allTopics_top.csv')

def LdaProc(Text_list):
    if len(Text_list) == 0:
        return None
    Dictionary = corpora.Dictionary(Text_list)
    Corpus = [Dictionary.doc2bow(words) for words in Text_list]
    print("Running LDA Model")
    Lda = models.ldamodel.LdaModel(corpus=Corpus, id2word=Dictionary, num_topics=500,passes=30)#passes=3,15,10,20,30
    # Lda.save('data_lda.model')
    print(Lda.print_topic(50))
    Tp_list = []
    Rate_list = []
    # for i in range(3):
    #     Topic = Lda.print_topics(num_words=1)[i][1]
    #     Rate, Tp = RateTopic(Topic)
    #     if Rate < 0.001:
    #         continue
    #     else:
    #         Tp_list.append(Tp)
    #         Rate_list.append(Rate)
    print(len(Lda.print_topics(num_words=1)))
    for i in Lda.print_topics(num_topics=50,num_words=1):
        Topic = i[1]
        Rate, Tp = RateTopic(Topic)
        Tp_list.append(Tp)
        Rate_list.append(Rate)
    return Rate_list, Tp_list

def RateTopic(LdaStr):
    # "0.111*"accept"
    print(LdaStr)
    Rate, Topic = LdaStr.split("*")
    return float(Rate), eval(Topic)

data = pd.read_csv('dataset_10,444posts.csv',encoding='latin-1')

StartLDA(DataFrame(data))

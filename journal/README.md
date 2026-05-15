# Multi-Language Software Development: Issues, Challenges, and Solutions (Artifact)

This is the artifact of the paper *Multi-Language Software Development: Issues, Challenges, and Solutions* to appear in TSE 2023.


## 1. Getting started
### Environment preparation
1. Python version: 3.6 or upper version
2. Dependent libraries: scrapy, nltk, pandas, gensim.

Install the python dependencies via the following command:
```
pip install scrapy
pip install nltk
pip install pandas
pip install gensim
```

---
## 2. Directory structure
```
├─ README.md                                        <- readme file
│
├─SOICS.zip
│  ├─ Code                                          <- Code for all tool
│  │  ├─ step1_Scrapy_tool                          <- Used for crawling posts
│  │  │
│  │  ├─ step2_LDA_topic_model                      <- Used for getting development-
│  │  │                                               issue-relevant topic words
│  │  │
│  │  ├─ step3_Random_sampling_for_Codebook         <- Used for randomly getting 
│  │  │                                                codebook posts
│  │  │                                     
│  │  ├─ step4_Random_sampling_for_Coding_Process   <- Used for randomly getting 
│  │  │                                                coding process posts
│  │  │
│  │  └─ analysis_scripts                           <- Archived some analysis scripts 
│  │                                                   that were used and not used in paper 
│  │
│  └─ Data                                          <- Main dataset
│     ├─ CodeBook.xlsx                              <- Used for the categorization
│     │
│     ├─ raw_data_10,444posts.csv                   <- Filtering via tags and #vote
│     │
│     ├─ dataset_10,444posts.csv                    <- Getting the detail of posts
│     │                                   
│     ├─ dataset_5,565posts.csv                     <- Filtering via topic modeling (LDA) 
│     │
│     ├─ dataset_1,113posts.csv                     <- Random sampling for coding process
│     │   
│     ├─ dataset_586posts.csv                       <- Filtering via coding process
│     │   
│     ├─ dataset_586posts_coding_process.csv        <- Final result with the coding process draft (in column 'coding' and 'memo')
│     │
│     └─ Coding_book_draft.docx                     <- Meeting minutes draft of deriving the code book
│ 
└─ LICENSE.txt                                      <- license file

```

---
##3.Usage

First, unzip the SOICS.zip as root folder ```./SOICS```. 
Note that all the commands below should be executed from the root folder.

####In step1 Scrapy tool, 
```
cp ./Data/raw_data_10,444posts.csv  ./Code/step1_Scrapy_tool/
cd Code/step1_Scrapy_tool && scrapy crawl -o output.csv getQA
``` 
Then, the tool start to crawl data from StackOverflow.

####In step2 LDA topic model, 
```
cp ./Data/dataset_10,444posts.csv  ./Code/step2_LDA_topic_model/
cd Code/step2_LDA_topic_model && python nltk_LDA.py
```
Then, a new file will be generated named allTopics_top.csv, which contains the topics generated from all the posts in dataset_10,444posts.csv.

####In step3 Random sampling for Codebook, 
```
cp ./Data/dataset_5,565posts.csv  ./Code/step3_Random_sampling_for_Codebook/
cd Code/step3_Random_sampling_for_Codebook && python get_random_posts.py
```
Then, the file sample_data.csv will be generated, including about 495 posts used to generate the codebook.

####In step4 Random sampling for Coding Process,
```
cp ./Data/dataset_5,565posts.csv  ./Code/step4_Random_sampling_for_Coding_Process/
cd Code/step4_Random_sampling_for_Coding_Process && python get_random_posts.py
```
Then, the file sample_data.csv will be generated, including about 1,113 posts used for coding process.

---
##4.Summary
For **Data collection**, *./Code/* contains the tools used in it. And the datasets generated are saved in *./Data*.

For **RQ1**, analysis scripts used and not used in the paper are archived to *./Data/*.

For **RQ2** and **RQ3**, *./Data/dataset_586posts.csv* saves some raw results during manual analysis.
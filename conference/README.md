# Demystifying Issues, Challenges, and Solutions for Multilingual Software Development (Artifact)

This is the artifact of the paper *Demystifying Issues, Challenges, and Solutions for Multilingual Software Development* to appear in ICSE 2023.


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

To avoid issues with certain code not working properly, please verify that the environment satisfies the aforementioned requirements.

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
│     └─ dataset_586posts.csv                       <- Filtering via coding process
│        
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

Kindly be advised that this process could be time-consuming. We have restricted the data acquisition speed to prevent the misidentification of malware due to rapid collection.

####In step2 LDA topic model, 
```
cp ./Data/dataset_10,444posts.csv  ./Code/step2_LDA_topic_model/
cd Code/step2_LDA_topic_model && python nltk_LDA.py
```
Then, a new file will be generated named allTopics_top.csv, which contains the topics generated from all the posts in dataset_10,444posts.csv.

Please note that this process may take a long time. If you want to get the topics quickly, you can change the variables *(passes=30)* in line 81 of *python nltk_LDA.py*.

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
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import nltk

from config.config import Config
from nltk.collocations import *
from nltk.tokenize import word_tokenize

class IdentifyThreads:

    def __init__(self, folder_name, filename):
        config = Config(folder_name, filename)
        self.file_path = config.get_path_prefix_filename()
        self.folder_name = folder_name
        self.filename = filename
        print("Starting thread identification")

    def process(self):
        texts = pd.read_csv(f'{self.file_path}/{self.filename}_threads_pre_processado.csv', sep = '|')
        print("data loaded ....")

        # The dataset to be read must have the columns below to work.
        # The clean column refers to pre-processed text.
        # The column sent refers to the date and time of the message.
        # The username column refers to the username of the message.
        texts = texts[['id', 'text', 'clean', 'sent', "diff_date_user", 'username']]
        texts['sent'] = pd.to_datetime(texts['sent'])
        texts['chatroom'] = "" #Coluna adicionada
        texts['mention'] = 0
        texts['ngrams'] = 0
        texts['involved'] = 0
        texts['coupling'] = "" #Coluna adicionada
        texts = texts.fillna("")

        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(word_tokenize(' '.join(texts['clean'])))
        listBigrams = finder.nbest(bigram_measures.pmi, 10000) 
        sorted_listBigrams = np.array(listBigrams)
        sorted_listBigrams.sort(axis=1)
        unique_listBigrams = self.unique(sorted_listBigrams)

        texts['bigrams'] = ""
        for i in range(len(texts)):
            flag = False
            text = texts.iloc[i,2]
            keywords = ""
            if i % 1000 == 0:
                print(i," messages bigrams done ...")
            for bigram in unique_listBigrams:
                if bigram[0]+" "+bigram[1] in text or bigram[1]+" "+bigram[0] in text:
                    if(keywords == ""):
                        keywords = bigram[0]+" "+bigram[1] 
                    else:
                        keywords = keywords + ", " + bigram[0]+" "+bigram[1] 
            texts.iloc[i,9] =keywords
        print("bigrams done ....")

        identify_threads = self.identify_threads(texts)
        identify_threads.to_csv(fr"{self.file_path}/{self.filename}_threads_identificadas.csv", sep = '|')

    def unique(self, a):
        a = np.ascontiguousarray(a)
        unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
        return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

    def identify_threads(self, texts):

        texts['discussionId'] = [[] for _ in range(len(texts))]
        index = 0
        thread_id = 0
        thread_found = True
        for i in range(len(texts)):
            j = i
            starter = texts.iloc[i,3]
            ngram_group = list("")
            ngram_group += texts.iloc[i,11].split(',')
            involvement_group =list("")
            involvement_group.append(texts.iloc[i,5])
            if thread_found == True:
                thread_id += 1
                thread_found = False
            cutoff = 4
            counter = i + cutoff
            pairs = {}
            coupling_effect = False
            while (j < counter) :
                if j == len(texts)-1:
                    break
                j = j + 1
                last_matched = 0
                matching = ""
                mention = 0
                involved = 0
                existing = 0
                my_list = texts.iloc[j,11].split(',')
                if texts.iloc[j,5] in involvement_group: #involement group
                    involved = 1
                elif any(met in texts.iloc[j,1] for met in involvement_group): #mention from involvement group
                    mention = 1
                elif (ngram_group[0] != '' ) & (my_list[0] != ''): # matching Bi-grams
                    matching = [s for s in ngram_group if any(xs in s for xs in my_list)]
                #back and forth user pattern
                pattern = texts.iloc[j-1,5]+","+texts.iloc[j,5]
                if pairs.get(pattern):
                    pairs[pattern] = pairs.get(pattern) + 1
                else:
                    pairs[pattern] = 1
                user = ""
                for key,value in pairs.items():
                    if value >= 3:
                        users = key.split(",")
                        for u in users:
                            if not u in involvement_group:
                                user = u
                                involvement_group.append(u)
                                coupling_effect = True
                if coupling_effect:
                    coupling_effect = False
                    for k in range(j, i, -1): 
                        if texts.iloc[k,5] == user:
                            texts.iloc[k,12].append(thread_id)
                            texts.iloc[k,10] = 1
                if (mention == 1) | (involved == 1) | (len(matching) > 0):
                    texts.iloc[j,7] = mention
                    texts.iloc[j,8] = len(matching)
                    texts.iloc[j,9] = involved
                    existing = any(i in texts.iloc[j,12] for i in texts.iloc[i,12])
                    if (thread_id not in texts.iloc[j,12]) & (existing == 0):
                        texts.iloc[j,12].append(thread_id)
                        thread_found = True
                        last_matched = j
                    if (thread_id not in texts.iloc[i,12]) & (existing == 0):
                        texts.iloc[i,12].append(thread_id)
                        last_matched = j
                    if thread_found == True:
                        involvement_group.append(texts.iloc[j,5])
                        ngram_group += texts.iloc[j,11].split(',')
                if ((j == counter)) & (last_matched != 0):
                    if (counter - last_matched <= 2) :
                        counter += 4
                        index+=1
        return texts
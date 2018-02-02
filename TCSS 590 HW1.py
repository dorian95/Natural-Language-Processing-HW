# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 22:57:50 2018

TCSS 590 HW1
@author: Nursultan
"""

import nltk
from nltk import word_tokenize

import glob2

filenames = glob2.glob('./Neg/*.txt')  # list of all .txt files in the directory

#Import NEGATIVE
with open('all_neg.txt', 'w') as f:
    for file in filenames:
        with open(file) as infile:
            f.write(infile.read()+'\n')
            
neg_txt = open('all_neg.txt')
neg = neg_txt.read()           

filenames = glob2.glob('./Pos/*.txt')  # list of all .txt files in the directory

#Import POSITIVE
with open('all_pos.txt', 'w') as f:
    for file in filenames:
        with open(file) as infile:
            f.write(infile.read()+'\n')

pos_txt = open('all_pos.txt')
pos = pos_txt.read()

from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

neg = neg.lower()
#tokens_neg = word_tokenize(neg)
# including regular expressions
tokens_neg = tokenizer.tokenize(neg)

print("# of negative tokens=", len(tokens_neg))

pos = pos.lower()
#tokens_pos = word_tokenize(pos)
# including regular expressions
tokens_pos = tokenizer.tokenize(pos)
print("# of positive tokens=", len(tokens_pos))


#remove English stopwords from both texts
from nltk.corpus import stopwords

stops = set(stopwords.words("english"))
tokens_neg_clean = [word for word in tokens_neg if word not in stops]
tokens_pos_clean = [word for word in tokens_pos if word not in stops]
print("# of clean negative tokens", len(tokens_neg_clean))
print("# of clean positive tokens", len(tokens_pos_clean))
      
total_tokens = tokens_neg_clean + tokens_pos_clean
print("Answer for question1: ", len(total_tokens))

print("Answer for question2: ", len(set(total_tokens)))

freq_distr_unigram = nltk.FreqDist(total_tokens)
#print(freq_distr_unigram.most_common(10))
#print(freq_distr_unigram['movie'])

#QUESTION 3
bigrams = nltk.bigrams(tokens_pos_clean+tokens_neg_clean)
#compute frequency distribution for all the bigrams in the text
freq_distr_bigram = nltk.FreqDist(bigrams)
top10_bigrams_freq = freq_distr_bigram.most_common(10)
#just the bigrams without the freq-cy
top10_bigrams = [x[0] for x in top10_bigrams_freq]
print('Top 10 bigrams and their frequencies:')
print(top10_bigrams_freq)

trigrams = nltk.trigrams(tokens_pos_clean+tokens_neg_clean)
#compute frequency distribution for all the bigrams in the text
freq_distr_trigrams = nltk.FreqDist(trigrams)
top10_trigrams_freq = freq_distr_trigrams.most_common(10)
print('Top 10 trigrams and their frequencies:')
#just the trigrams without the frequencies
top10_trigrams = [x[0] for x in top10_trigrams_freq]
print(top10_trigrams_freq)

#QUESTION 4
# I will use Laplace smoothing (parameter = 0.1)
prev_words = {}
for t in total_tokens[1: len(total_tokens) -1]:
    if t not in prev_words:
        prev_words[t] = 1
    else:
        prev_words[t] += 1
        
bigrams = [(total_tokens[n], total_tokens[n+1]) for n in range(1, len(total_tokens)-1)]

#print("Question #4 bigrams count", len(bigrams)) 
bigram_counts_laplace = {}
for bigram in bigrams:
    if bigram not in bigram_counts_laplace:
        bigram_counts_laplace[bigram] = 1.1
    else:
        bigram_counts_laplace[bigram]+=1

#print(bigram_counts_laplace[('coast', 'guard')])

bigram_probs_laplace = {}
for k,v in bigram_counts_laplace.items():
    bigram_probs_laplace[(k[1], k[0])] = v / (prev_words[k[0]] + 0.1*len(prev_words))

#print(bigram_probs_laplace[('guard', 'coast')])

prev_2words = {}
for t in bigrams:
    if t not in prev_2words:
        prev_2words[t] = 1
    else:
        prev_2words[t] += 1

#print(prev_2words[('costner', 'movie')])     

trigram_counts_laplace = {}
for trigram in trigrams:
    if trigram not in trigram_counts_laplace:
        trigram_counts_laplace[trigram] = 1.1
    else:
        trigram_counts_laplace[trigram]+=1
		
print("FOR SOME REASON THIS CODE DOESN'T WORK HERE")
print("But it works in my JUPYTER NOTEBOOK")
#print(trigram_counts_laplace[('br','br', 'movie')])

trigram_probs_laplace = {}
for k,v in trigram_counts_laplace.items():
    trigram_probs_laplace[(k[2],k[0], k[1])] = v / (prev_2words[(k[0], k[1])] + 0.1*len(prev_2words))
    #print(prev_2words[(k[0], k[1])])

#FUNCTION TO GET PROBABILITY of a word using TRIGRAM LM
def get_trigram_prob(w1, w2, w3):
    return trigram_probs_laplace[w3, w1,w2]

print(len(trigram_probs_laplace))

#QUESTION 5
print(get_trigram_prob('costner', 'dragged', 'movie'))
print(get_trigram_prob('overconfident', 'ashton', 'kutcher'))
print(get_trigram_prob('characters', 'us', 'ghosts'))
print(get_trigram_prob('far','longer', 'necessary'))
print(get_trigram_prob('care', 'characters', 'us'))
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 21:46:08 2018


TCSS 590
HW2
@author: Nursultan
"""

from nltk import word_tokenize
import pandas as pd

import nltk

trans_prob = {}
trans_prob[('START', 'START')] = 0.0
trans_prob[('START', 'N')] = 0.2
trans_prob[('START', 'V')] = 0.3
trans_prob[('START', 'ADV')] = 0
trans_prob[('START', 'STOP')] = 0
trans_prob[('N', 'N')] = 0.1
trans_prob[('N', 'V')] = 0.3
trans_prob[('N', 'ADV')] = 0.1
trans_prob[('N', 'STOP')] = 0
trans_prob[('N', 'START')] = 0
trans_prob[('V', 'N')] = 0.3
trans_prob[('V', 'ADV')] = 0.4
trans_prob[('V', 'STOP')] = 0
trans_prob[('V', 'V')]  = 0.1
trans_prob[('V', 'START')]  = 0
trans_prob[('ADV', 'N')] = 0
trans_prob[('ADV', 'V')] = 0
trans_prob[('ADV', 'ADV')] =0 
trans_prob[('ADV', 'STOP')] = 0.1
trans_prob[('ADV', 'START')] = 0
trans_prob[('STOP', 'N')] = 0
trans_prob[('STOP', 'V')] = 0
trans_prob[('STOP', 'ADV')] = 0
trans_prob[('STOP', 'START')] = 0
trans_prob[('STOP', 'STOP')] = 0
trans_prob = pd.Series(trans_prob)
print(trans_prob.unstack(level=-1))


emis_prob = {('learning', 'V'): 0.003,
             ('learning', 'ADV'): 0,
             ('learning', 'N'): 0.001,
             ('learning', 'STOP'): 0,
             ('changes', 'STOP'): 0,
             ('throughly', 'STOP'): 0,
             ('changes', 'STOP'):0,
             ('changes', 'V'): 0.004,
             ('changes', 'ADV'): 0,
             ('throughly', 'ADV'): 0.002,
             ('throughly', 'N'): 0,
             ('throughly', 'V'): 0,
             ('changes', 'N'): 0.003,
             ('START', 'START'): 0,
             ('START', 'N'): 0,
             ('START', 'ADV'): 0,
             ('START', 'STOP'): 0,
             ('START', 'V'):0,
             ('STOP', 'START'): 0,
             ('STOP', 'N'): 0,
             ('STOP', 'V'): 0,
             ('STOP', 'ADV'): 0,
             ('STOP', 'STOP'):0,
             ('learning', 'START'): 0,
             ('changes', 'START'): 0,
             ('throughly', 'START'): 0
           }
emis_prob = pd.Series(emis_prob)
print(emis_prob.unstack())

test = "learning changes throughly"
pos = ['START', 'N', 'V', 'ADV', 'STOP']
test_list = test.split(' ')
position_dict = {}
result_dict = {}
curr_pos = {}

for i in range(len(test_list)):
    for j in range(len(pos)):
        position_dict[(i,j)] = (test_list[i], pos[j])
print(position_dict)

for i in range(len(test_list)):
    for j in range(len(pos)):
        if i == 0:
            result_dict[(i,j)] = trans_prob[('START', pos[j])] * emis_prob[(test_list[i], pos[j])]  
        else:
            max_prev = 0
            for k in range(len(pos)):
                curr = result_dict[(i-1,k)] * trans_prob[(pos[k], pos[j])] 
                if (curr > max_prev):
                    max_prev = curr
                    curr_pos[(i,j)] = (i-1,k)
                    #print(str(i - 1) + ": i " + str(trans_prob[(pos[j], pos[k])]) + " " + str(result_dict[(i-1,k)])) 
                    #print(str(k) + ": j")
            result_dict[(i,j)] = max_prev * emis_prob[(test_list[i], pos[j])]
            #print("end")

max = 0
for n in range(len(pos)):
    if result_dict[2, n] > max:
        max = result_dict[2,n]
        save = n
result_list = []        
index = 2
result_list.append(pos[save])

while (index > 0):
    result_list.append(pos[curr_pos[(index, save)][1]])
    save = curr_pos[(index, save)][1]
    index = index - 1
result_list.reverse()

result_dict = pd.Series(result_dict)
result_dict.unstack()
print("\n")
print("POS tags: ",result_list)

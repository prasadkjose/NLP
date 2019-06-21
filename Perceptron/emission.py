import sys
import numpy as np
from collections import namedtuple

# countsfile = sys.argv[1]


def initemision_probability(fr,count={}, Counttag={}): #calculates the word emmission probabilities
    words = namedtuple("word", ["tag", "word"]) #format of the output 
    emmision = {}
    with open(fr, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) != 0:
                w = line.split(" ")
                #calculate the counts of occurrance of words in each class
                if w[1] == "WORDTAG":
                    if count.get(w[3]):
                        count[w[3]] = count[w[3]] + float(w[0])
                    else:
                        count[w[3]] = float(w[0])
                        
                    if Counttag.get(w[2]):
                        Counttag[w[2]] = Counttag[w[2]] + float(w[0])
                    else:
                        Counttag[w[2]] = float(w[0])
                    
    #Count The rare items in the dev set
    count['__RARE__'] = 0
    for word in count:
        if count[word] < 5 and word != '__RARE__':
            count['__RARE__'] = count['__RARE__'] + count[word]
            count[word] = 0
    #calculate the emmission probabilities                   
    with open(fr, 'r') as g:
        for line in g:
            line = line.strip()
            if len(line) != 0:
                w = line.split(" ")
                if w[1] == "WORDTAG":
                    if count[w[3]] < 5:
                        w[3] = "__RARE__"
                    if emmision.get(words(w[2],w[3])):
                        emmision[words(w[2],w[3])] = 0
                    else:
                        emmision[words(w[2],w[3])] = 0
    return emmision
# print (emision_probability(countsfile))





# def emision_probability(fr,count={}, Counttag={}): #calculates the word emmission probabilities
#     words = namedtuple("word", ["tag", "word"]) #format of the output 
#     emmision = {}
#     with open(fr, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if len(line) != 0:
#                 w = line.split(" ")
#                 #calculate the counts of occurrance of words in each class
#                 if w[1] == "WORDTAG":
#                     if count.get(w[3]):
#                         count[w[3]] = count[w[3]] + float(w[0])
#                     else:
#                         count[w[3]] = float(w[0])
                        
#                     if Counttag.get(w[2]):
#                         Counttag[w[2]] = Counttag[w[2]] + float(w[0])
#                     else:
#                         Counttag[w[2]] = float(w[0])
                    
#     #Count The rare items in the dev set
#     count['__RARE__'] = 0
#     for word in count:
#         if count[word] < 5 and word != '__RARE__':
#             count['__RARE__'] = count['__RARE__'] + count[word]
#             count[word] = 0
#     #calculate the emmission probabilities                   
#     with open(fr, 'r') as g:
#         for line in g:
#             line = line.strip()
#             if len(line) != 0:
#                 w = line.split(" ")
#                 if w[1] == "WORDTAG":
#                     if count[w[3]] < 5:
#                         w[3] = "__RARE__"
#                     if emmision.get(words(w[2],w[3])):
#                         emmision[words(w[2],w[3])] = emmision[words(w[2],w[3])] + (float(w[0])/Counttag[w[2]])
#                     else:
#                         emmision[words(w[2],w[3])] = (float(w[0])/Counttag[w[2]])
#     return emmision

import sys
import numpy as np
import emission
from collections import namedtuple
import transition


Element = namedtuple("Element", ["tag", "word"])
count = {} #Count is a global Dic with the count of each word in the dev set
# Counttag = {}   

# countsfile = sys.argv[1]

# tags = ["GENE","NOGENE","*","STOP"]
# n = len(tags)
# ****************** The viterbi function***************8 
def viterbi(words, emmision, tri, tags, n):
    lengSen = len(words)
    word = [words[x] for x in range(len(words))]
    trigram = namedtuple("trigram", ["first", "second", "third"]) 
    # bigram = namedtuple("bigram", ["first", "second"]) 
    for i in range(len(words)):       
        if count.get(words[i]):
            if count[words[i]] < 5:  #if the word count is < 5 
                word[i] = "__RARE__"
        else:                            
            word[i] = "__RARE__"        #if the word is not in the training set
    transitionMatrix = [[[0 for x in range(n)] for x in range(n)]for x in range(lengSen + 1)]
    matrix = [[[0 for x in range(n)] for x in range(n)]for x in range(lengSen + 1)]
    for i in range(n):
        for j in range(n):
            transitionMatrix[0][i][j] = 0
    transitionMatrix[0][n-2][n-2] = 1

    y = [0 for x in range (lengSen+1)]
#find all possible trigrams if exists in the sentence and get the emission prob
    for k in range(1,lengSen+1): #for every sentence
        for u in range(n):
            for v in range(n):
                transitionMatrix[k][u][v] = 0
                for w in range(n):
                    t = 0
                    
                    if tri.get(trigram(tags[w],tags[u],tags[v])) and emmision.get(Element(tags[v],word[k-1])):
                        t = transitionMatrix[k-1][w][u]*tri[trigram(tags[w],tags[u],tags[v])]*emmision[Element(tags[v],word[k-1])]
                        #check max prob of a tag sequence ending in tags u,v at position k of the sentence
                        if(t > transitionMatrix[k][u][v]):
                            matrix[k][u][v] = w
                            transitionMatrix[k][u][v] = t
    curr = 0

    for u in range(n):
        for v in range(n):
            if tri.get(trigram(tags[u],tags[v],'STOP')):
                t = transitionMatrix[lengSen][u][v]*tri[trigram(tags[u],tags[v],'STOP')]
                #check max prob of a tag sequence ending in STOP

                if(t > curr):
                    curr = t
                    y[lengSen-1] = u
                    y[lengSen] = v
                    
    for k in list(reversed(range(1,lengSen-1))):
        y[k] = matrix[k+2][y[k+1]][y[k+2]]
    return y 
    

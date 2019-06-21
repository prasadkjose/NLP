import sys
import numpy as np
from collections import namedtuple
import transition
import emission
import viterbi
import time


devFile = sys.argv[2]
devW = []
countsfile = sys.argv[1]
"Init Alpha Params"

alpha_emision = emission.initemision_probability(countsfile)
alpha_trans = transition.inittransitionProb(countsfile)
trigram = namedtuple("trigram", ["first", "second", "third"]) 
words = namedtuple("word", ["tag", "word"]) #format of the output
 
def Perceptron(s):
    global alpha_emision
    global alpha_trans
    tags = ["GENE","NOGENE","*","STOP"]
    n = len(tags)
    z = viterbi.viterbi(s,alpha_emision,alpha_trans, tags, n)
    c1 = {} 
    c2 = {} 
    c3={}
    c4 = {}
    #sequence using viterbi on train and raw train tags
    Viterbiseq ={}
    for i in range(1,len(z)-1):
        Viterbiseq[trigram(tags[z[i]],tags[z[i+1]],tags[z[i+1]])] = 0
    tagSeq = {}
    t1=[]
    for i in s:
        t =i.split(" ")
        t1.append(t[1])
    for i in range(len(t1)-2):
        tagSeq[trigram(t1[i],t1[i+1],t1[i+2])] = 0
    # print(tagSeq)
    # print(Viterbiseq)
    for i in range(1,len(s)):        
        for u in range(n):
            for v in range(n):
                for w in range(n):                                      
                        c1[trigram(tags[w],tags[u],tags[v])] = 0
                        c2[trigram(tags[w],tags[u],tags[v])] = 0
    for i in range(1,len(s)):        
        for u in range(n):
            for v in range(n):
                for w in range(n):                                      
                    if trigram(tags[w],tags[u],tags[v]) in tagSeq :
                        c2[trigram(tags[w],tags[u],tags[v])] += 1
                    if trigram(tags[w],tags[u],tags[v]) in Viterbiseq :
                        c1[trigram(tags[w],tags[u],tags[v])] += 1
                    if c1.get(trigram(tags[w],tags[u],tags[v])) != c2.get(trigram(tags[w],tags[u],tags[v])):
                        alpha_trans[tags[w],tags[u],tags[v]] += c1.get(trigram(tags[w],tags[u],tags[v]))-c2.get(trigram(tags[w],tags[u],tags[v]))
    wordTagSeq={}
    wordTagVit={}           
    for i in range(1,len(z)):
        t =s[i-1].split(" ")
        wordTagSeq[words(t[1],t[0])]=0
        wordTagVit[words(tags[z[i]],t[0])]=0
    # print(wordTagSeq)
    # print("\n")
    # print(wordTagVit)
    for i in s:
        for j in tags: 
            c3[words(j,i)] =0
            c4[words(j,i)] =0
    for i in s:
        for j in tags: 
            if words(j,i) in  wordTagSeq:
                c3[words(j,i)] += 1
            if words(j,i) in  wordTagVit:
                c4[words(j,i)] += 1
            if c3.get(words(j,i)) != c4.get(words(j,i)):
                alpha_emision+= c3.get(words(j,i)) - c4.get(words(j,i)) 


start_time = time.time()
    
with open(devFile, 'r') as f:
    for line in f:
        line = line.strip()

        if len(line) != 0:
            devW.append(line)
        else:
            Perceptron(devW)
            devW = []

            
            

            # for i in range(1,len(z)):
            #     sys.stdout.write(  devW[i-1] + " " + tags[z[i]] + "\n")
            # sys.stdout.write("\n")

print((time.time()-start_time)/60)

# print(alpha_emision)
# print(alpha_trans)
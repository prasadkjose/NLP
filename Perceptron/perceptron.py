import sys
import numpy as np
from collections import namedtuple
import transition
import viterbi
import time
import json
import emission

devFile = sys.argv[2]
devW = []
countsfile = sys.argv[1]
"Init Alpha Params"


alpha_emision = emission.initemision_probability(countsfile)
alpha_trans = transition.inittransitionProb(countsfile)
trigram = namedtuple("trigram", ["first", "second", "third"]) 
words = namedtuple("word", ["tag", "word"]) 
tags = ["GENE","NOGENE","*","STOP"]
c1 = {} 
c2 = {} 
c3 = {}
c4 = {}
n = len(tags)

class Perceptron :
    def __init__(self, s):
        self.c1 = {} 
        self.c2 = {} 
        self.c3 = {}
        self.c4 = {}
        global trigram
        global words
        global tags  
        global n 
        self.z = viterbi.viterbi(s,alpha_emision,alpha_trans, tags, n)
        self.wordTagSeq={}
        self.wordTagVit={} 
        self.Viterbiseq ={}
        # print(self.z)
        
        for i in range(len(self.z)-2):            
            self.Viterbiseq[trigram(tags[self.z[i]],tags[self.z[i+1]],tags[self.z[i+2]])] = 0

        self.tagSeq = {}
        t1=[]
        for i in s:
            t =i.split(" ")
            t1.append(t[1])
        for i in range(len(s)-2):
            self.tagSeq[trigram(t1[i],t1[i+1],t1[i+2])] = 0
        # print(self.Viterbiseq, "--> viterbi seq")
        # print(self.tagSeq,"--> ti seq")

        for i in range(1,len(self.z)):
            t =s[i-1].split(" ")
            self.wordTagSeq[words(t[1],t[0])]=0
            self.wordTagVit[words(tags[self.z[i]],t[0])]=0

    # def initAlpha_emision(self,s):
    #     for i in s:
    #         for j in tags: 
    #             t =i.split(" ")
    #             alpha_emision[words(j,t[0])] =0
 
    def initCVlas(self, s):       
        for i in range(0,len(s)):        
                for u in range(n):
                    for v in range(n):
                        for w in range(n):                                      
                                self.c1[trigram(tags[w],tags[u],tags[v])] = 0
                                self.c2[trigram(tags[w],tags[u],tags[v])] = 0
        for i in s:
            for j in tags: 
                t =i.split(" ")
                self.c3[words(j,t[0])] =0
                self.c4[words(j,t[0])] =0

    def CalcAlphaTrans(self, s,):
        for i in range(1,len(s)):        
                for u in range(n):
                    for v in range(n):
                        for w in range(n):                                      
                            if trigram(tags[w],tags[u],tags[v]) in self.tagSeq :
                                self.c2[trigram(tags[w],tags[u],tags[v])] += 1
                            if trigram(tags[w],tags[u],tags[v]) in self.Viterbiseq :
                                self.c1[trigram(tags[w],tags[u],tags[v])] += 1
                            
        for i in range(1,len(s)):        
            for u in range(n):
                for v in range(n):
                    for w in range(n):                                      
                        if self.c1.get(trigram(tags[w],tags[u],tags[v])) != self.c2.get(trigram(tags[w],tags[u],tags[v])):
                            alpha_trans[tags[w],tags[u],tags[v]] += self.c1.get(trigram(tags[w],tags[u],tags[v]))-self.c2.get(trigram(tags[w],tags[u],tags[v]))                

    def CalcAlphaEmision(self,s):
        # self.initAlpha_emision(s)
        for i in s:
            for j in tags: 
                t =i.split(" ")
                 
                if words(j,t[0]) in  self.wordTagSeq:
                    # print("yayy")
                    self.c3[words(j,t[0])] += 1
                if words(j,t[0]) in  self.wordTagVit:
                    self.c4[words(j,t[0])] += 1
                
        for i in s:
            for j in tags: 
                t =i.split(" ")
                if self.c3.get(words(j,t[0])) != self.c4.get(words(j,t[0])):
                    alpha_emision[j,t[0]]+= self.c3.get(words(j,t[0])) - self.c4.get(words(j,t[0])) 
                    # alpha_emision[j,i[0]]
start_time = time.time()
lines = []

with open(devFile, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) != 0:
                devW.append(line)
            else:
                lines.append(devW)
                devW = []  

i = 0
while(i<1) :   
    print(i , "--> Iteration")
    for j in lines:
        p = Perceptron(j)
        p.initCVlas(j)
        p.CalcAlphaEmision(j)
        p.CalcAlphaTrans(j)          
    i+=1


# print(alpha_emision)
# print(alpha_trans)
print((time.time()-start_time)/60)

with open('trans.alpha', 'w') as outfile:
    print(alpha_trans, file=outfile)
with open('emission.alpha', 'w') as outfile:
    print(alpha_emision, file=outfile)
# sys.stdout.write( str(alpha_emision)+ "\n"+ "\n" + str(alpha_trans)  )

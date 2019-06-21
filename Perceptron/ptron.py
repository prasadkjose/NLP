from tagger import *
from collections import defaultdict
import time
import sys
import random
class Perceptron(viterbiDec):

    def Ptron(self, train_file):
        c = train_corpus(train_file)
        lst = list(c)
        random.shuffle(lst)
        
        # print(c)
        for sen in lst:
            tags = self.viterbi(sen[0])            
            g = countFeatures(sen[0], tags)
            b = countFeatures(sen[0], sen[1])
            self.set_diff(g, b)

    def learn(self, train_file):
        out = open("out.alpha", "w")
        for i in range(5):
            print(i)
            self.Ptron(train_file)
        #normalizing the aplha vals
        a= 0
        for k,v in self.alpha.items():
            a+=v
        factor=1.0/a

        for k,v in self.alpha.items():
            v = v*factor
            if v != 0.0:
                out.write(k + " " + str(v) + "\n")
        # print(self.alpha)
            

    def set_diff(self, ViterbiSen, TestSen):
 
        for a in TestSen:
            self.alpha[a] += TestSen[a]
            if self.alpha[a]< 0.0:
                self.alpha[a] = 0.00000001
            
        for a in ViterbiSen:
            self.alpha[a] -= ViterbiSen[a]
            if self.alpha[a]< 0.0:
                self.alpha[a] = 0.00000001
start_time = time.time()
  
if __name__ == "__main__":
    p = Perceptron()
    file1 = sys.argv[1]
    p.learn(file1)
    p.tagger("gene.dev")
print((time.time()-start_time))
 
 
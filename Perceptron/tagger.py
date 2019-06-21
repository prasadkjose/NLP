from collections import defaultdict
import random

#read Test files
def test(file_name):
    f = open(file_name, "r")
    curr = []
    for line in f:
        if len(line.strip()) == 0:
            yield curr
            curr = []
        else:
            curr.append(line.strip())

#read train files
def train_corpus(file_name):
    # lines = open(file_name).readlines()
    # random.shuffle(lines)
    # print(len(lines))
    f = open(file_name, "r")
    sen = [[], []]
   
    for line in f:
        # print(line)
        line = line.split()
        if len(line) == 0:
            yield sen
            sen = [[], []]

        else:
            line[-1] = line[-1].strip()
            sen[0].append(line[0])
            sen[1].append(line[1])

#add wordtags and trigram feats
def features(t, u, sen, i, s):

    g = list()
    g.append("TRIGRAM:" + t + ":" + u + ":" + s)
  
    if i != len(sen):
      
        g.append(sen[i] + " " + s)

    return g

#init feat counts to 1(used in viterbi)
def countFeatures(sen, tags):
    g = defaultdict(int)
    tags = ["*", "*"] + tags + ["STOP"]

    for i in range(len(tags) - 2):
        g["TRIGRAM:" + tags[i] + ":" + tags[i + 1] + ":" + tags[i + 2]] = 1

    for u, v in zip(sen, tags):
        g[u + " " + v] = 1

    return g

#viterbi decoder during and after perceptron
class viterbiDec :
    def __init__(self):
        self.alpha = defaultdict(float)
        self.states = [ "NOGENE","GENE"]

    def read_alpha(self):
        f = open("out.alpha", "r")
        for line in f:
            line = line.split()
            line[-1] = line[-1].strip()
            key = line[0]
            self.alpha[key] = float(line[-1])

    def tagger(self, file_name):
        ite = test(file_name)
        self.read_alpha()

        out = open("dev.out", "w")
        for sen in ite:
            tags = self.viterbi(sen)
            for i in range(len(sen)):
                out.write(sen[i] + " " + tags[i] + "\n")
            out.write("\n")

    def viterbi(self, sen):
        n = len(sen)
        # self.read_alpha()
        
        tags = [""] * n
        tri = defaultdict(float)
        tri[-1, "*", "*"] = 0.0
        bp = defaultdict(str)
        
        for i in range(n):
            s0 = self.states
            if i - 1 < 0:
                s1 = ["*"]
            else:
                s1 = self.states

            if i - 2 < 0:
                s2 = ["*"]
            else:
                s2 = self.states

            for s in s0:
                for u in s1:
                    l = {t: (tri[i - 1, t, u] + self.sumBest(t, u, sen, i, s)) for t in s2}
                    tri[i, u, s] = max(l.values())
                    # print(l.values())
                    bp[i, u, s] = [t for t in l if l[t] == max(l.values())][-1]
        # for s in self.states:
        #     for u in self.states:
        #         gen = (u,s)
        gen = ((u, s) for u in self.states for s in self.states)
        l = {(u, s):(tri[n - 1, u, s] + self.sumBest(u, s, sen, n, "STOP")) for u, s in gen}
        tags[n-2], tags[n-1] = [t for t in l if l[t] == max(l.values())][-1]

        for i in range(n - 3, -1, -1):
            tags[i] = bp[i + 2, tags[i + 1], tags[i + 2]]
        # print(tags)

        return tags
    def sumBest(self, t, u, sen, i, s):

        g = features(t, u, sen, i, s)
        x = sum(self.alpha[k] for k in g)
        # print(x)
        return x
  

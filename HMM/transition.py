import sys
import numpy as np
from collections import namedtuple

#calculates the trigram occurance for each of the tags and calculate the transition probability


def transitionProb(fr):
    tri = {}
    trigram = namedtuple("trigram", ["first", "second", "third"])
    bigram = namedtuple("bigram", ["first", "second"])
    c = {}
    with open(fr, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) != 0:
                w = line.split(" ")
                if w[1] == "3-GRAM":
                    if c.get(bigram(w[2],w[3])):
                        c[bigram(w[2],w[3])] = c[bigram(w[2],w[3])] + float(w[0])
                    else:
                        c[bigram(w[2],w[3])] = float(w[0])
    
    with open(fr, 'r') as g:
        for line in g:
            line = line.strip()
            if len(line) != 0:
                w = line.split(" ")
                if w[1] == "3-GRAM":
                    tri[trigram  (w[2],w[3],w[4])] = (float(w[0])/c[bigram(w[2],w[3])])
    return tri

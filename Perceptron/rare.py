import random
from collections import Counter
lines = open('gene.train').read().splitlines()
f = open('rare.train','w')
a=Counter(lines)
for i in range(len(lines)) :
    if a.get(lines[i]) <5:
        b = lines[i].split()
        b[0] = '__RARE__'
        lines[i] =' '.join(b)
        # print(lines[i])

    f.write(str(lines[i])+ '\n')

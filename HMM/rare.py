import sys, collections
import time


counts= []
dev=[]
with open(sys.argv[1], 'r') as f:       
        content = f.readlines()
        for lines in content:
            lines = lines.rstrip()
            words = lines.split(" ")
            counts.append(words)

# print( counts)
def rare() :
    w1= []
    w=[]
    
    for i in counts:
        
        if i[1] == 'WORDTAG' and i[2] == 'GENE'  and int(i[0])<5  :
            
            w.append(i[3])
        if i[1] == 'WORDTAG' and i[2] == 'NOGENE'  and int(i[0])<5 :
            
            w1.append(i[3])
    return list(set(w1).intersection(w))
    
a = rare()

for i in counts :
    for q in a :
        if i[1] == 'WORDTAG' and  i[3] == q :
            i[3] = '__RARE__'
       
generare = 0
nogenerare = 0
for i in counts :
    
    if i[1] == 'WORDTAG' and i[2] == 'GENE' and i[3] == '__RARE__' :
        generare += int(i[0])
        # print (i) 
        counts.remove(i)
    if i[1] == 'WORDTAG' and i[2] == 'NOGENE' and i[3] == '__RARE__' :
        nogenerare += int(i[0])
        # print (i )
        counts.remove(i)

counts.append([generare,'WORDTAG','GENE','__RARE__'])
counts.append([nogenerare,'WORDTAG','NOGENE','__RARE__'])

# print (generare)
# print (nogenerare)

a = '\n'.join(' '.join(map(str,sl)) for sl in counts)
fw = open("a.counts",'w')
fw.write(str(a))
# sys.stdout.write(str(a))
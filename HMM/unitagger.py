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

with open(sys.argv[2], 'r') as f:       
        content = f.readlines()
        for lines in content:
            lines = lines.rstrip()
            
            dev.append(lines)
count_class= [0,0]
#Function that replaces the rare words with __RARE__
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
counts_file = []
with open("a.counts", 'r') as f:       
        content = f.readlines()
        for lines in content:
            lines = lines.rstrip()
            words = lines.split(" ")
            counts_file.append(words)


for i in counts_file :
    if i[2] == 'NOGENE' :
        count_class[0] += int(i[0])
    
    if i[2] == 'GENE' :
        count_class[1] += int(i[0]) 
        
#calculates the count of occurnaces for each class

def count_classes(word):
    words_countclass = {}            # count of all words in both classes
    nogene = 0
    gene = 0
    for i in counts_file : 
        if i[1] == 'WORDTAG' and i[3] == word and i[2] == 'NOGENE'  :
            nogene = i[0]
        if i[1] == 'WORDTAG' and i[3] == word and i[2] == 'GENE':
            gene = i[0]
        
        
            
    words_countclass.update({ word : [nogene, gene]})
    return words_countclass
#function to calculate the emission probability
def emision_probability(word,clas) :
    count = count_classes(word)
    count_clas = count.get(word)
    return int(count_clas[clas])/count_class[clas]

# ep_rare = max(emision_probability("__RARE__",0),emision_probability("__RARE__",1))
# print ep_rare
for i in dev :

    if i == "" :
        c =  ""
    else:
        ep_nogene = emision_probability(i , 0)
        ep_gene = emision_probability(i , 1)
        
            
        if ep_gene > ep_nogene  :
            c =   str(i + ' GENE')
        elif ep_gene < ep_nogene :
            c =  str(i + ' NOGENE')
        else :
            c =   str(i + ' GENE')
        
    sys.stdout.write(c+"\n")   
        
# t0 = time.time()

# print (count_classes('__RARE__'))


    # c= str(a+b)
    # sys.stdout.write(c+"\n")    
    
# d = time.time() - t0
# print ("duration: %.2f s." % d)

# print (counts_file)
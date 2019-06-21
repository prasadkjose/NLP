import sys, collections
import time


counts_file= []
dev=[]
with open(sys.argv[1], 'r') as f:       
        content = f.readlines()
        for lines in content:
            lines = lines.rstrip()
            words = lines.split(" ")
            counts_file.append(words)

with open(sys.argv[2], 'r') as f:       
        content = f.readlines()
        for lines in content:
            lines = lines.rstrip()
            
            dev.append(lines)
count_class= [0,0]

for i in counts_file :
    if i[2] == 'NOGENE' :
        count_class[0] += int(i[0])
    
    if i[2] == 'GENE' :
        count_class[1] += int(i[0])    

def count_classes(word):
    words_countclass = {}            # count of all words in both classes
    nogene = 0
    gene = 0
    for i in counts_file : 
        if i[1] == 'WORDTAG' and i[3] == word and i[2] == 'NOGENE'  :
            if int(i[0])< 5 :
                nogene = "__RARE__"
                
            else :
                nogene = i[0]
        if i[1] == 'WORDTAG' and i[3] == word and i[2] == 'GENE':
            if int(i[0])< 5 :
                gene = "__RARE__"
            else :
                gene = i[0]
        
            
    words_countclass.update({ word : [nogene, gene]})
    return words_countclass

def emision_probability(word,clas) :
    count = count_classes(word)
    count_clas = count.get(word)
    if count_clas[clas] == "__RARE__" :
        return 0
    else :
        return int(count_clas[clas])/count_class[clas]

def tagger(word):
    if word == "" :
        return "", "" 
    else :
        ep_nogene = emision_probability(word , 0)
        ep_gene = emision_probability(word , 1)
        if ep_gene == "__RARE__" or ep_nogene == "__RARE" :
            return  word, " __RARE__"
        else : 
            if ep_gene > ep_nogene :
                return   word , ' GENE'
            elif ep_gene < ep_nogene :
                return  word , ' NOGENE'
            else :               # for words not in the training set
                # print(word)
                return  word, " __RARE__"
        
# t0 = time.time()
for i in dev :    
    a, b = (tagger(i))
    c= str(a+b)
    sys.stdout.write(c+"\n")    
    
# d = time.time() - t0
# print ("duration: %.2f s." % d)
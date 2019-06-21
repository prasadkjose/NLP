import sys
import copy
import json
import copy

    #Dictionary with a default value for unknown keys.

class DefaultDict (dict):
    def __init__(self, default):
        self.default = default
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))
   


f = open("toygrammar.json", "r")
a=json.load(f)
# print(a)

global grammar
grammar={}
for line in a:
    if len(line)==1:
            continue
    if len(line)==3:
        for i in a.get(line):
            grammar.setdefault(i[0], {}).update({(i[1],i[2]) : i[3]})

    if len(line)==2:
        for i in a.get(line):
            grammar.setdefault(i[0], {}).update({i[1]: i[2]})


#check if T or NT exixts in grammar
def Check_grammar(constituent):
    #print constituent
    results = []
    for (lhs,rhss) in grammar.items():
        for rhs in rhss:
            if rhs == constituent:
                results.append(lhs)

    return results

def printtable(table, wordlist):
#print the CYK Table with the T and NT.
    print ("    ", wordlist)
    for row in table:
	    print (row)

def tree(x, back, i, j, X):
    n = j - i
    if n == 1:
        return [X, x[i]]
    else:
        Y, Z, s = back[i, j, X]
        return [X, tree(x, back, i, s, Y),
                   tree(x, back, s, j, Z)]

def cky(sentence):
    global grammar
    # Create the table; index j for rows, i for columns for the grammar
    # create Table2 for the assiciated probabilitites
    length = len(sentence)
    table = [[[] for j in range(length+1)] for i in range(length)]
    # table2.setdefault(float, copy.deepcopy(table2))

    Prob_Table = DefaultDict(float)
    # table2={}
    backPointer = {}

   
    # Fill the diagonal of the table with the parts-of-speech of the words
    for k in range(1,length+1):
        results = Check_grammar(sentence[k-1])
        for item in results:
            prob = grammar[item][sentence[k-1]]
            # print(prob)
            Prob_Table[k-1,k, item] = prob    #assign the probablilities in the table
        # print(table)
        # print(k)
        table[k-1][k].extend(results)

    #Weighted CYK

    for width in range(2,length+1): 
        for start in range(0,length+1-width): 
            end = start + width 
            for mid in range (start, end): 
                args = None
                for x in table[start][mid]: 
                    for y in table[mid][end]:
                        #print( x,y)
                        results = Check_grammar((x,y))
                        for k in results:
                            prob1 = grammar[k][(x,y)]
                            prob2 = prob1 * Prob_Table[start, mid, x] * Prob_Table[mid, end, y]
                            q = start, end, k
                            #check in Prob_table if POS exist
                            if q in Prob_Table:
                                if prob2 > Prob_Table[start, end, k]:
                                    Prob_Table[start, end, k] = prob2
                            else:
                                Prob_Table[start, end, k] = prob2
                            args2 = x, y, mid
                            #update the highest probability to BackPOinter.
                            #backPointer is the sentece with the highest prbability. 
                            if args2 in backPointer:
                                if prob2 > Prob_Table[start, end, k]:
                                    args = x, y, mid
                                    backPointer[start, end, k] = args
                            else:
                                args = x, y, mid
                                backPointer[start, end, k] = args
                            backPointer[start, end, k] = args
                            if k not in table[start][end]:
                                table[start][end].append(k)



    # Print the table
    # print ("The Tags Table")
    # printtable(table, sentence)

    # print ("\nProbability Table")
    # print (Prob_Table)
    #the probability of the sentence
    # print(prob2)
    print ("\nThe Parse Tree")
    if Prob_Table[0, length-1, 'S']:
        try:
            print (tree(sentence, backPointer, 0, length, 'S'))
            print(prob2)

        except KeyError:
            print ('No analysis')


                   
"Please Uncomment the below functions one by one"
# cky('the man the girl'.split())
# cky('the girl sees the telescope'.split())
# cky('the girl sees the telephone'.split())
# cky('the telescope watches the man with the girl'.split())
cky('the man sees the man with the telescope'.split())





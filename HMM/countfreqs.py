#! /usr/bin/env python3

# Original version: Daniel Bauer <bauer@cs.columbia.edu>, Sep 12, 2011
# Modified version: Yves Scherrer, UNIGE, Nov 7, 2014

import sys, collections

"""
Count n-gram frequencies in a data file and write counts to stdout. 
"""

def ngramIterator(corpusFile, n):
    """
    Get a generator that returns n-grams over the entire corpus,
    respecting sentence boundaries and inserting boundary tokens.
    """
    l = corpusFile.readline()
    currentSentence = [] #Buffer for the current sentence
    
    while l:
        line = l.strip()
        if line: # Nonempty line
            fields = line.split(" ")
            tag = fields[-1]
            word = " ".join(fields[:-1])
            currentSentence.append((word, tag)) # Add token to the buffer
        else: # Empty line
            if currentSentence: # Reached the end of a sentence
                currentSentence = (n-1) * [(None, "*")] + currentSentence + [(None, "STOP")] # Add boundary symbols to the sentence
                ngrams = [currentSentence[i:i+n] for i in range(len(currentSentence)-n+1)] # Then extract n-grams
                for ngram in ngrams: # Return one n-gram at a time
                    yield ngram
                currentSentence = [] # Reset buffer
            else: # Got empty input stream
                sys.stderr.write("WARNING: Got empty input file/stream.\n")
                raise StopIteration
        l = corpusFile.readline()
    
    if currentSentence: # If the last line was blank, we're done
    # Otherwise when there is no more token in the stream return the last sentence.
        currentSentence = (n-1) * [(None, "*")] + currentSentence + [(None, "STOP")] # Add boundary symbols to the sentence
        ngrams = [currentSentence[i:i+n] for i in range(len(currentSentence)-n+1)] # Then extract n-grams
        for ngram in ngrams: # Return one n-gram at a time
            yield ngram


def countNgrams(corpusFile, n, outputFile):
    emissionCounts = collections.defaultdict(int)
    ngramCounts = [collections.defaultdict(int) for i in range(n)]
    iter = ngramIterator(corpusFile, n)
    
    for ngram in iter:
        #Sanity check: n-gram we get from the corpus stream needs to have the right length
        assert len(ngram) == n, "ngram in stream is {}, expected {}".format(len(ngram), n)
        
        tagsonly = tuple([tag for word, tag in ngram]) #retrieve only the tags            
        for i in range(2, n+1): #Count tag 2-grams..n-grams
            ngramCounts[i-1][tagsonly[-i:]] += 1
        
        if ngram[-1][0] is not None: # If this is not the last word in a sentence
            ngramCounts[0][tagsonly[-1:]] += 1 # count 1-gram
            emissionCounts[ngram[-1]] += 1 # and emission frequencies

        # Need to count a single n-1-gram of sentence start symbols per sentence
        if ngram[-2][0] is None: # this is the first n-gram in a sentence
            ngramCounts[n - 2][tuple((n - 1) * ["*"])] += 1

    # First write counts for emissions
    for word, tag in emissionCounts:  
        outputFile.write("{} WORDTAG {} {}\n".format(emissionCounts[(word, tag)], tag, word))

    # Then write counts for all ngrams
    for i in range(1, n+1):
        for ngram in ngramCounts[i-1]:
            ngramstr = " ".join(ngram)
            outputFile.write("{} {}-GRAM {}\n".format(ngramCounts[i-1][ngram], i, ngramstr))


def usage():
    print("""
    python count_freqs.py [input_file] > [output_file]
        Read in a gene tagged training input file and produce counts.
    """)

if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        input = open(sys.argv[1], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n")
        sys.exit(1)
    
    countNgrams(input, 3, sys.stdout)

import numpy as np
from trie import Trie


# ======================== ADDED METHODS FELIX =================================
#returns dictionary of valid words and their distances!
# searched = searched word
# words = trie obbject containing all the words from the vocabulary
# threshold: maximum distance from word
def dp_levenshtein_trie(searched, words, threshold):
    # array vacía de len(x)·len(trie)
    D = np.zeros((len(searched)+1, words.get_num_states()), int)
    # fill in the first column
    for j in range(1, words.get_num_states()):
        D[0, j] = trie_depth(words, j)
    for i in range(1, len(searched)+1):
        # fill in the first row
        D[i, 0] = i                                                 
        for j in range(1, words.get_num_states()):
            c  = 0 if words.get_label(j) == searched[i-1] else 1
            D[i,j]= min(D[i-1, words.get_parent(j)]+c, D[i, words.get_parent(j)]+1, D[i-1,j]+1)
    results = {}
    #vector of enddistances
    v = D[len(searched),]
    #filter vector for valid words and words below threshold and put into dictionary
    for i in range(words.get_num_states()):
        if words.is_final(i) and v[i] <= threshold:
            results[words.get_output(i)] = v[i]
    return results

# This version does not calculate distances to nodes whose word is too long 
def dp_levenshtein_trie_improved(searched, words, threshold):
    # array vacía de len(x)·len(trie)
    D = np.zeros((len(searched)+1, words.get_num_states()), int)
    first_too_deep = words.get_num_states()

    # fill in the first column til the first node that is too deep
    for j in range(1, words.get_num_states()):
        depth = trie_depth(words, j)
        if len(searched)+threshold < depth:
            first_too_deep = j
            break
        else:
            D[0, j] = depth

    #All these nodes are unreachable in the threshold
    for j in range(first_too_deep, words.get_num_states()):
        D[len(searched), j] = threshold+1

    for i in range(1, len(searched)+1):
        # fill in the first row
        D[i, 0] = i                                                 
        for j in range(1, first_too_deep):
            c  = 0 if words.get_label(j) == searched[i-1] else 1
            D[i,j]= min(D[i-1, words.get_parent(j)]+c, D[i, words.get_parent(j)]+1, D[i-1,j]+1)
    results = {}
    #vector of enddistances
    v = D[len(searched),]
    #filter vector for valid words and words below threshold and put into dictionary
    for i in range(words.get_num_states()):
        if words.is_final(i) and v[i] <= threshold:
            results[words.get_output(i)] = v[i]
    return results

def dp_restricted_damerau_trie_improved(searched, words, threshold):
    # array vacía de len(x)·len(trie)
    D = np.zeros((len(searched)+1, words.get_num_states()), int)
    D[1, 0] = 1
    first_too_deep = words.get_num_states()

    # fill in the first two columns (only for reachable nodes depending on their depth)
    for j in range(1, words.get_num_states()):
        depth = trie_depth(words, j)
        if len(searched)+threshold < depth:
            first_too_deep = j
            break
        else:
            D[0, j] = depth
            c = 0 if words.get_label(j) == searched[0] else 1
            D[1, j] = min(D[0, words.get_parent(j)]+c, D[1, words.get_parent(j)]+1, D[0,j]+1)

    # unreachable, too deep nodes get th+1 value
    for j in range(first_too_deep, words.get_num_states()):
        D[len(searched), j] = threshold+1
    
    for i in range(2, len(searched)+1):
        # fill in the first row
        D[i, 0] = i
        #now we know: i >= 2 (necessary for swap)
        for j in range(1, first_too_deep):
            c  = 0 if words.get_label(j) == searched[i-1] else 1
            #swap possible? -> check letters and that j has at least depth 2
            if words.get_label(j) == searched[i-2] and words.get_parent(words.get_parent(j)) != -1 and words.get_label(words.get_parent(j)) == searched[i-1]:
                D[i,j]= min(    D[i-1, words.get_parent(j)]+c, \
                                D[i, words.get_parent(j)]+1, \
                                D[i-1,j]+1, \
                                D[i-2, words.get_parent(words.get_parent(j))]+1)
            else:
                D[i,j]= min(    D[i-1, words.get_parent(j)]+c, \
                                D[i, words.get_parent(j)]+1, \
                                D[i-1,j]+1)

    results = {}
    #vector of enddistances
    v = D[len(searched),]
    #filter vector for valid words and words below threshold and put into dictionary
    for i in range(words.get_num_states()):
        if words.is_final(i) and v[i] <= threshold:
            results[words.get_output(i)] = v[i]
    return results

def dp_restricted_damerau_trie(searched, words, threshold):
    # array vacía de len(x)·len(trie)
    D = np.zeros((len(searched)+1, words.get_num_states()), int)
    D[1, 0] = 1
    # fill in the first two columns
    for j in range(1, words.get_num_states()):
        D[0, j] = trie_depth(words, j)
        c = 0 if words.get_label(j) == searched[0] else 1
        D[1, j] = min(D[0, words.get_parent(j)]+c, D[1, words.get_parent(j)]+1, D[0,j]+1)
    
    for i in range(2, len(searched)+1):
        # fill in the first row
        D[i, 0] = i
        #now we know: i >= 2 (necessary for swap)
        for j in range(1, words.get_num_states()):
            c  = 0 if words.get_label(j) == searched[i-1] else 1
            #swap possible? -> check letters and that j has at least depth 2
            if words.get_label(j) == searched[i-2] and words.get_parent(words.get_parent(j)) != -1 and words.get_label(words.get_parent(j)) == searched[i-1]:
                D[i,j]= min(    D[i-1, words.get_parent(j)]+c, \
                                D[i, words.get_parent(j)]+1, \
                                D[i-1,j]+1, \
                                D[i-2, words.get_parent(words.get_parent(j))]+1)
            else:
                D[i,j]= min(    D[i-1, words.get_parent(j)]+c, \
                                D[i, words.get_parent(j)]+1, \
                                D[i-1,j]+1)

    results = {}
    #vector of enddistances
    v = D[len(searched),]
    #filter vector for valid words and words below threshold and put into dictionary
    for i in range(words.get_num_states()):
        if words.is_final(i) and v[i] <= threshold:
            results[words.get_output(i)] = v[i]
    return results


def dp_intermediate_damerau_trie(searched, words, threshold):
    # array vacía de len(x)·len(trie)
    D = np.zeros((len(searched)+1, words.get_num_states()), int)
    D[1, 0] = 1
    # fill in the first two columns
    for j in range(1, words.get_num_states()):
        D[0, j] = trie_depth(words, j)
        c = 0 if words.get_label(j) == searched[0] else 1
        D[1, j] = min(D[0, words.get_parent(j)]+c, D[1, words.get_parent(j)]+1, D[0,j]+1)
    
    for i in range(2, len(searched)+1):
        # fill in the first row
        D[i, 0] = i
        #now we know: i >= 2 (necessary for swap)
        for j in range(1, words.get_num_states()):
            c  = 0 if words.get_label(j) == searched[i-1] else 1
            #swap possible? -> check letters and that j has at least depth 2
            if words.get_label(j) == searched[i-2] and words.get_parent(words.get_parent(j)) != -1 and words.get_label(words.get_parent(j)) == searched[i-1]:
                D[i,j]= min(    D[i-1, words.get_parent(j)]+c, \
                                D[i, words.get_parent(j)]+1, \
                                D[i-1,j]+1, \
                                D[i-2, words.get_parent(words.get_parent(j))]+1)
            else:
                D[i,j]= min(    D[i-1, words.get_parent(j)]+c, \
                                D[i, words.get_parent(j)]+1, \
                                D[i-1,j]+1)
            # word in trie "axb" -> searched word "ba"
            case1 = words.get_parent(words.get_parent(words.get_parent(j))) != -1 and \
                    words.get_label(words.get_parent(words.get_parent(j))) == searched[i-1] and \
                    words.get_label(j) == searched[i-2]

            # word in trie "ba" -> searched word "axb"
            case2 = words.get_parent(words.get_parent(j)) != -1 and \
                    i > 2 and \
                    words.get_label(words.get_parent(j)) == searched[i-1] and \
                    words.get_label(j) == searched[i-3]
            if case1:
                #trie "axb" -> searched "ba" with cost 2
                #print("Case 1 activated at i, j = "+str(i)+", "+str(j))
                D[i, j] = min(D[i, j], D[i-2, words.get_parent(words.get_parent(words.get_parent(j)))]+2)
            elif case2:
                #trie "ba" -> searched "axb" with cost 2
                #print("Case 2 activated at i, j = "+str(i)+", "+str(j))
                D[i, j] = min(D[i, j], D[i-3, words.get_parent(words.get_parent(j))]+2)
            #print(str(D)+"\n")
    results = {}
    #vector of enddistances
    v = D[len(searched),]
    #filter vector for valid words and words below threshold and put into dictionary
    for i in range(words.get_num_states()):
        if words.is_final(i) and v[i] <= threshold:
            results[words.get_output(i)] = v[i]
    return results

def trie_depth(tree, node):
    if node == 0:
        return 0
    depth = 1
    while tree.get_parent(node) != tree.get_root():
        depth += 1
        node = tree.get_parent(node)
    return depth



def poliformat_test():
    """ CÓDIGO DE TESTEO DE POLIFORMAT (FUNCIONA!) """
    words = ["algortimo", "algortximo","lagortimo", "agaloritom", "algormio", "ba"]
    words.sort()
    trie = Trie(words)

    test = ["algoritmo", "acb"]
    thrs = range(1, 4)

    for threshold in thrs:
        print(f"threshols: {threshold:3}")
        for x in test:
            for dist,name in (
                        (dp_levenshtein_trie,"levenshtein"),
                        (dp_restricted_damerau_trie,"restricted"),
                        (dp_intermediate_damerau_trie,"intermediate"),
                        ):
                print(f"\t{x:12} \t{name}\t", end="")
                print(dist(x, trie, threshold))
"""
Salida del programa:

threshols:   1
	algoritmo    	levenshtein	[]
	algoritmo    	restricted	[('algortimo', 1)]
	algoritmo    	intermediate	[('algortimo', 1)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[]
threshols:   2
	algoritmo    	levenshtein	[('algortimo', 2)]
	algoritmo    	restricted	[('algortimo', 1), ('lagortimo', 2)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 2)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[('ba', 2)]
threshols:   3
	algoritmo    	levenshtein	[('algormio', 3), ('algortimo', 2), ('algortximo', 3)]
	algoritmo    	restricted	[('algormio', 3), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 3)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('agaloritom', 3), ('algortximo', 2)]
	acb          	levenshtein	[('ba', 3)]
	acb          	restricted	[('ba', 3)]
	acb          	intermediate	[('ba', 2)]

"""         

""" CÓDIGO DE TESTEO DE FELIX """
# # little test method 
def interactive():
    test_dict = ["aa", "aaaaba", "ab", "ac", "bb", "c", "cab", "cac", "hellotest"]
    test_trie = Trie(sorted(test_dict))
    print("Test dictonary in tree format:")
    print(test_trie)
    searched = input("Input word to search for (ignoring upper/lowercase)\n").lower()
    threshold = int(input("Input threshold: (e.g. 3)\n"))
    print("Levenshtein:\n"+str(dp_levenshtein_trie(searched, test_trie, threshold)))
    print("Restricted:\n"+str(dp_restricted_damerau_trie(searched, test_trie, threshold)))
    print("Intermediate:\n"+str(dp_intermediate_damerau_trie(searched, test_trie, threshold)))


if __name__ == "__main__":
    poliformat_test()
    interactive()

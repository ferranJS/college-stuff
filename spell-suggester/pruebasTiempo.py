from spellsuggest import TrieSpellSuggester, SpellSuggester
import time
import re, json
import numpy as np
import matplotlib.pyplot as plt


def tiempo_test3():
    measure_name = input("Please give this measurement a name\n")
    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    trie_spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    words = sorted(["tal", "casa", "senor", "jabón", "constitución", "ancho",
                            "savaedra", "vicios", "quixote", "s3afg4ew"], key = len)
    distancias = ["levenshtein", "levenshtein_improved", "restricted", "restricted_improved", "intermediate"]
    thresholds = [1, 2, 3, 5, 7]
    D = np.zeros((len(thresholds), len(words), len(distancias)*2), float)
    for threshold in thresholds:
        print("\nTHRESHOLD: "+str(threshold))
        print("\t\t\tL\tLI\tDLR\tDLRI\tDLI\tTL\tTLI\tTDLR\tTDLRI\tTDLI")
        for word in words:
            for distancia in distancias:
                t1 = time.process_time()
                res1 = spellsuggester.suggest(word, threshold, distancia)
                t2 = time.process_time()
                D[thresholds.index(threshold)][words.index(word)][distancias.index(distancia)] = t2-t1
                t1 = time.process_time()
                res2 = trie_spellsuggester.suggest(word, threshold, distancia)
                t2 = time.process_time()
                D[thresholds.index(threshold)][words.index(word)][distancias.index(distancia)+5] = t2-t1
                # maybe not necessary, just extra ensuring that the functions do the right thing
                # assert(res1 == res2)
            print(word+":"+" "*(20-len(word)), end = "")
            string = ""
            for i in range(len(distancias)*2):
                string += "{:8.3f}".format(D[thresholds.index(threshold)][words.index(word)][i])
            print(string)

    # #Testing:
    # D = np.zeros((5, 10, 10), float)
    # for i in range(5):
    #     for j in range(10):
    #         for k in range(10):
    #                 D[i][j][k] = round(np.random.uniform(0.5,3), 3)

    print("Times: (5 thresholds x 10 words x 10 distancia methods)\n"+str(D))

    # PLOTTING:
    dist_names = ["lev", "lev_cota", "restr", "restr_cota", "intermediate", "trie_lev", \
        "trie_lev_improved", "trie_restr", "trie_restr_improved", "trie_intermediate"]
    #First Plot: all 10 words with the 6 most optimised distance functions and different thresholds
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(16, 30), constrained_layout = True)
    fig.suptitle("Performance of 6 most optimised algorithms (3 distances, trie and not trie)", fontsize = 16)
    configs1 = ["cornflowerblue", "cornflowerblue", "blue", "blue", "darkblue", "springgreen", "springgreen", \
            "mediumseagreen", "mediumseagreen", "darkgreen"]
    for i in range(10):
        axes[i//2][i%2].set_title("Word: \""+words[i]+"\" (len = "+str(len(words[i]))+")")
        axes[i//2][i%2].set_ylabel("Time")
        axes[i//2][i%2].set_xlabel("Threshold")
        for j in [1, 3, 4, 6, 8, 9]:
            axes[i//2][i%2].plot(thresholds, D[:,i,j], '-o', color = configs1[j], label = dist_names[j])
        axes[i//2][i%2].legend(loc='upper left')
    filename = measure_name + "_graph1.pdf"
    plt.savefig(filename)
    print("File \""+filename+"\" saved!")

    #Second Plot: Improvement of improved methods depending on wordlength and threshold
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,9), constrained_layout=True)
    fig.suptitle("Improvement speedup depending on word length", fontsize = 16)
    threshindices = [0, 3]
    wordlengths = [len(w) for w in words]
    for i in [0, 1]:
        axes[i].set_title("Threshold = "+str(thresholds[threshindices[i]]))
        axes[i].set_ylabel("Speedup (normal/improved)")
        axes[i].set_xlabel("Wordlength")
        axes[i].plot([2, 13], [1, 1], color = "red", label = "speedup = 1 (no improvement)", linewidth = 3)
        #normal lev vs normal lev improved -> index 0 and index 1
        axes[i].plot(wordlengths, [(x/y) for x,y in zip(D[threshindices[i],:,0], D[threshindices[i],:,1])], '-o', label ="lev vs lev_cota", color = "cornflowerblue")
        #normal restr vs normal restr improved -> index 2 and index 3
        axes[i].plot(wordlengths, [(x/y) for x,y in zip(D[threshindices[i],:,2], D[threshindices[i],:,3])], '-o', label ="restr vs rstr_cota", color = "darkblue")
        #trie lev vs trie lev improved -> index 5 and index 6
        axes[i].plot(wordlengths, [(x/y) for x,y in zip(D[threshindices[i],:,5], D[threshindices[i],:,6])], '-o', label ="trie_lev vs trie_lev_cota", color = "mediumseagreen")
        #trie restr vs trie restr improved -> index 7 and index 8
        axes[i].plot(wordlengths, [(x/y) for x,y in zip(D[threshindices[i],:,7], D[threshindices[i],:,8])], '-o', label ="trie_restr vs trie_restr_cota", color = "darkgreen")
        axes[i].legend()
    filename = measure_name + "_graph3.pdf"
    plt.savefig(filename)
    print("File \""+filename+"\" saved!")

    #Third Plot: Speedup of trie algo vs normal algo, depending on threshold, for different words and average
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18,12), constrained_layout=True)
    fig.suptitle("Speedup using trie algorithms instead of normal ones", fontsize = 16)
    wordindices = [0, 5, 9]
    titles = [("Word: \""+words[wordindices[i]]+"\" (len = "+str(len(words[wordindices[i]]))+")") for i in range(3)] \
    + ["Average over all words"]
    algoindices = [(1, 6), (3, 8), (4, 9)]
    y_values = np.zeros((4, 3, 5),float)

    for j in range(3):
        for i in range(3):
            a, b = algoindices[j]
            w = wordindices[i]
            y_values[i][j] = [x/y for x,y in zip(D[:,w,a], D[:,w,b])]
        avg1 = [np.mean(list) for list in D[:,:,a]]
        avg2 = [np.mean(list) for list in D[:,:,b]]
        y_values[3][j] = [x/y for x,y in zip(avg1, avg2)]
        
    for i in range(4):
        axes[i//2][i%2].set_title(titles[i])
        axes[i//2][i%2].set_xlabel("Threshold")
        axes[i//2][i%2].set_ylabel("Speedup (normal/trie)")
        axes[i//2][i%2].plot([0, 8], [1, 1], color = "red", label = "speedup = 1 (no improvement)", linewidth = 3)
        axes[i//2][i%2].plot(thresholds, y_values[i][0], '-o', label = "lev_cota vs trie_lev_cota", color = "darkgrey")
        axes[i//2][i%2].plot(thresholds, y_values[i][1], '-o', label = "restr_cota vs trie_restr_cota", color = "dimgrey")
        axes[i//2][i%2].plot(thresholds, y_values[i][2], '-o', label = "intermediate vs trie_intermediate", color = "black")
        axes[i//2][i%2].legend()
    filename = measure_name + "_graph2.pdf"
    plt.savefig(filename)
    print("File \""+filename+"\" saved!")
           

# Test with fixed dictionary size and 10 words, 5 different thresholds comparing 10 different methods, 
# takes about 15 minutes to run through
def tiempo_test2():
    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    trie_spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    words = sorted(["tal", "casa", "senor", "jabón", "constitución", "ancho",
                            "savaedra", "vicios", "quixot", "s3afg4ew"], key = len)
    distancias = ["levenshtein", "levenshtein_improved", "restricted", "restricted_improved", "intermediate"]
    thresholds = [1, 2, 3, 5, 7]
    times_trie = [None] * len(thresholds)
    times_normal = [None] * len(thresholds)
    for threshold in thresholds:
        print("\nTHRESHOLD: "+str(threshold))
        print("\t\t\tL\tLI\tDLR\tDLRI\tDLI\tTL\tTLI\tTDLR\tTDLRI\tTDLI")
        for word in words:
            for distancia in distancias:
                t1 = time.process_time()
                res1 = spellsuggester.suggest(word, threshold, distancia)
                t2 = time.process_time()
                times_normal[distancias.index(distancia)] = t2-t1
                t1 = time.process_time()
                res2 = trie_spellsuggester.suggest(word, threshold, distancia)
                t2 = time.process_time()
                times_trie[distancias.index(distancia)] = t2-t1
                # maybe not necessary, just extra ensuring that the functions do the right thing
                assert(res1 == res2)
            print(word+":"+" "*(20-len(word)), end = "")
            string = ""
            for i in range(len(times_normal)):
                string += "{:8.3f}".format(times_normal[i])
            for i in range(len(times_trie)):
                string += "{:8.3f}".format(times_trie[i])
            print(string)
           



def tiempo_test1():
    dicts = ["10000quijote.txt", "100quijote.txt","30000quijote.txt", "quijote.txt"] #"1000quijote.txt", "20000quijote.txt" 
    thresholds = [1, 2, 3, 5, 7]
    word = "caballo"
    print("WORD: "+word)
    print("Levenshtein \t\t\t\t Levenshtein Improved \t\t Lev-Dam Restringida \t\t Lev-Dam Intermedia \t\t Levenshtein Trie \t\t Lev-Dam Restringida Trie \t\t Lev-Dam Intermedia Trie")

    for dict in dicts:
        
        print("\n"+str(dict)+"\n")

        spellsuggester = SpellSuggester("./corpora/"+dict)
        trie_spellsuggester = TrieSpellSuggester("./corpora/"+dict)

        for threshold in thresholds:

            #Levenshtein
            t_ini_lev = time.process_time()
            res = spellsuggester.suggest(word, threshold, "levenshtein")
            t_end_lev = time.process_time()

            #Levenshtein con complex cota
            t_ini_lev_imp = time.process_time()
            res = spellsuggester.suggest(word, threshold, "levenshtein_improved")
            t_end_lev_imp = time.process_time()

            #Restringida
            t_ini_lev_res = time.process_time()
            res = spellsuggester.suggest(word, threshold, "restricted")
            t_end_lev_res = time.process_time()

            #Intermedia
            t_ini_lev_int = time.process_time()
            res = spellsuggester.suggest(word, threshold,"intermediate")
            t_end_lev_int = time.process_time()

            #Con Trie
            t_ini_lev_trie = time.process_time()
            res = trie_spellsuggester.suggest(word, threshold, "levenshtein")
            t_end_lev_trie = time.process_time()

            t_ini_res_trie = time.process_time()
            res = trie_spellsuggester.suggest(word, threshold, "restricted")
            t_end_res_trie = time.process_time()

            t_ini_int_trie = time.process_time()
            res = trie_spellsuggester.suggest(word, threshold, "intermediate")
            t_end_int_trie = time.process_time()

            print("THRESHOLD: "+str(threshold))
            print(format(round(t_end_lev - t_ini_lev,5),'.5f') + " \t\t\t\t " + format(round(t_end_lev_imp - t_ini_lev_imp,5),'.5f') + " \t\t\t\t " + format(round(t_end_lev_res - t_ini_lev_res,5),'.5f') + " \t\t\t\t " + format(round(t_end_lev_int - t_ini_lev_int,5),'.5f') + " \t\t\t\t " + format(round(t_end_lev_trie - t_ini_lev_trie,5),'.5f') + " \t\t\t\t " + format(round(t_end_res_trie - t_ini_res_trie,5),'.5f') + " \t\t\t\t " + format(round(t_end_int_trie - t_ini_int_trie,5),'.5f') )    
        

        print("----------------------------------------------------------")

if __name__ == "__main__":
    tiempo_test3()
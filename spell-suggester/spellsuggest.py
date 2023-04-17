# -*- coding: utf-8 -*-
import re
import time

from trie import Trie

import functions_suggest as cadena_funcs#import dp_levenshtein_threshold, dp_levenshtein_threshold_cota, dp_restricted_damerau_threshold, dp_intermediate_damerau_threshold
# from functions_trie_suggest import dp_levenshtein_trie, dp_restricted_damerau_trie, dp_intermediate_damerau_trie
import functions_trie_suggest as trie_funcs

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path, sorted_vocabulary = None):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """
        if vocab_file_path == None:
            self.vocabulary = sorted_vocabulary
        else:
            self.vocabulary = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

    def suggest(self, term, threshold, distance="levenshtein"):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "levenshtein_improved", "restricted", "restricted_improved", "intermediate"]

        results = {} # diccionario termino:distancia
        
        if distance == "levenshtein":
            for word in self.vocabulary:
                length = cadena_funcs.dp_levenshtein_threshold(term, word,threshold)
                if length <= threshold:
                    results[word] = length
        elif distance == "levenshtein_improved":
            for word in self.vocabulary:
                length = cadena_funcs.dp_levenshtein_threshold_improved(term, word,threshold)
                if length <= threshold:
                    results[word] = length
        elif distance == "restricted":
            for word in self.vocabulary:
                length = cadena_funcs.dp_restricted_damerau_threshold(term, word,threshold)
                if length <= threshold:
                        results[word] = length
        elif distance == "restricted_improved":
            for word in self.vocabulary:
                length = cadena_funcs.dp_restricted_damerau_threshold_improved(term, word,threshold)
                if length <= threshold:
                        results[word] = length
        elif distance == "intermediate":
            for word in self.vocabulary:
                length = cadena_funcs.dp_intermediate_damerau_threshold(term, word,threshold)
                if length <= threshold:
                        results[word] = length

        return results

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y aÃ±ade el trie
    """
    def __init__(self, vocab_file_path, sorted_vocabulary = None):
        super().__init__(vocab_file_path, sorted_vocabulary)  # por defecto coge el suggest() de SpellSuggester
        self.trie = Trie(self.vocabulary)

    def suggest(self, term, threshold, distance="levenshtein"):

        assert distance in ["levenshtein", "levenshtein_improved", "restricted", "restricted_improved", "intermediate"]
        if distance == "levenshtein":
            return trie_funcs.dp_levenshtein_trie(term, self.trie, threshold)
        elif distance == "levenshtein_improved":
            return trie_funcs.dp_levenshtein_trie_improved(term, self.trie, threshold)
        elif distance == "restricted":
            return trie_funcs.dp_restricted_damerau_trie(term, self.trie, threshold)
        elif distance == "restricted_improved":
            return trie_funcs.dp_restricted_damerau_trie_improved(term, self.trie, threshold)
        elif distance == "intermediate":
            return trie_funcs.dp_intermediate_damerau_trie(term, self.trie, threshold)


# Methods return the same for Word sdbohekhbs, threshold 10 and distance "intermediate":False
# tests if the cadena vs cadena and the trie function actually calculate the same:
def test():
    spells = SpellSuggester("./corpora/quijote.txt")
    t_spells = TrieSpellSuggester("./corpora/quijote.txt") 
    for word in ["casa", "caballo", "sdbohekhbs"]:
        for threshold in [1, 2, 3, 5, 10]:
            for distance in ["levenshtein", "restricted", "intermediate"]:
                print("Methods return the same for Word "+word+", threshold "+str(threshold)+" and distance \""+distance+"\": ", end = "")
                print(spells.suggest(word, threshold, distance) == t_spells.suggest(word, threshold, distance))


#TODO: Theres still some mistakes / differences in the result of lev-dam intermediate distance for high thresholds
def spec_test():
    word = "caballo"
    threshold = 13
    distance = "intermediate"
    print(cadena_funcs.dp_intermediate_damerau_threshold(word, "estraordinario", threshold))
    spells = SpellSuggester("./corpora/quijote.txt")
    t_spells = TrieSpellSuggester("./corpora/quijote.txt") 
    res1 = spells.suggest(word, threshold, distance)
    res2 = t_spells.suggest(word, threshold, distance)
    set1 = set(res1.items())
    set2 = set(res2.items())
    sym_dif = set1 ^ set2
    print("Difference:\n"+str(sym_dif))

def improved_test():
    t_spells = TrieSpellSuggester("./corpora/quijote.txt") 
    for word in ["tal", "casa", "caballo", "sdbohekhbs"]:
        for threshold in [1, 2, 3, 5, 10]:
            print("Trie normal vs improved methods return the same for Word "+word+" and threshold "+str(threshold)+": ", end = "")
            t1 = time.process_time()
            resNormal = t_spells.suggest(word, threshold, "restricted")
            t2 = time.process_time()
            t3 = time.process_time()
            resImproved = t_spells.suggest(word, threshold, "restricted_improved")
            t4 = time.process_time()
            print(resNormal == resImproved)
            print("Time normal: "+"{:7.3f}".format(t2-t1)+"\tTime improved: "+"{:7.3f}".format(t4-t3)+"\tSpeedup (normal/improved): "+"{:7.2f}".format((t2-t1)/(t4-t3))+"x")

def intermediate_test():
        t_spells = TrieSpellSuggester("./corpora/problem_words.txt") 
        print(t_spells.trie)
        word = "jabón"
        print(trie_funcs.dp_intermediate_damerau_trie(word, t_spells.trie, 4))


if __name__ == "__main__":
    intermediate_test()
# -*- coding: utf-8 -*-

from spellsuggest import SpellSuggester, TrieSpellSuggester


if __name__ == "__main__":
    #spellsuggester = SpellSuggester("./corpora/quijote.txt")
    spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    for distance in ['levenshtein','restricted','intermediate']:
        destiny =  f'result_{distance}_quijote_own.txt'
        with open(destiny, "w", encoding='utf-8') as fw:
            words = ["casa", "senor", "jabón", "constitución", "ancho",
                            "savaedra", "vicios", "quixot", "s3afg4ew"]
            #print("im here")
            for palabra in words:
                max = 5
                for threshold in range(1, max+1):
                    print("Doing word \""+palabra+"\" ("+str(words.index(palabra)+1)+"/"+str(len(words))+") and distance "+distance+ " for threshold "+str(threshold)+" "*5+"|"+"==="*threshold+"..."*(max-threshold)+"|"+" "*20, end = "\r")
                    resul = spellsuggester.suggest(palabra,distance=distance,threshold=threshold)
                    numresul = len(resul)
                    resul = " ".join(sorted(f'{v}:{k}' for k,v in resul.items()))
                    fw.write(f'{palabra}\t{threshold}\t{numresul}\t{resul}\n')
        print("File \""+destiny+"\" written!"+" "*60)       


# Porject ALG-SAR

Python project

result*_txt are reference and result files to test the correct functioning of the distance methods

leer_resultados.py and plantilla_generar_resultados.py are used to create and read these textfiles   

SAR_*.py files form the SAR project, use "python SAR_Indexer.py --help" and "python SAR_Searcher.py --help"  to learn how to use the program

plots.ipynb is a jupyter notebook that was used to visually test the creation of the graphs with random numbers

functions_suggest.py and functions_trie_suggest contain the methods to measure the different distances 

pruebasTiempo.py can be used to measure and compare the times of the different methods. When executed it creates the 3 different graphs in pdfs with a given name in the form <name>_graph[1 | 2 | 3].pdf
During the execution, there is also live feedback given about the state of the execution

spellsuggest.py contains the SpellSuggester and TrieSpellsuggester classes, which are used in the SAR project to suggest similar words to a search term

The directory corpora contains excerpts of the quijote.txt file of different size as well as the reference data for the SAR project (Newspaper archives in .json format)

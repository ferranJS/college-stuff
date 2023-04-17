# version 1.1


import argparse
import pickle
import sys

from SAR_lib import SAR_Project


def syntax():
    print("python %s indexfile [-s] [query | -l query_list]" % sys.argv[0])
    #print(sys.argv)
    sys.exit()


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Search the index.')

    parser.add_argument('index', metavar='index', type=str,
                        help='name of the file with the index object.')

    group0 = parser.add_mutually_exclusive_group()
    
    group0.add_argument('-N', '--snippet', dest='snippet', action='store_true', default=False, 
                    help='show a snippet of the retrieved documents.')

    group0.add_argument('-C', '--count', dest='count', action='store_true', default=False, 
                    help='show only the number of documents retrieved.')

    parser.add_argument('-A', '--all', dest='all', action='store_true', default=False, 
                    help='show all the results. If not used, only the first 10 results are showed. Does not apply with -C and -T options.')


    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-Q', '--query', dest='query', metavar= 'query', type=str, action='store',
                    help='query.')
    group1.add_argument('-L', '--list', dest='qlist', metavar= 'qlist', type=str, action='store',
                    help='file with queries.')
    group1.add_argument('-T', '--test', dest='test', metavar= 'test', type=str, action='store',
                    help='file with queries and results, for testing.')


        # ALGORITMICA
    group2 = parser.add_argument_group()
    group2.add_argument('-S', '--suggestion', dest='suggestion', action='store_true', default=False,
                    help='Activar sugerencias.')
    group2.add_argument('-D', '--distancia', dest='distancia', type=str, action='store', default='restricted_improved',
                    help='Algoritmo a utilizar (levenshtein[_improved], restricted[_improved] o intermediate). By default "restricted_improved".')
    group2.add_argument('-U', '--threshold', dest='threshold', type=int, action='store', default=2,
                    help='Threshold entre palabras. Por defecto a 2.')
    
    args = parser.parse_args()

    with open(args.index, 'rb') as fh:
        searcher = pickle.load(fh)

    searcher.set_showall(args.all)
    searcher.set_snippet(args.snippet)
    distancia = args.distancia
    #ALT
    if distancia not in ["levenshtein", "levenshtein_improved", "restricted", "restricted_improved", "intermediate"]:
        distancia = "restricted_improved"
    searcher.set_suggestion(args.suggestion, args.distancia, args.threshold)

    # se debe contar o mostrar resultados?
    if args.count is True:
        fnc = searcher.solve_and_count
    else:
        fnc = searcher.solve_and_show

    if args.test is not None:
        # opt: -T, testing

        with open(args.test, encoding='utf-8') as fh:
            lines = fh.read().split('\n')
            for line in lines:
                if len(line) > 0 and not line.startswith('#'):
                    query, reference = line.split('\t')
                    reference = int(reference)
                    result = searcher.solve_and_count(query)
                    if result != reference:
                        print("==> ERROR: '%s'\t%d\t%d" % (query, result, reference))
                        sys.exit(-1)
                else:
                    print(line)
            print('\nParece que todo ha ido bien, buen trabajo!')

    elif args.query is not None:
        # opt: -Q, una query pasada como argumento
        fnc(args.query) # searcher.solve_and_show(args.query)

    elif args.qlist is not None:
        # opt: -L, una lista de queries
        with open(args.qlist, encoding='utf-8') as fh:
            queries = fh.read().split('\n')
            queries.pop()
            for query in queries:
                if len(query) > 0 and not query.startswith('#'):
                    fnc(query)
                else:
                    print(query)
    else:
        # modo interactivo
        query = input("query:")
        while query != "":
            fnc(query)
            query = input("query:")
import argparse
import pickle
import sys
import time

from SAR_lib import SAR_Project


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Index a directory with news in json format.')
    parser.add_argument('newsdir', metavar='newsdir', type=str,
                        help='directory with the news.')

    parser.add_argument('index', metavar='index', type=str,
                        help='name of the file to save the project object.')

    #ALT
    parser.add_argument('-S', '--suggestion', dest='suggestion', action='store_true', default=False, 
                        help='Sugiere palabras similares en caso de no obtener resultados para la palabra seleccionada.')                   
    
    args = parser.parse_args()

    newsdir = args.newsdir
    indexfile = args.index
    # give as an argument if we want to create a spellsuggester for the SAR_Project Object
    indexer = SAR_Project(args.suggestion)
    t0 = time.time()
    indexer.index_dir(newsdir, **vars(args))
    t1 = time.time()
    with open(indexfile, 'wb') as fh:
            pickle.dump(indexer, fh)
    t2 = time.time()
    indexer.show_stats()
    print("Time indexing: %2.2fs." % (t1 - t0))
    print("Time saving: %2.2fs." % (t2 - t1))
    print()
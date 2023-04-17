import numpy as np

# calculates the minimum number of letter changes
def cota_complex(x, y):
    d_x = {}
    #count occurrences of letters in the two words
    for l in x:
        d_x[l] = d_x.get(l, 0) +1
    d_y = {}
    for l in y:
        d_y[l] = d_y.get(l, 0) +1
    # M is set of all letters
    M = set(d_y.keys()).union(set(d_x.keys()))
    pos = 0
    neg = 0
    # temp counts the difference in occurrences of one letter to add to the total count
    # of minimum number of letters that have to be changed
    for k in M:
        temp = d_y.get(k, 0)-d_x.get(k, 0)
        if temp < 0: neg -= temp
        else: pos += temp
    return max(neg, pos)

def dp_levenshtein_threshold_improved(x, y, th):
    if((abs(len(x)-len(y)) > th) or (cota_complex(x, y) > th)): return th+1       
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        valorMin = th+1                                     #task 2
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0
            else: sust = 1
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust )
            if(m[i,j]<valorMin): valorMin = m[i,j]         #task 2
        if(valorMin>th) : return th+1                          #task 2
    return min(m[i,j], th+1)

def dp_levenshtein_threshold(x, y, th):
    if(abs(len(x)-len(y)) > th): return th+1        # comparar len
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        valorMin = th+1                                     #task 2
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0
            else: sust = 1
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust )
            if(m[i,j]<valorMin): valorMin = m[i,j]         #task 2
        if(valorMin>th) : return th+1                          #task 2
    return min(m[i,j], th+1)

def dp_restricted_damerau_threshold_improved(x, y, th):
    if((abs(len(x)-len(y)) > th) or (cota_complex(x, y) > th)): return th+1
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        valorMin = th+1                              #task 2
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0 #sust
            else: sust = 1 
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust)
            if i > 1 and j > 1 and x[i-2] == y[j-1] and y[j-2] == x[i-1]: #rempl
                m[i,j] = min (m[i,j], m[i-2,j-2] + 1)
            if(m[i,j]<valorMin): valorMin = m[i,j]         #task 2
        # print(m, "\n")
        if(valorMin>th) : return th+1                               #task 2
    return min(m[i,j], th+1) 

def dp_restricted_damerau_threshold(x, y, th):
    if(abs(len(x)-len(y)) > th): return th+1        # comparar len
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        valorMin = th+1                              #task 2
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0 #sust
            else: sust = 1 
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust)
            if i > 1 and j > 1 and x[i-2] == y[j-1] and y[j-2] == x[i-1]: #rempl
                m[i,j] = min (m[i,j], m[i-2,j-2] + 1)
            if(m[i,j]<valorMin): valorMin = m[i,j]         #task 2
        # print(m, "\n")
        if(valorMin>th) : return th+1                               #task 2
    return min(m[i,j], th+1) 

def dp_intermediate_damerau_threshold(x, y, th):
    if(abs(len(x)-len(y)) > th): return th+1        # comparar len
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        valorMin = th+1                              #task 2
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0 #sust
            else: sust = 1
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust)
            if i > 1 and j > 1 and x[i-2] == y[j-1] and y[j-2] == x[i-1]: #rempl
                m[i,j] = min (m[i,j], m[i-2,j-2] + 1)
            
            if i > 2 and j > 1 and x[i-3] == y[j-1] and x[i-1] == y[j-2]: 
                m[i,j] = min( m[i,j], m[i-3, j-2] + 2 )  #el borrar y switch
            if i > 1 and j > 2 and y[j-3] == x[i-1] and y[j-1] == x[i-2]: 
                m[i,j] = min( m[i,j], m[i-2, j-3] + 2 ) #el insertar  y switch
            if(m[i,j]<valorMin): valorMin = m[i,j]         #task 2
        if(valorMin>th) : return th+1                              #task 2
    # print(m)
    return min(m[i,j], th+1)

def poliformat_test():
    test = [
            ("algoritmo","algortimo"),
            ("algoritmo","algortximo"),
            ("algoritmo","lagortimo"),
            ("algoritmo","agaloritom"),
            ("algoritmo","algormio"),
            ("acb","ba")
            ]
    thrs = range(1,4)
    for threshold in thrs:
        print(f"thresholds: {threshold:3}")
        for x,y in test:
            print(f"{x:12} {y:12} \t",end="")
            for dist,name in ((dp_levenshtein_threshold,"levenshtein"),
                            (dp_restricted_damerau_threshold,"restricted"),
                            (dp_intermediate_damerau_threshold,"intermediate")):
            
                print(f" {name} {dist(x,y,threshold):2}",end="")
            print()
                 
        """
        Salida del programa:
        thresholds:   1
        algoritmo    algortimo       levenshtein  2 restricted  1 intermediate  1
        algoritmo    algortximo      levenshtein  2 restricted  2 intermediate  2
        algoritmo    lagortimo       levenshtein  2 restricted  2 intermediate  2
        algoritmo    agaloritom      levenshtein  2 restricted  2 intermediate  2
        algoritmo    algormio        levenshtein  2 restricted  2 intermediate  2
        acb          ba              levenshtein  2 restricted  2 intermediate  2
        thresholds:   2
        algoritmo    algortimo       levenshtein  2 restricted  1 intermediate  1
        algoritmo    algortximo      levenshtein  3 restricted  3 intermediate  2
        algoritmo    lagortimo       levenshtein  3 restricted  2 intermediate  2
        algoritmo    agaloritom      levenshtein  3 restricted  3 intermediate  3
        algoritmo    algormio        levenshtein  3 restricted  3 intermediate  2
        acb          ba              levenshtein  3 restricted  3 intermediate  2
        thresholds:   3
        algoritmo    algortimo       levenshtein  2 restricted  1 intermediate  1
        algoritmo    algortximo      levenshtein  3 restricted  3 intermediate  2
        algoritmo    lagortimo       levenshtein  4 restricted  2 intermediate  2
        algoritmo    agaloritom      levenshtein  4 restricted  4 intermediate  3
        algoritmo    algormio        levenshtein  3 restricted  3 intermediate  2
        acb          ba              levenshtein  3 restricted  3 intermediate  2
        """         
if __name__ == "__main__":
    poliformat_test()

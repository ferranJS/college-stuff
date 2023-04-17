import numpy as np

# matrix = np.zeros((len(x), len(y)), int)
# matrix[i, j] = +1


def dp_levenshtein_backwards(x, y):
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0
            else: sust = 1
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust )
    return m[i,j]


def dp_restricted_damerau_backwards(x, y):
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0 #sust
            else: sust = 1
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust)
            if i > 1 and j > 1 and x[i-2] == y[j-1] and y[j-2] == x[i-1]: #rempl
                m[i,j] = min (m[i,j], m[i-2,j-2] + 1)
    return m[i,j]





def dp_intermediate_damerau_backwards(x, y):
    m = np.zeros((len(x)+1, len(y)+1), int) #una fila para la cadena vacía
    for i in range(len(x)+1):
        m[i,0] = i
    for j in range(len(y)+1):
        m[0,j] = j
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]: sust = 0 #sust
            else: sust = 1
            m[i,j] = min( m[i-1,j] + 1, m[i,j-1] + 1, m[i-1,j-1] + sust)
            if i > 1 and j > 1 and x[i-2] == y[j-1] and y[j-2] == x[i-1]: #rempl
                m[i,j] = min (m[i,j], m[i-2,j-2] + 1)
            
            if i > 2 and j > 1 and x[i-3] == y[j-1] and x[i-1] == y[j-2]: 
                m[i,j] = min( m[i,j], m[i-3, j-2] + 2 )  #el borrar y switch
            if i > 1 and j > 2 and y[j-3] == x[i-1] and y[j-1] == x[i-2]: 
                m[i,j] = min( m[i,j], m[i-2, j-3] + 2 ) #el insertar  y switch  /qué falla aquí??
    # print(m)
    return m[i,j]

test = [("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")]

for x,y in test:
    print(f"{x:12} {y:12}",end="")
    for dist,name in ((dp_levenshtein_backwards,"levenshtein"),
                    (dp_restricted_damerau_backwards,"restricted"),
                    (dp_intermediate_damerau_backwards,"intermediate")):
        print(f" {name} {dist(x,y):2}",end="")
    print()
                
"""
Salida del programa:

algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""

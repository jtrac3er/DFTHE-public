import numpy as np
from itertools import permutations
import math

def euler_phi_slow(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)

def canonical_relabel(M):
    n = M.shape[0]
    relabel = {}
    next_color = 0
    M_relabel = np.zeros_like(M)

    for i in range(n):
        for j in range(n):
            val = M[i, j]
            if val not in relabel:
                relabel[val] = next_color
                next_color += 1
            M_relabel[i, j] = relabel[val]

    return M_relabel


def enum_graphs(n):
    for perm in permutations(range(n)):
        perm = np.array(perm)
        M = (perm[:, None] + perm[None, :]) % n
        M[range(N), range(N)] = n+1
        yield canonical_relabel(M)


def count_equal_graphs(n, G_target):
    G_target_canon = canonical_relabel(G_target)
    count = 0

    for G in enum_graphs(n):
        if np.array_equal(G, G_target_canon):
            count += 1

    return count


def create_graph(n):
    # Erstellt die Matrix c(u,v) = (u + v) % n
    nodes = np.arange(n)
    return (nodes[:, None] + nodes[None, :]) % n

# ohne farben permutieren
def create_permuted_graph(n):
    graph = create_graph(n)
    # P ist die Knoten-Permutation (wo landet Knoten i?)
    p = np.random.permutation(n)
    # Sigma ist die Farben-Permutation (was wird aus Farbe i?)
    #sigma = np.random.permutation(n)
    sigma = np.arange(n)
    
    # 1. Knoten permutieren
    g_p = graph[p][:, p]
    
    # 2. Farben permutieren
    g_final = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            g_final[i, j] = sigma[g_p[i, j]]
    
    return g_final, p, sigma    


if __name__ == '__main__':
    for N in range(2, 9):

        # Alle Graphen die es gibt enumerieren und auf gleichheit prüfen
        perm0 = np.arange(N)
        G0 = (perm0[:, None] + perm0[None, :]) % N
        G0[range(N), range(N)] = N+1

        print("N", N, ", Equal Graphs: ", count_equal_graphs(N, G0), f"expected", euler_phi_slow(N)*N)

    print()

    """
    Das beweist, dass die Anzal gleicher Graphen genau phi(N)*N ist, wie ChatGPT es vorausgesagt hat
    Und das ist leider nicht exponentiell, auch nicht wenn N composite ist. Das ist schon mal nicht 
    so gut, aber vielleicht ist das noch nicht das Ende...

    """

    # Die frage ist nun, was ist, wenn man nicht den ursprünglihen Graphen nimmt, sondern eine Permutation davon?

    N = 7
    G,p,_ = create_permuted_graph(N)
    print(G)

    perm0 = np.arange(N)
    G0 = (perm0[:, None] + perm0[None, :]) % N


    print("N:", N, ", Equal Graphs to permuted Graph: ", count_equal_graphs(N, G))

    """
    Auch da genau dasselbe ergebnis.. nicht so gut
    """
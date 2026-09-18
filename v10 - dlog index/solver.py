import numpy as np
from itertools import product
import random
from copy import deepcopy


def create_graph(n):
    # Erstellt die Matrix c(u,v) = (u + v) % n
    nodes = np.arange(n)
    return (nodes[:, None] + nodes[None, :]) % n

def apply_permutation(graph, n):
    # P ist die Knoten-Permutation (wo landet Knoten i?)
    p = np.random.permutation(n)
    # Sigma ist die Farben-Permutation (was wird aus Farbe i?)
    sigma = np.random.permutation(n)
    
    # 1. Knoten permutieren
    g_p = graph[p][:, p]
    
    # 2. Farben permutieren
    g_final = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            g_final[i, j] = sigma[g_p[i, j]]
    
    return g_final, p, sigma    


"""
++++++++ Solver ++++++++++++

"""

# ---------- Hilfsfunktionen ----------

def mod_inv(a, p):
    return pow(int(a), -1, p)

def gauss_jordan_mod_p(A, b, p):
    A = A.copy() % p
    b = b.copy() % p

    m, n = A.shape
    row = 0
    pivots = []

    for col in range(n):
        pivot_rows = np.where(A[row:, col] != 0)[0]
        if pivot_rows.size == 0:
            continue

        pivot = pivot_rows[0] + row
        A[[row, pivot]] = A[[pivot, row]]
        b[[row, pivot]] = b[[pivot, row]]

        inv = mod_inv(A[row, col], p)
        A[row] = (A[row] * inv) % p
        b[row] = (b[row] * inv) % p

        for r in range(m):
            if r != row and A[r, col] != 0:
                factor = A[r, col]
                A[r] = (A[r] - factor * A[row]) % p
                b[r] = (b[r] - factor * b[row]) % p

        pivots.append(col)
        row += 1
        if row == m:
            break

    return A, b, pivots


# ---------- Basis-Extraktion ----------

def solution_basis(A_rref, b_rref, pivots, p):
    m, n = A_rref.shape
    free_vars = [j for j in range(n) if j not in pivots]

    # partikuläre Lösung
    x0 = np.zeros(n, dtype=int)
    for i, col in enumerate(pivots):
        x0[col] = b_rref[i] % p

    # Basisvektoren
    basis = []
    for fv in free_vars:
        v = np.zeros(n, dtype=int)
        v[fv] = 1
        for i, col in enumerate(pivots):
            v[col] = (-A_rref[i, fv]) % p
        basis.append(v)

    return x0, basis


# ---------- Hauptfunktion ----------

def solve_lgs_mod_p(A, b, p, all_solutions=False):
    A = np.asarray(A, dtype=int)
    b = np.asarray(b, dtype=int)

    A_rref, b_rref, pivots = gauss_jordan_mod_p(A, b, p)

    # Konsistenz prüfen
    for i in range(A.shape[0]):
        if np.all(A_rref[i] == 0) and b_rref[i] != 0:
            return {
                "status": "no_solution"
            }

    x0, basis = solution_basis(A_rref, b_rref, pivots, p)

    result = {
        "status": "ok",
        "particular": x0,
        "basis": basis,
        "dimension": len(basis)
    }

    if all_solutions:
        sols = []
        for coeffs in product(range(p), repeat=len(basis)):
            x = x0.copy()
            for a, v in zip(coeffs, basis):
                x = (x + a * v) % p
            sols.append(x)
        result["all_solutions"] = sols

    return result

def create_edge_lgs(g,n):
    A = np.zeros((n, n), dtype=int)
    prev_nodes = set()
    K = 4

    for row in range(n):
        while True:
            nodes = tuple(sorted(random.sample(range(n), K)))
            edges = [(nodes[i], nodes[(i + 1) % K]) for i in range(K)]
            rows, cols = zip(*edges)
            edges_color = g[rows, cols]
            #print(edges_color)
            assert len(edges_color) == K
            if nodes not in prev_nodes:
                prev_nodes.add(nodes)
                break

        values = [(-1)**i for i in range(K)]
        np.add.at(A, (row, edges_color), values)

    return A

def solve(g, n):
    A = create_edge_lgs(g,n)

    edges_solution = solve_lgs_mod_p(A, np.zeros(n), n, all_solutions=False)
    if edges_solution["dimension"] == 0:
        return []

    all_solutions = []
    for edge_sol in edges_solution["basis"]:
        if np.unique(edge_sol).size == n:

            # nun noch die knoten lösen
            A = np.zeros((n, n), dtype=int)
            b = np.zeros((n,), dtype=int)
            for i in range(n):
                A[i, [i, (i+1) % n]] = [1,1]
                b[i] = edge_sol[g[i, (i+1) % n]]

            node_solution = solve_lgs_mod_p(A, b, n)
            assert node_solution["dimension"] == 0
            all_solutions.append(node_solution["particular"])
            print(node_solution)

    return all_solutions


def linear_combination_mod_p(v, vectors, p):
    """
    Prüft v ∈ span(vectors) über Z_p
    """
    A = np.asarray(vectors, dtype=int) % p
    v = np.asarray(v, dtype=int) % p

    # erweitertes LGS: A c = v
    A_ext = np.column_stack([A, v])

    A_rref, b_rref, pivots = gauss_jordan_mod_p(A, v, p)

    # Konsistenzcheck
    for i in range(A.shape[0]):
        if np.all(A_rref[i] == 0) and b_rref[i] != 0:
            return False, None

    # Eine Lösung extrahieren
    coeffs = np.zeros(A.shape[1], dtype=int)
    for i, col in enumerate(pivots):
        coeffs[col] = b_rref[i] % p

    return True, coeffs

def inverse_permutation(p):
    """
    p: NumPy-Array mit einer Permutation
    Rückgabe: inverse Permutation p^{-1}
    """
    inv = np.empty_like(p)
    inv[p] = np.arange(len(p))
    return inv


if __name__ == '__main__':
    
    N = 16

    g, p, s = apply_permutation(create_graph(N), N)
    if N < 30: print(g); print()
    sol = solve(g, N)

    #print(sol)
    if len(sol) == 0:
        print("No solution found (maybe bad random node choice)")
        exit()

    print()
    print("edge_permutation", s, inverse_permutation(s))
    print("node_permutation", p, inverse_permutation(p))

    vectors = np.column_stack(sol + [np.ones(N, dtype=int)])
    ok, coeffs = linear_combination_mod_p(p, vectors, N)

    if ok:
        print("\nSolutions could be found through linear combination:")
        print(coeffs, vectors)
    else:
        print("\nNo solution found (by linear combination)")




import numpy as np
from graph_enumerator import create_permuted_graph
from solver import create_edge_lgs

def rank_mod_2k_numpy(A, k):
    """
    Compute rank of A modulo 2^k using Gaussian elimination
    with only odd pivots (valid over Z / 2^k Z).
    """
    mod = 2 ** k
    A = np.array(A, dtype=np.int64) % mod
    N = A.shape[0]

    rank = 0
    row = 0

    for col in range(N):
        # find pivot with odd entry
        pivot = None
        for r in range(row, N):
            if A[r, col] % 2 == 1:
                pivot = r
                break

        if pivot is None:
            continue

        # swap rows
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]

        # normalize pivot row
        inv = pow(int(A[row, col]), -1, mod)
        A[row] = (A[row] * inv) % mod

        # eliminate other rows
        for r in range(N):
            if r != row and A[r, col] % 2 == 1:
                factor = A[r, col]
                A[r] = (A[r] - factor * A[row]) % mod

        rank += 1
        row += 1
        if row == N:
            break

    return rank


def kernel_size_mod_2n_numpy(A, n):
    """
    Compute |ker(A mod 2^n)| using rank drops on each level.
    """
    A = np.array(A, dtype=np.int64)
    N = A.shape[0]

    exponent = 0
    for k in range(1, n + 1):
        rk = rank_mod_2k_numpy(A, k)
        #print(rk)
        exponent += (N - rk)

    return 2 ** exponent

if __name__ == '__main__':

    n = 7
    N = 2**n
    prev_best = 1e100
    prev_worst = 0

    for _ in range(1000):
        g,p,_ = create_permuted_graph(N)
        #print(g, "\n")
        A = create_edge_lgs(g,N)
        #print(A, "\n")
        no_sols = kernel_size_mod_2n_numpy(A, n)
        if no_sols < prev_best:
            print("best", n, N, no_sols)
            prev_best = no_sols
        if no_sols > prev_worst:
            print("worst", n, N, no_sols)
            prev_worst = no_sols

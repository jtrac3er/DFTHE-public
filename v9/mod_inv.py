import numpy as np

def modinv(a, m):
    """Multiplikatives Inverses von a mod m."""
    # Erweiterter Euklidischer Algorithmus
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        raise ValueError(f"{a} hat kein Inverses modulo {m}")
    return t % m

def matrix_modinv(A, mod):
    """Inverse einer quadratischen Matrix A modulo mod (nur mit NumPy)."""
    n = A.shape[0]
    A = A.copy() % mod
    A = A.astype(object)

    I = np.identity(n, dtype=object)
    AI = np.hstack((A, I))  # Erweitere Matrix: [A | I]

    # Gauß-Jordan-Modulo-Inversion
    for i in range(n):
        # Pivot-Element
        if AI[i, i] == 0:
            for j in range(i+1, n):
                if AI[j, i] != 0:
                    AI[[i, j]] = AI[[j, i]]
                    break
            else:
                raise ValueError("Matrix ist nicht invertierbar mod", mod)

        inv_pivot = modinv(AI[i, i], mod)
        AI[i] = (AI[i] * inv_pivot) % mod

        for j in range(n):
            if j != i:
                factor = AI[j, i]
                AI[j] = (AI[j] - factor * AI[i]) % mod

    A_inv = AI[:, n:]
    assert np.array_equal(A @ A_inv % mod, np.eye(5, dtype=object))
    return A_inv % mod

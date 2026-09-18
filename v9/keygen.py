import sympy
import random
from types import SimpleNamespace
import numpy as np
from matrices import *

def generate_prime(bits=512, divisor=3):
	assert divisor > 1, "Teiler muss > 1 sein"
	while True:
		# Erzeuge zufälliges Vielfaches von divisor
		k = random.getrandbits(bits - divisor.bit_length()) | 1  # Stelle sicher, dass k ungerade ist
		candidate = k * divisor + 1  # dann ist p - 1 teilbar durch divisor
		if sympy.isprime(candidate):
			return candidate

def crt(x, p, y, q):
    N = p*q
    phi = (p-1)*(q-1)
    p1_q0 = pow(q, phi, N)
    p0_q1 = pow(p, phi, N)
    res = (p1_q0*x + p0_q1*y) % N
    assert res % p == x
    assert res % q == y
    return res


def find_unity_root(n, p):
    while (res := pow(random.randint(0, p), (p - 1) // n, p)) == 1: pass
    return res


def keygen(bits=512, n=5):
    p = generate_prime(bits, divisor=n*4)
    q = generate_prime(bits, divisor=n*4)

    bp = sympy.ntheory.sqrt_mod(-1, p)
    bq = sympy.ntheory.sqrt_mod(-1, q)
    up = find_unity_root(n, p)
    uq = find_unity_root(n, q)

    key = SimpleNamespace()
    key.N = p*q
    key.b = crt(bp, p, bq, q)
    key.u = crt(up, p, uq, q)
    key.p = p
    key.q = q

    m = Matrices(key.N, key.u, key.b)
    m.generate()
    key.T_in_1 = m.T_in_1
    key.T_in_2 = m.T_in_2
    key.T_out  = m.T_out
    key.U      = m.U
    key.U_inv  = m.U_inv

    return key

import sys
import os
from random import *

sys.path.append(os.path.abspath("../v7"))
from modnum import *
from complex import *
from convnum import *

sys.path.append(os.path.abspath("../v6"))
from dft import *

def primitive_unity_roots_mod_2k(n, k):
    """
    Find all x such that:
      - x^n ≡ 1 (mod 2^k)
      - ord(x) = n
    """
    modulus = 2 ** k
    roots = []

    def proper_divisors(n):
    	return [d for d in range(1, n) if n % d == 0]

    for x in range(1, modulus, 2):  # nur Einheiten (ungerade)
        if pow(x, n, modulus) != 1:
            continue

        # prüfe kleinere Exponenten
        is_primitive = True
        for d in proper_divisors(n):
            if pow(x, d, modulus) == 1:
                is_primitive = False
                break

        if is_primitive:
            roots.append(x)

    return roots


N = 4			# no elemente
	
m = 32			# bitlänge koeffizienten
M = 2**m 		# Modulo

u = primitive_unity_roots_mod_2k(N, m)
print(u)

v = [ModNum(i, M) for i in range(N)]

c = ConvNum(fourier_transform(u, N, 1, v))

print(c)

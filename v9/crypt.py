from keygen import *
import numpy as np
from random import randint


def cyclic_convolve(a, b):
	n = len(a)
	return np.array([sum(a[k] * b[(i - k) % n] for k in range(n)) for i in range(n)], dtype=object)

def encrypt(x):
	v = np.array([x] + [randint(0, k.N) for _ in range(4)], dtype=object)
	return k.U @ v % k.N

def decrypt(v):
	v = k.U_inv @ v % k.N
	return v[0]

def hom_add(x, y):
	return x + y % k.N

def hom_mul(x, y):
	return k.T_out @ (cyclic_convolve(k.T_in_1 @ x, k.T_in_2 @ y))

if __name__ == '__main__':
	k = keygen(1024)

	print(k.T_in_1)
	print()
	print(k.T_in_2)
	print()
	print(k.T_out)
	print()
	print(k.T_in_1 @ k.T_out % k.N)
	print()
	print(k.T_out @ k.T_in_1 % k.N)
	print("\n")

	c1 = encrypt(10)
	c2 = encrypt(20)
	c_add = hom_add(c1, c2)
	print(decrypt(c_add))

	c_mul = hom_mul(c1, c2)
	print(decrypt(c_mul))
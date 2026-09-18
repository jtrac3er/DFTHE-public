from lgs import *
from convnum import *
from random import randint
from keygen import *
from dft import *
from primes import mod_inverse
import math

# zuerst: Setze p, n fest
n = 3
key = keygenEx(n, 1e10, 9e10, 3)
M = key.N
u = key.u
N = key.p

M_max = int(M**0.5)		


ifft = lambda v : fourier_transform(mod_inverse(u, M), n, 1, v)
ffft = lambda v : fourier_transform(u, n, mod_inverse(n, M), v)

def pwmod(v,p): return [x%p for x in v]

def pwint(v): return [int(x) for x in v]

def pwcheck(v): 
	for x in v: 
		if abs(x) >= M_max: return False
	return True

def encrypt(m, distributed=None):
	if distributed is None:
		r1 = [randint(-M_max // N, M_max // N) for i in range(3)]
		r2 = [randint(-M_max // N, M_max // N) for i in range(3)]		
	else:
		r1 = [randint(-M_max // N, M_max // N) if distributed==i else 
				randint(-100,100) for i in range(3)]
		r2 = [randint(-M_max // N, M_max // N) if distributed==i else 
				randint(-100,100) for i in range(3)]

	v1 = pwmod(ifft(r1), M)
	v2 = pwmod(ifft(r2), M)

	x1 = randint(0, int(N**0.5))
	x2 = (mod_inverse(v2[1], N) * (m - x1*v1[1])) % N		# x2*v2[0] + x1*v1[0] = m

	assert (x2*v2[1] + x1*v1[1]) % N == m

	res = x1*ConvNum(r1) + x2*ConvNum(r2)

	assert ifft(res.l)[1] % N == m
	assert pwcheck(res.l)

	return res


def decrypt(c):
	return ifft(pwmod(c.l, M))[1] % N

def public_keygen():
	return [encrypt(0,i) for i in range(n)]

assert M % N == 0
Np = public_keygen()

def normalize(v, Np=Np, depth=0):
	#assert depth <= 10
	if pwcheck(v.l): return v 
	A = transpose_matrix([nvec.l for nvec in Np])
	x = pwint(gauss_elimination(A, v.l))
	res = v - ConvNum(matrix_mul(A,x))
	print(f"x: {gauss_elimination(A, v.l)}")
	if not pwcheck(res.l):
		# In diesem falle war es wohl zu finde-grained mit Integer, also skaliert
		# nochmals probieren
		return normalize(v, [nvec*10 for nvec in Np], depth+1)
	return res


if __name__ == '__main__':
	m1 = encrypt(1)
	m2 = encrypt(1)
	r = encrypt(0)

	for i in range(1000):
		r += m1
		r *= m2
		r = normalize(r)

	print(r)
	print(decrypt(r))
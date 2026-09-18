from keygen import *
from primes import *
from dft import *

from random import randint
from lgs import *
import numpy as np
from gradient_descent_discrete import *

from convnum import *
from modnum import *
from complex import *

M_ind = 1


def norm(c): return sum([e.l() for e in c.l])

"""
def shrink(c):
	n = len(c.l)
	c -= ConvNum([c.l[0] for i in range(n)])
	k = (n-1) // 2
	return ConvNum(c.l[1:k+1])

def expand(c):
	return ConvNum([Complex(0,0)] + c.l + [e.t() for e in c.l][::-1])
"""

def encrypt(k, m, M):
	e = [Complex(ModNum(randint(0, t_half), k.N), ModNum(0, k.N)) for i in range(k.n)]
	e[M_ind] = Complex(ModNum(m, k.N) + randint(0, t_half//M)*M, ModNum(0, k.N)) 
	return ConvNum(fourier_transform(k.U, k.n, mod_inverse(k.n, k.N), e))

def decrypt(k, c, M):
	e = fourier_transform(k.U.t(), k.n, 1, c.l)
	m = e[M_ind]
	assert m.Im() == 0
	r = m.Re()
	if r.sgn() == -1:	# negativ
		r -= (r.rel() // M -1) * M 	# -1, sodass es sicher positiv ist nachher
		#print("neg", r.x)
	return r.x % M


def generate_cv(k, M):
	cv_1 = [[randint(0, (t_quart if j==i else t_eight) // (M if j==M_ind else 1))*(M if j==M_ind else 1)
		for j in range(k.n)] 
			for i in range(k.n)]

	cv_2 = [[randint(0, (t_eight if j==i else t_quart) // (M if j==M_ind else 1))*(M if j==M_ind else 1)
		for j in range(k.n)] 
			for i in range(k.n)]

	cv_3 = [[randint(0, t_eight // (M if j==M_ind else 1))*(M if j==M_ind else 1) for j in range(k.n)],
			[randint(0, t_quart // (M if j==M_ind else 1))*(M if j==M_ind else 1) for j in range(k.n)]]

	cv = cv_1 + cv_2 + cv_3

	return [ConvNum(fourier_transform(k.U, k.n, mod_inverse(k.n, k.N), v)) 
		for v in cv]


def normalize(cv, c):
	x = gradient_descent_with_oracle(
		lambda x: (3*norm(c - sum([xi*vi for xi,vi in zip(x, cv)]))).x, 
		k.n,
		threshold=t_half)
	res = c - sum([xi*vi for xi,vi in zip(x, cv)])
	assert (3*norm(res)).x <= t_half
	return res 

if __name__ == '__main__':
	M = 1000
	k = keygen(3, 1e50, 9e50)
	
	const_factor = 100
	t_half = int((k.N ** 0.5) // const_factor)
	t_quart = int((k.N ** 0.2) // const_factor)
	t_eight = int((k.N ** 0.1) // const_factor)

	assert M < t_quart

	cv = generate_cv(k, M)
	c = encrypt(k, 2, M)
	c = normalize(cv, c)

	print(f"t_half={t_half}, k.N={k.N}")
	assert (norm(c)*3).x <= t_half

	c_res = c
	for i in range(7):
		c_res = c_res*c
		c_res = normalize(cv, c_res)

	print(decrypt(k, c_res, M))
	print(c_res)

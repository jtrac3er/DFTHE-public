from lgs import *
from convnum import *
from random import randint
from keygen import *
from dft import *
from primes import mod_inverse
import math

import numpy as np
from scipy.linalg import lstsq

# zuerst: Setze p, n fest
N_max = 2**64
n = 3
N = generatePrime(n, N_max // 32, N_max)
u = findUnityRoot(n, N)

M_max = N_max*10
const_value = 1000

ifft = lambda v : fourier_transform(mod_inverse(u, N), n, 1, v)
ffft = lambda v : fourier_transform(u, n, mod_inverse(n, N), v)

def pwmod(v): return [x % N for x in v]
def pwmod_convnum(v): return ConvNum([x % N for x in v.l])
def pwint(v): return [round(x) for x in v]


def generate_normalizators(n):
	# Generiere O(1), O(N), O(N^2) normalisatoren
	# O(1) 		- Verhältnis max : rest O(1) (nur 1 Vektor)
	# O(N) 		- Verhältnis max : rest O(N)
	# O(N^2) 	- Verhältnis max : rest O(N^2)
	
	# Achtung, das ganze ist nicht sicher, da N_o2 direkt durch addition von N
	# erschaffen wurde, nur für test, sonst komplexe linearkombi!

	N_oc = [ConvNum([1 for i in range(n)])]
	N_o1 = [generate_base_normalizator(i,n) for i in range(n)]
	N_o2 = [generate_base_normalizator(i,n) + (randint(N//2, N)*N * ConvNum([
		1 if i==j else 0 for j in range(n)])) for i in range(n)]

	return N_oc, N_o1, N_o2


def generate_base_normalizator(i, n):
	m = 0
	m_index = 1

	rand = [randint(0,const_value) for i in range(n)]
	ones = [1 if i==j else 0 for j in range(n)]

	v1 = pwmod(ifft(rand))
	v2 = pwmod(ifft(ones))

	x2 = (mod_inverse(v2[m_index], N) * (m - v1[m_index])) % N

	assert (x2*v2[m_index] + v1[m_index]) % N == m
	return ConvNum(rand) + x2*ConvNum(ones)


def encrypt(m): 
	# encoding: [l, m, r1, 0, r2]		
	# l : länge des vektors
	# m : message
	# 0 : Für Zerotests muss dieses feld immer 0 sein
	e = [randint(0,N), m, randint(0,N), 0, randint(0,N)]
	c = ConvNum(pwmod(ffft(e)))
	c -= min(c.l) * N_oc[0]
	return c


def decrypt(c):
	e = pwmod(ifft(c.l))
	return e[1]


N_oc, N_o1, N_o2 = generate_normalizators(n)

"""
for nvec in N_oc: print(nvec)
for nvec in N_o1: print(nvec)
for nvec in N_o2: print(nvec)
for nvec in N_oc: print(pwmod(nvec.l))
for nvec in N_o1: print(pwmod(nvec.l))
for nvec in N_o2: print(pwmod(nvec.l))
print()
"""

def lsq(Normalizator, v):
	A = transpose_matrix([nvec.l for nvec in Normalizator])
	x = pwint(gauss_elimination(A, v.l))
	return v - ConvNum(matrix_mul(A,x))


def normalize(c):
	# So, hier muss eine bessere heuristik her. Und zwar die folgende
	# Es wird jede ebene durchgemacht, von O(N^2) zu O(1)

	try:
		if c.norm() < M_max**2: return c

		high = max(c.l)
		low = min(c.l)
		ratio = high / low

		c = lsq(N_o2, c)
		c = lsq(N_o1, c)
		c -= min(c.l) * N_oc[0]

		assert c.norm() < M_max**4
		#print(c)
		return c
	except Exception as e:
		print(f"Exception aufgetreten: {e}")
		print(N)
		print(c)
		exit()


if __name__ == '__main__':
	m1 = encrypt(2)
	m2 = encrypt(0)
	r = encrypt(0)

	for i in range(1000):
		r += m1
		r *= m2
		r = normalize(r)
		#print(r)

	print(M_max**2, N, decrypt(r))
	print(r)

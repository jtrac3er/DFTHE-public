from complex import *
from modnum import *
from primes import *
from random import randint


n = 3

def generatePrime(n, min_rand, max_rand):
	while True:
		p = randint(min_rand, max_rand)*n + 1
		if rabinMiller(p) and legendre(-1, p) == 1:
			return p


def findUnityRoot(n, p):
	while True:
		u = pow(randint(0, p-1), (p-1)//n, p)
		for i in range(1, n):
			if pow(u, i, p) == 1: 
				u = None
				break
		if u is not None:
			return u

for i in range(100):
	p = generatePrime(n, 1e100, 9e100)
	u = findUnityRoot(n, p)
	l = [min(int.bit_length(pow(u,k,p) % p), int.bit_length((-pow(u,k,p)) % p)) for k in range(n)]
	print(int.bit_length(p), l)




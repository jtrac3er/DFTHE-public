from complex import *
from primes import *
from modnum import *
from random import randint

def generatePrime(n, min_rand, max_rand):
	while True:
		p = randint(min_rand, max_rand)*n + 1
		if rabinMiller(p):
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


def findGoodGen(p):
	while True:
		g = randint(0, p-1)
		if legendre(g, p) == -1 % p: 
			return g



p = generatePrime(1, 1e2, 9e2)
g = findGoodGen(p)
x = 2
X = pow(g, x, p)

c = 0
f = 1

print(p,g,x,X,legendre(X,p), legendre(X*mod_inverse(g,p), p), STonelli(X, p) % p)

while X != g:
	if legendre(X, p) == -1 % p: 
		c += f
		X = (X * mod_inverse(g, p)) % p
	X = STonelli(X, p) % p
	print(X)
	f *= 2

print(c)
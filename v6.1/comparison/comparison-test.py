from complex import *
from primes import *
from modnum import *
from random import randint

def generatePrime(n, min_rand, max_rand):
	while True:
		p = randint(min_rand, max_rand)*n + 1
		if rabinMiller(p) and legendre(-1, p) == 1:
			return p

def findUnityRoot(n, p):
	while True:
		u = Complex(ModNum(randint(0, p-1), p),
			 ModNum(randint(0, p-1), p)) ** ((p-1)//n)
		for i in range(1, n):
			if u**i == Complex(1,0): 
				u = None
				break
		if u is not None:
			return u

N = 31
p = generatePrime(4*N, 1e4, 9e4)
u = findUnityRoot(4*N, p)
u = u / ModNum(STonelli(u.l().x, p), p)

print(p)
r = u

for i in range(4*N):
	print(r, r.l(), 2*r.Re())
	r *= u


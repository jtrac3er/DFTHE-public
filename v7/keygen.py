from random import randint
from primes import *
from modnum import *
from complex import *


def generatePrime(n, min_rand, max_rand):
	while True:
		p = randint(min_rand, max_rand)*n + 1
		if rabinMiller(p) and legendre(-1, p) == 1:
			return p


def findUnityRootComplex(n, p):
	while True:
		u = Complex(*[ModNum(randint(0,p), p) for i in range(2)])
		u /= ModNum(STonelli(u.l().x, p), p)
		u = u**((p-1)//n)
		if not u.l() == 1:
			continue
		for i in range(1, n):
			if u**i == Complex(1,0): 
				u = None
				break
		if u is not None:
			return u


def keygen(n, min_rand=1e100, max_rand=9e100):
	p = generatePrime(n, min_rand, max_rand)
	N = p
	U = findUnityRootComplex(n, p)

	class Key: pass
	key = Key()

	key.U = U
	key.N = N
	key.n = n

	assert U**n == Complex(1,0)
	assert U.l() == 1

	return key


def print_key(key):
	for name, value in key.__dict__.items():
		print(f'{name}: {value}')


if __name__ == '__main__':
	# Das war dann die Key-Generation
	n = 3
	key = keygen(n)
	print(f"Key-Generation abgeschlossen. Schlüssel für n={key.n} aus: ")
	print_key(key)


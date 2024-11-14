from random import randint
from primes import *

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



def keygen(n, min_rand=1e300, max_rand=9e300):

	p = generatePrime(n, min_rand, max_rand)
	q = generatePrime(n, min_rand, max_rand)

	N = p*q
	phi = (p-1)*(q-1)
	p1_q0 = pow(q, phi, N)
	p0_q1 = pow(p, phi, N)

	pa = (p+1)//2
	qa = (q+1)//2
	pb = STonelli(-pa**2, p)
	qb = STonelli(-qa**2, q)

	pu = findUnityRoot(n, p)
	qu = findUnityRoot(n, q)

	class Key: pass
	key = Key()

	key.a = (N+1)//2
	key.b = (p1_q0*pb + p0_q1*qb) % N
	key.u = (p1_q0*pu + p0_q1*qu) % N
	key.N = N
	key.n = n
	key.p = p
	key.q = q

	assert ((key.a**2 + key.b**2) % N == 0)
	assert ((key.u ** n) % N == 1)

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


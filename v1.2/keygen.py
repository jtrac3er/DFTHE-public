from complex import *
from prime import *
from random import randint


def generate(n, min_rand, max_rand):

	while True:
		while True:
			p = randint(min_rand, max_rand) * n + 1
			if rabinMiller(p) and pow(-1, (p-1)//2, p) == 1:
				break 

		while True:
			pu = pow(randint(1, p-1), ((p-1)//n), p)
			accepted = True
			for i in range(1,n):
				accepted &= ((pu**i) % p != 1)
			if accepted:
				break

		pa = (p+1)//2
		pb = (STonelli(-(pa**2), p)) % p
		if (pa**2 + pb**2) % p != 0:
			continue

		return p,pu,pa,pb




def keygen(n, min_rand=1e300, max_rand=9e300):

	p,pu,pa,pb = generate(n, min_rand, max_rand)
	q,qu,qa,qb = generate(n, min_rand, max_rand)

	N = p*q
	phi = (p-1)*(q-1)

	p1q0 = pow(q, phi, N)
	p0q1 = pow(p, phi, N)
	assert((p1q0 * p0q1) % N == 0)

	class Key: pass
	k = Key()

	k.n = n
	k.N = N
	k.u = (pu*p1q0 + qu*p0q1) % N
	k.a = (pa*p1q0 + qa*p0q1) % N
	k.b = (pb*p1q0 + qb*p0q1) % N

	assert((k.u**n) % N == 1)
	assert((k.a**2 + k.b**2) % N == 0)

	return k


	
if __name__ == '__main__':
	# Das war dann die Key-Generation
	n = 3
	key = keygen(n)
	print(f"Key-Generation abgeschlossen. Schlüssel für n={key.n} aus (N, u, a, b): ")
	print(f"{key.N}\n{key.u}\n{key.a}\n{key.b}")


from primes import *
from random import randint

def generate_ordn(n, min_rand, max_rand):
	while True:
		while True:
			p = randint(min_rand // n, max_rand // n)*n + 1
			if rabinMiller(p):
				break

		c = pow(randint(0, p), (p-1) // n, p)
		found = True

		for i in range(1,n):
			if pow(c, i, p) == 1:
				found = False
				break

		if found: return p, c


def keygen(n, min_rand=1e300, max_rand=9e300):
	p, pc = generate_ordn(n, min_rand, max_rand)
	q, qc = generate_ordn(n, min_rand, max_rand)

	N = p*q
	phi = (p-1)*(q-1)

	p1_q0 = pow(q, phi, N)
	p0_q1 = pow(p, phi, N)
	assert(p1_q0 * p0_q1 % N == 0)

	class Key: pass
	key = Key()
	key.p1_q0 = p1_q0
	key.p0_q1 = p0_q1
	key.pc = pc
	key.qc = qc
	key.p = p 
	key.q = q

	# Diese beiden sind öffentlich
	key.N = N
	key.n = n

	return key


if __name__ == '__main__':
	# Das war dann die Key-Generation. Der symmetrische key besteht aus 
	# dem Paar (N, uN, n)
	n = 3
	key = keygen(n)
	print(f"Key-Generation abgeschlossen. Schlüssel für n={key.n} aus (N,p,q,pc,qc): ")
	print(f"{key.N}\n\n{key.p}\n\n{key.q}\n\n{key.pc}\n\n{key.qc}")
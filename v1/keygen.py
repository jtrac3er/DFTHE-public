from imag import *
from prime import *
from random import randint

def generate_unity_root(n, min_rand, max_rand):

	def check(rand, p):
		if l(rand, p) != 1 or pot(rand, n, p) != (1,0):
			return False
		for i in range(1, n):
			if pot(rand, i, p) == (1,0):
				return False
		return True

	while True:
		while True:
			p = randint(min_rand, max_rand)
			if (p**2 -1) % n == 0 and rabinMiller(p):
				break

		for i in range(n*3):
			rand = (randint(0, p), randint(0, p))
			uc = pot(rand, (p**2 -1) // n, p)
			if check(uc, p):
				return p, uc


def keygen(n, min_rand=1e300, max_rand=9e300):
	p, up = generate_unity_root(n, min_rand, max_rand)
	q, uq = generate_unity_root(n, min_rand, max_rand)

	N = p*q
	phi = (p-1)*(q-1)

	p1_q0 = pow(q, phi, N)
	p0_q1 = pow(p, phi, N)
	assert(p1_q0 % p == 1 and p1_q0 % q == 0)
	assert(p0_q1 % p == 0 and p0_q1 % q == 1)

	uN = add(smul(p1_q0, up, N), smul(p0_q1, uq, N), N)
	assert(pot(uN, n, N) == (1,0) and l(uN, N) == 1)

	s = pow(n, phi-1, N)
	assert((s*n) % N == 1)

	class Key(): pass
	key = Key()
	key.n = n
	key.N = N
	key.uN = uN
	key.s = s
	return key


if __name__ == '__main__':
	# Das war dann die Key-Generation. Der symmetrische key besteht aus 
	# dem Paar (N, uN, n)
	n = 5
	key = keygen(n)
	print(f"Key-Generation abgeschlossen. Schlüssel für n={key.n} aus (n, N, uN0, uN1, scale): ")
	print(f"{key.N}\n{Re(key.uN)}\n{Im(key.uN)}\n{key.s}")
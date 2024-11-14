from random import randint
from keygen import keygen

def _encrypt(m, n, p, pc):
	 acc = 0
	 res = []

	 for i in range(n):
	 	if i == (n -1): r = (m - acc) % p
	 	else: r = randint(1, p)

	 	acc = (acc + r) % p
	 	x = (r * pow(pc, i, p)) % p
	 	res.append(x)

	 assert (acc == m)
	 return res


def _decrypt(c, n, p, pc):
	m = 0
	for i in range(n):
		m = (m + c[i] * pow(pc, n-i, p)) % p
	return m


# p: Wird für Message gebraucht
# q: Wird für Checksum gebraucht
def encrypt(m, k, s=None):
	if not s: s = randint(0, k.q)
	em = _encrypt(m, k.n, k.p, k.pc)
	es = _encrypt(s, k.n, k.q, k.qc)
	return [(x*k.p1_q0 + y*k.p0_q1) % k.N for x,y in zip(em,es)]


def decrypt(c, k):
	em = [i % k.p for i in c]
	es = [i % k.q for i in c]
	return _decrypt(em, k.n, k.p, k.pc), _decrypt(es, k.n, k.q, k.qc)


def hom_add(c1, c2, N):
	return [(x + y) % N for x,y in zip(c1,c2)]

def hom_mul(c1, c2, N):
	n = len(c1)
	result = [0 for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[(i+j) % n] = (result[(i+j) % n] + c1[i] * c2[j]) % N
	return result


if __name__ == '__main__':
	
	key = keygen(3, min_rand=1e4, max_rand=9e4)
	N = key.N

	n1 = 0
	n2 = 30
	m1 = encrypt(n1, key)
	m2 = encrypt(n2, key)
	m_add = hom_add(m1, m2, N)
	m_mul = hom_mul(m1, m2, N)

	print(m1)
	print(m2)
	print(m_add)
	print(m_mul)

	print(decrypt(m1, key)[0])
	print(decrypt(m2, key)[0])
	print(decrypt(m_add, key)[0])
	print(decrypt(m_mul, key)[0])

from random import randint
from primes import *
from convnum import *
from dft import *

const_value = 1000
M_ind = 1

def generatePrime(n, min_rand, max_rand):
	while True:
		p = randint(min_rand, max_rand)*n + 1
		if rabinMiller(p) and legendre(-1, p) == 1:
			return p


def findUnityRoot(n, p, nPrime=False):
	while True:
		u = pow(randint(0, p-1), (p-1)//n, p)

		if nPrime:
			if u != 1: return u
			else: continue 
		
		for i in range(1, n):
			if pow(u, i, p) == 1: 
				u = None
				break
		if u is not None:
			return u


def pwmod(v, N): return [x % N for x in v]


def generate_normalizators(n, ifft, N):

	def generate_base_normalizator(i, n):
		m = 0
		m_index = 1
		rand = [randint(0,const_value) for i in range(n)]
		ones = [1 if i==j else 0 for j in range(n)]

		v1 = ifft(rand)
		v2 = ifft(ones)
		x2 = (mod_inverse(v2[m_index], N) * (m - v1[m_index])) % N

		assert (x2*v2[m_index] + v1[m_index]) % N == m
		return ConvNum(rand) + x2*ConvNum(ones)

	# Generiere O(N), O(N^2) normalisatoren
	# O(N) 		- Verhältnis max : rest O(N)
	# O(N^2) 	- Verhältnis max : rest O(N^2)
	
	N_o1 = [generate_base_normalizator(i,n) for i in range(n)]
	N_o2 = [generate_base_normalizator(i,n) + (randint(N//2, N)*N * ConvNum([
		1 if i==j else 0 for j in range(n)])) for i in range(n)]

	return [N_o1, N_o2]


def generate_evaluation_keys_RSA(M,n,u):
	p = generatePrime(M, 1e4, 9e4)		# für sicherheit mindestens 1e100 !
	q = generatePrime(M, 1e4, 9e4)
	pu = findUnityRoot(M, p, nPrime=True)
	qu = findUnityRoot(M, q, nPrime=True)
	N = p*q
	p1q0 = pow(q, p-1, N)
	p0q1 = pow(p, q-1, N)
	g = (pu*p1q0 + qu*p0q1) % N
	assert pow(g, M, N) == 1

	gl = []
	for i in range(n):
		gl.append(pow(g, pow(u,i,M), N))

	return N, gl


def keygen(n=3, bitlength=64, checksum=False):
	
	class key: pass
	SK = key()
	PK = key()
	HK = key()
	EK = key()

	if not checksum:
		SK.N = N = generatePrime(n, 2**(bitlength-3), 2**bitlength)
		SK.u = u = findUnityRoot(n, N)
	else:
		m = generatePrime(n, 2**(bitlength-3), 2**bitlength)
		c = generatePrime(n, 2**(bitlength-3), 2**bitlength)
		bitlength *= 2
		mu = findUnityRoot(n, m)
		cu = findUnityRoot(n, c)
		SK.N = N = m*c
		m1c0 = pow(c, m-1, N)
		m0c1 = pow(m, c-1, N)

		SK.u = u = (mu*m1c0 + mu*m0c1) % N
		SK.m1c0 = m1c0
		SK.m0c1 = m0c1
		SK.m = m
		SK.c = c

	SK.n = n
	SK.M_ind = M_ind
	SK.checksum = checksum 

	ifft = lambda v : pwmod(fourier_transform(mod_inverse(u, N), n, 1, v), N)

	HK.CVL = generate_normalizators(n, ifft, N)
	EK.G, EK.gl = generate_evaluation_keys_RSA(N, n, mod_inverse(u, N))
	HK.M_max = 2**(bitlength*4)
	HK.N_max = 2**bitlength
	HK.n = n

	PK.k = 0	# keine message slots
	PK.l = []	# leere liste
	PK.HK = HK

	EK.n = n
	EK.type = "RSA"

	return SK,HK,PK,EK



def print_key(key):
	for name, value in key.__dict__.items():
		print(f'{name}: {value}')


def print_cv(cvl):
	for l in cvl:
		for v in l: print(v)
		print("---------")


if __name__ == '__main__':
	SK,HK,PK,EK = keygen(checksum=True)
	print(f"Key-generation done. Outputting the secret key SK: ")
	print_key(SK)



from lgs import *
from convnum import *
from random import randint
from keygen import *
from dft import *
from primes import mod_inverse


ifft = lambda n,u,N,v : fourier_transform(mod_inverse(u, N), n, 1, v)
ffft = lambda n,u,N,v : fourier_transform(u, n, mod_inverse(n, N), v)

def pwmod(v, N): return [x % N for x in v]
def pwint(v): return [round(x) for x in v]


def encrypt(SK, m): 
	e = [randint(0,SK.N) for i in range(SK.n)]
	e[SK.M_ind] = m
	c = ConvNum(pwmod(ffft(SK.n, SK.u, SK.N, e), SK.N))
	#c -= min(c.l, key=abs) * ConvNum([1 for i in range(SK.n)])
	c -= c.l[0] * ConvNum([1 for i in range(SK.n)])
	return c


def decrypt(SK, c):
	e = pwmod(ifft(SK.n, SK.u, SK.N, c.l), SK.N)
	return e[SK.M_ind]


def normalize(c, *cvl_list):

	def lsq_approx(Normalizator, v):
		A = transpose_matrix([nvec.l for nvec in Normalizator])
		x = pwint(lgs_solve(A, v.l))
		return v - ConvNum(matrix_mul(A,x))

	try:
		#if c.norm() < M_max**2: return c
		for cv in cvl_list: c = lsq_approx(cv, c)
		#c -= min(c.l, key=abs) * N_oc[0]
		c -= c.l[0] * ConvNum([1 for i in range(len(c.l))])
		#assert c.norm() < M_max**4
		#print(c)
		return c
	except Exception as e:
		print(f"Exception occured: {e}")
		print(N, c)
		exit(1)


def hom_eval(EK, c):
	res = 1
	for i in range(EK.n): 
		res = (res * pow(EK.gl[i], c.l[i], EK.G)) % EK.G
	return res

def hom_mul(HK,c1,c2): return normalize(c1*c2, *HK.CVL)

def hom_add(HK,c1,c2): return normalize(c1+c2, *HK.CVL)

def hom_smul(HK,s,c): return normalize(s*c, *HK.CVL)

def hom_pot(HK,c,e): return normalize(c**e, *HK.CVL)


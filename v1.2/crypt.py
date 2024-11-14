from complex import * 
from random import randint
from prime import *
from keygen import keygen


def qft(qu, v, s=1):
	n = len(v)
	res = [CZero for i in range(n)]
	for i in range(n):
		for j in range(n):
			res[i] += (qu**(i*j)) * v[j]
		res[i] *= s
	return res

def encrypt_vector(k, ml):
	z0 = Complex(k.a, k.b)
	z1 = Complex(k.a, -k.b)
	e = [z0*x + z1*y for x,y in ml]
	cu = (Complex(k.u,0))*z0 + (Complex(k.u,0)**((k.n+1)//2))*z1
	#cu = (Complex(k.u,0))*z0 + Complex(randint(0,k.N), randint(0,k.N))
	return qft(cu, e, mod_inverse(k.n, k.N))

def decrypt_vector(k, cl):
	z0 = Complex(k.a, k.b)
	z1 = Complex(k.a, -k.b)
	cu = (Complex(k.u,0))*z0 + (Complex(k.u,0)**((k.n+1)//2))*z1
	#cu = (Complex(k.u,0))*z0 + z1
	e = qft(cu**-1, cl, 1)
	inv = mod_inverse((k.N+1) // 2, k.N)
	return [((qe*z0).Re()*inv % k.N , (qe*z1).Re()*inv % k.N) for qe in e]


# Hier muss das super encoding zum Zuge
def encrypt(k, m, s=0):
	vec = [(1,1), (m, randint(0, k.N)), (s, randint(0, k.N))]
	return encrypt_vector(k, vec)

def decrypt(k, c, se=0):
	vec = decrypt_vector(k, c)
	m = vec[1][0]
	s = vec[2][0]
	if s != se:
		#raise ValueError(f"Decryption failed, s != se: s={s}, se={se}")
		pass
	return m


def hom_mul(c1, c2):
	n = len(c1)
	result = [CZero for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[(i+j) % n] += c1[i] * c2[j]
	return result

def hom_add(c1, c2):
	return [x + y for x,y in zip(c1,c2)]

def hom_smul(s, c):
	return [s*x for x in c]

def hom_pow(c, e):	# langsam, kein sqam
	res = [CUnit] + [CZero for i in range(len(c)-1)]
	for i in range(e):
		res = hom_mul(res, c)
	return res

def pp_vec(v):
	print("\nvector dump:")
	for q in v: print(q)


if __name__ == '__main__':

	n = 3
	k = keygen(n, min_rand=1e20, max_rand=9e20)
	Complex.N = k.N

	"""
	m1 = [(randint(0,10), randint(0,10)) for i in range(n)]
	m2 = [(randint(0,10), randint(0,10)) for i in range(n)]

	print("m1")
	pp_vec(m1)
	print("\nm2")
	pp_vec(m2)
	
	c1 = encrypt_vector(k, m1)
	c2 = encrypt_vector(k, m2)

	print("\nadd")
	pp_vec(decrypt_vector(k, hom_add(c1, c2)))
	print("\nmul")
	pp_vec(decrypt_vector(k, hom_mul(c1, c2)))
	"""

	m1 = 10
	m2 = 23

	c1 = encrypt(k, m1)
	c2 = encrypt(k, m2)

	c_add = hom_add(c1, c2)
	c_mul = hom_mul(c1, c2)

	print(decrypt(k, c_add))
	print(decrypt(k, c_mul))

	pp_vec(c1)
	pp_vec(c2)



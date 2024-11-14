from keygen import *
from primes import *
from dft import *

from random import randint

from complex import *
from convnum import *
from modnum import *


def encrypt(k, m):
	b0 = Complex(k.a, k.b)
	b1 = Complex(k.a, -k.b)

	m1 = m2 = m
	r1 = randint(1,k.N)
	r2 = randint(1,k.N)

	z1 = m1*b0 + r1*b1
	z2 = r2*b0 + m2*b1

	v1 = [0, z1.Re(), z2.Re()]
	v2 = [0, z1.Im(), z2.Im()]

	A = fourier_transform(k.u, k.n, mod_inverse(k.n, k.N), v1)
	B = fourier_transform(k.u, k.n, mod_inverse(k.n, k.N), v2)

	return Complex(ConvNum(A), ConvNum(B))


def decrypt(k, c):
	b0 = Complex(k.a, k.b)
	b1 = Complex(k.a, -k.b)

	A,B = c.Re(), c.Im()
	v1 = fourier_transform(k.u**-1, k.n, 1, A.l)
	v2 = fourier_transform(k.u**-1, k.n, 1, B.l)
	z1 = Complex(v1[1], v2[1])
	z2 = Complex(v1[2], v2[2])

	# x*a = z  <==>  x = z / a
	m1 = (z1*b0).Re() / k.a
	r1 = (z1*b1).Re() / k.a
	r2 = (z2*b0).Re() / k.a
	m2 = (z2*b1).Re() / k.a

	assert m1 == m2
	return m1.x			# weil modnum


def init_key(key):
	key.u = ModNum(key.u, key.N)
	key.a = ModNum(key.a, key.N)
	key.b = ModNum(key.b, key.N)
	return key


if __name__ == '__main__':
	key = init_key(keygen(3, min_rand=1e3, max_rand=9e3))
	
	m1 = 34
	m2 = 17
	
	c1 = encrypt(key, m1)
	c2 = encrypt(key, m2)
	print(c1)
	print(c2)

	c_mul = c1 * c2
	c_add = c1 + c2

	print(decrypt(key, c_mul))
	print(decrypt(key, c_add))


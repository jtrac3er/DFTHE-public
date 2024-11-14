"""
So nun geht es darum, auch zu verschlüsseln und all das
"""

from keygen import keygen
from random import randint
from imag import *


def create_dft_matrix(unity_root, n, s, p):
	m = [[None for i in range(n)] for i in range(n)]
	for i in range(n):
		for j in range(n):
			m[i][j] = pot(unity_root, i*j, p)
			m[i][j] = smul(s, m[i][j], p)
	return m


def matrix_mul(A,x,p):
	n = len(x)
	result = [(0,0) for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[i] = add(result[i], mul(A[i][j], x[j], p), p)
	return result


def convolve(v,w,p):
	n = len(v)
	result = [(0,0) for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[(i+j) % n] = add(result[(i+j) % n], mul(v[i], w[j], p), p)
	return result

def pw_mul(v,w,p):
	return [mul(x,y,p) for x,y in zip(v,w)]

def pw_add(v,w,p):
	return [add(x,y,p) for x,y in zip(v,w)]


# Für das encoding muss n gesetzt werden
# Support für Checksum muss eingebaut werden, denn checksum (0,0) ist unsicher
n = 5

def encode(m, p):
	# m | c | r | m | r
	return [(m,0), (0,0), (randint(0,p), randint(0,p)), (m,0), (randint(0,p), randint(0,p))]

def decode(e, p):
	if e[0] != e[3]:
		raise ValueError("Invalid Ciphertext, m0!=m3")
	if Im(e[0]) != 0:
		raise ValueError("Invalid Ciphertext, Im!=0")
	if e[1] != (0,0):
		raise ValueError("Invalid Ciphertext, checksum failed")
	return Re(e[0]) % p

def generate_zero_test(k):
	e = [(randint(0,k.N), randint(0,k.N)), (0,0), (0,0), (randint(0,k.N), randint(0,k.N)), (0,0)]
	return encrypt_vec(e, k)

def encrypt_num(m, k):
	return encrypt_vec(encode(m, k.N), k)

def decrypt_num(c, k):
	return decode(decrypt_vec(c, k), k.N)

def encrypt_vec(v, k):
	return matrix_mul(
		create_dft_matrix(k.uN, k.n, k.s, k.N), 
		v, 
		k.N)

def decrypt_vec(w, k):
	return matrix_mul(
		create_dft_matrix(t(k.uN, k.N), k.n, 1, k.N), 
		w, 
		k.N)


def hom_mul(c1, c2, N):
	return convolve(c1, c2, N)

def hom_add(c1, c2, N):
	return pw_add(c1, c2, N)

def hom_zero_mum(c1, ztest, N):
	res = convolve(c1, ztest, N)
	for num in res:
		if num != (0,0):
			return False
	return True


if __name__ == '__main__':

	key = keygen(n, min_rand=1e4, max_rand=9e4)
	N = key.N

	n1 = 10
	n2 = 30
	m1 = encrypt_num(n1, key)
	m2 = encrypt_num(n2, key)
	ztest = generate_zero_test(key)

	m_add = hom_add(m1, m2, N)
	m_mul = hom_mul(m1, m2, N)

	print(m1)
	print(m2)

	print(decrypt_num(m1, key))
	print(decrypt_num(m2, key))
	print(decrypt_num(m_add, key))
	print(decrypt_num(m_mul, key))

	print(hom_zero_num(m_mul, ztest, N))


# Für sicherheitsbeweise, siehe security.txt
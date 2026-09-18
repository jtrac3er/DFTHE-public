import numpy as np 
from random import randint
from sympy import Matrix
from mod_inv import matrix_modinv

class Matrices:

	def __init__(self, N, u, b):
		self.N = N 
		self.u = u 
		self.b = b

	def generate(self):
		N = self.N
		V, V_inv = self.generate_V_V_inv()
		U, U_inv = self.generate_U_U_inv()
		D1, D2, D3 = self.generate_3_D()

		A_in_1 = self.generate_split()    @ self.generate_z2encode() % N
		A_in_2 = self.generate_split()    @ self.generate_z2encode() % N
		A_out  = self.generate_z2decode() @ self.generate_combine()  % N

		self.T_in_1 = V @ D1    @ A_in_1  @ U_inv % N
		self.T_in_2 = V @ D2    @ A_in_2  @ U_inv % N
		self.T_out  = U @ A_out @ D3      @ V_inv % N

		self.U 		= U
		self.U_inv  = U_inv

	# Non-checksum version
	"""
	def generate_z2encode(self):
		def r(): return randint(0, self.N)
		re = (self.N + 1) // 2 
		im = re * self.b % self.N
		return np.array([
			[re, re, re, re, re ],
			[im,-im,-im,-im,-im ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)

	def generate_z2decode(self):
		def r(): return randint(0, self.N)
		b = self.b
		return np.array([
			[1,  -b, 0,  0,  0, ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)
	"""

	def generate_z2encode(self):
		def r(): return randint(0, self.N)
		re = (self.N + 1) // 2 
		im = re * self.b % self.N
		return np.array([
			[re, re,  0,  0,  0 ],
			[im,-im,  0,  0,  0 ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)


	def generate_z2decode(self):
		def r(): return randint(0, self.N)
		b = self.b
		return np.array([
			[1,  -b, 0,  0,  0, ],
			[1,   b, 0,  0,  0, ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)


	def generate_split(self):
		def r(): return randint(0, self.N)
		return np.array([
			[1,  1,  0,  0,  0  ],
			[1,  0,  0,  0,  0  ],
			[0,  1,  0,  0,  0  ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)

	def generate_combine(self):
		def r(): return randint(0, self.N)
		return np.array([
			[0,  1, -1,  0,  0  ],
			[1, -1, -1,  0,  0  ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)

	def generate_3_D(self):
		r1 = np.array([randint(1, self.N-1) for _ in range(5)], dtype=object)
		r2 = np.array([randint(1, self.N-1) for _ in range(5)], dtype=object)
		r3 = np.array([pow(x*y, -1, self.N) for x,y in zip(r1, r2)])
		return np.diag(r1), np.diag(r2), np.diag(r3)


	def generate_U_U_inv(self):
		try:
			U = np.array([[randint(0, self.N) for _ in range(5)]
					 for _ in range(5)], dtype=object)
			U_inv = matrix_modinv(U, self.N)
			return U % self.N, U_inv % self.N
		except ValueError:
			return self.generate_U_U_inv()	# retry


	def generate_V_V_inv(self):
		V = np.array([[pow(self.u, i*j, self.N) for i in range(5)] 
			for j in range(5)], dtype=object) * pow(5, -1, self.N)
		return V, matrix_modinv(V, self.N)



if __name__ == '__main__':

	from keygen import *
	k = keygen(16)
	M = Matrices(k.N, k.u, k.b)
	N = k.N

	D = M.generate_3_D()[0]

	print(M.generate_z2decode() @ M.generate_z2encode() % N)
	print()
	print(M.generate_combine() @ M.generate_split() % N)
	print()
	print(M.generate_split()  @  M.generate_z2encode() % N)
	print()
	print(M.generate_z2decode() @ M.generate_combine()  % N)
	print()
	print((M.generate_z2decode() @ M.generate_combine() @ D @
		   M.generate_split()  @  M.generate_z2encode()) % N)

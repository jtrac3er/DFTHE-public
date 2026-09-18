from matrices import Matrices

# geht nicht so!!! Man kann [1, r] nicht einfach so erstellen, das geht nicht
# dafür bräuchte man eine lineare transformation, welche eine addition erforder

class Matrices2 (Matrices):

	def __init__(self, N, u, b):
		super().__init__(N, u, b)


	def generate(self):

		V, V_inv = self.generate_V_V_inv()
		U, U_inv = self.generate_U_U_inv()
		D1, D2, D3 = self.generate_3_D()

		self.Ds = []
		for i in range(3):
			self.Ds.append(self.generate_3_D())
 
		# [x, r]
		A_in_1 = self.generate_split()   @ self.generate_z2encode() % N
		A_in_2 = self.generate_split()   @ self.generate_z2encode() % N
		A_out = self.generate_z2decode() @ self.generate_combine()  % N

		self.T_in_1_1 = V @ D[0][0]    @ A_in_1  @ U_inv % N
		self.T_in_2_1 = V @ D[0][1]    @ A_in_2  @ U_inv % N
		self.T_out_1  = U @ A_out @ D[0][1]      @ V_inv % N


		# [1, r]
		V, V_inv = self.generate_V_V_inv()
		U, U_inv = self.generate_U_U_inv()
		D1, D2, D3 = self.generate_3_D()

		A_in_1 = self.generate_split()     @ self.generate_z2encode_2() % N
		A_in_2 = self.generate_split()     @ self.generate_z2encode_2() % N
		A_out = self.generate_z2decode_2() @ self.generate_combine()    % N

		self.T_in_1_1 = V @ D[0][0]    @ A_in_1  @ U_inv % N
		self.T_in_2_1 = V @ D[0][1]    @ A_in_2  @ U_inv % N
		self.T_out_1  = U @ A_out @ D[0][1]      @ V_inv % N



	def generate_z2encode_2(self):
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


	def generate_z2decode_2(self):
		def r(): return randint(0, self.N)
		b = self.b
		return np.array([
			[1,  -b, 0,  0,  0, ],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
			[r(),r(),r(),r(),r()],
		], dtype=object)
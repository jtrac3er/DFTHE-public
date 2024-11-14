# Modulare zahlen

from primes import mod_inverse

class ModNum:

	def UNIT(self): return ModNum(1, self.N)
	def ZERO(self): return ModNum(0, self.N)

	def __init__(self, x, N):
		self.N = N
		self.x = x % self.N

	def __add__(self, o):
		try:
			if type(o) == type(self):
				return ModNum(self.x + o.x, self.N)
			else:
				return ModNum(self.x + o, self.N)
		except TypeError:
			return NotImplemented

	def __sub__(self, o):
		return self + (o * -1)

	def __neg__(self):
		return ModNum(-self.x, self.N)

	def __mul__(self, o):
		try:
			if type(o) == type(self):
				return ModNum(self.x * o.x, self.N)
			else:
				return ModNum(self.x * o, self.N)
		except TypeError:
			return NotImplemented

	def __rmul__(self, o):	# skalarmultiplikation andere Seite
		return self * o

	def __pow__(self, e):
		if not type(e) == int:
			raise ValueError("Exponent has to be integer")
		if e < 0:
			return ModNum(mod_inverse(self.x, self.N), self.N)**abs(e)
		return ModNum(pow(self.x, int(e), self.N), self.N)

	def __eq__(self, o):
		if type(self) == type(o):
			return self.x == o.x
		else:
			return self.x == o

	def __truediv__(self, o):
		return self * o**-1

	def __floordiv__(self, o):
		return self.__truediv__(o)

	def __str__(self):
		#return f"{self.x} mod {self.N}"
		return f"{self.x}'"
		#return f"{self.x}"



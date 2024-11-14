# Modul wird verallgemeinert, sodass es über anderen Körpern arbeitet
# Alle typechecks wurden weggenommen

class Complex:

	def UNIT(self): return Complex(self.a.UNIT(), self.b.ZERO())
	def ZERO(self): return Complex(self.a.ZERO(), self.b.ZERO())

	def __init__(self, a, b):
		self.a = a
		self.b = b 

	def __add__(self, o):
		return Complex(self.a+o.a, self.b+o.b)

	def __sub__(self, o):
		return self + (o * -1)

	def __neg__(self):
		return Complex(-self.a, -self.b)

	def __mul__(self, o):
		try:
			if type(o) == type(self):					# Complex-Complex
				return Complex(self.a*o.a - self.b*o.b, self.a*o.b + self.b*o.a)
			else: # 									# skalarmultiplikation
				return Complex(o*self.a, o*self.b)
		except TypeError:
			return NotImplemented

	def __rmul__(self, o):	# skalarmultiplikation andere Seite
		return self * o

	def __pow__(self, e):
		if not type(e) == int:
			raise ValueError("Exponent has to be integer")
		if e == 0:
			return Complex.UNIT(self)
		if e < 0:
			return self.__inv()**abs(e)
		binary = [0 if b == '0' else 1 for b in bin(e)[2:]][::-1]
		start = self
		res = None
		for b in binary:
			if b == 1:
				if res is not None: res = res * start
				else: res = start
			start = start * start
		return res

	def __eq__(self, o):
		return self.a == o.a and self.b == o.b

	def __truediv__(self, o):
		return self * (o**-1)

	def __inv(self):
		inv = self.t()
		scale = inv.l() ** -1
		return inv*scale

	def t(self):
		return Complex(self.a, -self.b)

	def l(self):
		return self.a**2 + self.b**2

	def Re(self):
		return self.a

	def Im(self):
		return self.b

	def __str__(self):
		return f"C({self.a},{self.b})"


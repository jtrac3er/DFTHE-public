
from prime import mod_inverse	# Wird eigentlich nur bei inversem gebraucht

class Complex:

	N = None

	def __init__(self, a, b):
		self.a = a % Complex.N if Complex.N else a
		self.b = b % Complex.N if Complex.N else b

	def __add__(self, o):
		if not type(o) == type(self):
			raise ValueError("Cannot add non-complex to complex")
		return Complex(self.a+o.a, self.b+o.b)

	def __sub__(self, o):
		return self + (o * -1)

	def __mul__(self, o):
		if type(o) == int or type(o) == float:		# skalarmultiplikation
			return Complex(o*self.a, o*self.b)
		elif type(o) == type(self):					# Complex-Complex
			return Complex(self.a*o.a - self.b*o.b, self.a*o.b + self.b*o.a)
		else:
			raise ValueError("Only scalar or complex multiplication possible")

	def __rmul__(self, o):	# skalarmultiplikation andere Seite
		return self * o

	def __pow__(self, e):
		if not type(e) == int:
				raise ValueError("Exponent has to be integer")
		if e < 0:
			return self.__inv()**abs(e)
		binary = [0 if b == '0' else 1 for b in bin(e)[2:]][::-1]
		start = self
		res = Complex(1,0)
		for b in binary:
			if b == 1:
				res = res * start
			start = start * start
		return res

	def __eq__(self, o):
		if not type(o) == type(self):
				raise ValueError("Can only compare Complex to Complex")
		return self.a == o.a and self.b == o.b

	def __mod__(self, m):
		if not type(m) == int:
			if Complex.N:
				raise ValueError("Can only modulo when Complex.N is None")
			q = self
			q._mod(m)
			return q
		else:
			raise ValueError("Can only modulo with integer")

	def __truediv__(self, o):
		return self * (o**-1)

	def __inv(self):
		try:
			inv = self.t()
			if Complex.N:
				scale = mod_inverse(inv.l(), Complex.N)
			else:
				scale = 1 / inv.l()
			return inv*scale
		except ValueError:	# inverses existiert nicht
			error = ZeroDivisionError("Inverse does not exist")
			error.inv = self
			raise error

	def t(self):
		return Complex(self.a, -self.b)

	def l(self):
		s = self.a**2 + self.b**2
		return s % Complex.N if Complex.N else s

	def Re(self):
		return self.a

	def Im(self):
		return self.b

	def __str__(self):
		return f"C({self.a},{self.b})"


CUnit = Complex(1,0)
CZero = Complex(0,0)


if __name__ == '__main__':
	#"""
	Complex.N = 11
	q1 = Complex(1,2)
	q2 = Complex(4,2)
	qas = CUnit
	qas *= q2

	print(q1 - q2)
	print(q2 * 3)
	print(3 * q2)
	print(q1 * q2)
	print(q2 ** 3)
	print(qas)
	print(q2.t())
	print(q1.l())
	print(q1 ** -2)
	print(q2 / q1)
	print(CUnit == CZero)
	print(CUnit != CZero)
	#"""



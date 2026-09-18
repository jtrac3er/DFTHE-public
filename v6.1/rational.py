# Modulare zahlen

from math import gcd

class Rational:

	def __init__(self, a, b):	# a / b
		if b < 0:
			b = -b
			a = -a
		if b == 0:
			ValueError("Deminator cannot be zero")
		cd = gcd(a,b)
		self.a = a // cd
		self.b = b // cd

	def __add__(self, o):
		try:
			if type(o) == type(self):
				return Rational(self.a*o.b + o.a*self.b, self.b * o.b)
			else:	# int
				return Rational(self.a + o*self.b, self.b)
		except TypeError:
			return NotImplemented

	def __sub__(self, o):
		return self + (o * -1)

	def __neg__(self):
		return Rational(-self.a, self.b)

	def __mul__(self, o):
		try:
			if type(o) == type(self):
				return Rational(self.a * o.a, self.b * o.b)
			else:
				return Rational(self.a * o, self.b)
		except TypeError:
			return NotImplemented

	def __rmul__(self, o):	# skalarmultiplikation andere Seite
		return self * o

	def __pow__(self, e):
		if not type(e) == int:
			raise ValueError("Exponent has to be integer")
		if e < 0:
			return Rational(self.b, self.a)**abs(e)
		elif e == 0:
			return Rational(1, 0)
		else:
			return Rational(self.a ** e, self.b ** e)

	def __eq__(self, o):
		if type(self) == type(o):
			return self.a == o.a and self.b == o.b
		else:	#int
			return self.a == o and self.b == 1

	def __truediv__(self, o):
		return self * o**-1

	def __floordiv__(self, o):
		return self.__truediv__(o)

	def __str__(self):
		return f"{self.a}/{self.b}"



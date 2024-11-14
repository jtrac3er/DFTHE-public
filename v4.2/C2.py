from primes import mod_inverse
from complex import *
# ( (a,b), (c,d) )

class C2:

	N = None

	def __init__(self,*args):
		Complex.N = C2.N
		if len(args) == 4:
			a,b,c,d = args
			self.x = Complex(a,b)
			self.y = Complex(c,d)
		else:
			x,y = args
			self.x = x
			self.y = y

	def __add__(self, o):
		return C2(self.x+o.x, self.y+o.y)

	def __sub__(self, o):
		return self + (o * -1)

	def __mul__(self, o):
		if type(o) == int or type(o) == float:		# skalarmultiplikation
			return C2(o*self.x, o*self.y)
		elif type(o) == Complex:					# Complex multiplication
			return C2(o*self.x, o*self.y)
		elif type(o) == type(self):					# C2-C2 Mult
			return C2(self.x*o.x - self.y*o.y, self.x*o.y + self.y*o.x)
		else:
			raise ValueError("Only scalar, complex or C2 multiplication possible")

	def __rmul__(self, o):	# skalarmultiplikation andere Seite
		return self * o

	def __pow__(self, e):
		if not type(e) == int:
				raise ValueError("Exponent has to be integer")
		if e < 0:
			return self.__inv()**abs(e)
		binary = [0 if b == '0' else 1 for b in bin(e)[2:]][::-1]
		start = self
		res = C2(1,0)
		for b in binary:
			if b == 1:
				res = res * start
			start = start * start
		return res

	def __truediv__(self, o):
		return self * (o**-1)

	def t(self):
		return C2(self.x,self.y*-1)

	def l(self):
		return self.x**2 + self.y**2

	def __inv(self):
		inv = self.t()
		return inv*(inv.l()**-1)

	def __eq__(self, o):
		if not type(o) == type(self):
				raise ValueError("Can only compare C2 to C2")
		return self.x == o.x and self.y == o.y

	def __str__(self):
		return f"C2[{self.x.a},{self.x.b},{self.y.a},{self.y.b}]"


if __name__ == '__main__':
	C2.N = 101

	x = C2(1,5,8,4)
	y = C2(1,0,0,0)

	print(x + y)
	print(x * y)
	print(x * 3)
	print(x ** 100)
	print(x ** -1)
	print(x ** -1 * x)
	print(x.t())

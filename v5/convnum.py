# Hier betrachtet man faltung als Körper

# Modul wird verallgemeinert, sodass es über anderen Körpern arbeitet
# Alle typechecks wurden weggenommen

from lgs import *

class ConvNum:

	def UNIT(self): 
		return ConvNum([self.l[0].UNIT()] + [x.ZERO() for x in self.l[1:]])
	def ZERO(self): 
		return ConvNum([x.ZERO() for x in self.l])

	def __init__(self, l):
		self.l = l
		self.n = len(l)

	def __add__(self, o):
		return ConvNum([x + y for x,y in zip(self.l, o.l)])

	def __sub__(self, o):
		return self + (o * -1)

	def __neg__(self):
		return ConvNum([-x for x in self.l])

	def __mul__(self, o):
		try:
			if type(o) == type(self):					# ConvNum-ConvNum
				result = [None for i in range(self.n)]
				for i in range(self.n):
					for j in range(self.n):
						if result[(i+j) % self.n] is not None:
							result[(i+j) % self.n] += self.l[i] * o.l[j]
						else:
							result[(i+j) % self.n]  = self.l[i] * o.l[j]
				return ConvNum(result)
			else: # 									# skalarmultiplikation
				return ConvNum([o * x for x in self.l])
		except TypeError:
			return NotImplemented

	def __rmul__(self, o):	# skalarmultiplikation andere Seite
		return self * o

	def __pow__(self, e):
		if not type(e) == int:
			raise ValueError("Exponent has to be integer")
		if e == 0:
			return ConvNum.UNIT(self)
		if e < 0:
			return ConvNum.UNIT(self) / (self ** abs(e))
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
		for x,y in zip(self.l, o.l):
			if x != y:
				return False
		return True

	def __truediv__(self, o):
		A = convolve_matrix(o.l)
		b = self.l
		return ConvNum(gauss_elimination(A, b))	# o * x = self  <==> x = self / o

	def __floordiv__(self, o):
		return self.__truediv__(o)

	def s(self):
		return sum(self.l)	# lgs.sum()

	def __str__(self):
		return f"V[{','.join([str(x) for x in self.l])}]"


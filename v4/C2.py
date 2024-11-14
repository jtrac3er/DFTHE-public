
# ( (a,b), (c,d) )

class C2:

	N = None

	def __init__(self,a,b,c,d):
		if C2.N:
			self.v = [a%C2.N, b%C2.N, c%C2.N, d%C2.N]
		else:
			self.v = [a,b,c,d]

	def __add__(self, o):
		return C2(*[x+y for x,y in zip(self.v, o.v)])

	def __sub__(self, o):
		return self + (o * -1)

	def __mul__(self, o):

		def mul(x,y):
			return [(x[0]*y[0] - x[1]*y[1]), (x[0]*y[1] + x[1]*y[0])]

		def add(x,y):
			return [(x[0]+y[0]), (x[1]+y[1])]

		def sub(x,y):
			return [(x[0]-y[0]), (x[1]-y[1])]

		if type(o) == int:			# skalarmultiplikation
			return C2(*[x * o for x in self.v])
		elif type(o) == type(self):
			return C2(*(
					sub( mul(self.v[0:2], o.v[0:2]), mul(self.v[2:4], o.v[2:4]) ) +
					add( mul(self.v[2:4], o.v[0:2]), mul(self.v[0:2], o.v[2:4]) )
				))
		else:
			raise ValueError("Only scalar or C2 multiplication possible")

	def __pow__(self, e):
		if not type(e) == int:
				raise ValueError("Exponent has to be integer")
		start = self
		res = C2(1,0,0,0)
		for b in [0 if b == '0' else 1 for b in bin(e)[2:]][::-1]:
			if b == 1:
				res = res * start
			start = start * start
		return res

	def t(self):
		return C2(*self.v[0:2], *[-x for x in self.v[2:4]])

	def __eq__(self, o):
		if not type(o) == type(self):
				raise ValueError("Can only compare Quaternion to Quaternion")
		return self.v == o.v

	def __str__(self):
		return f"C[{self.v[0]},{self.v[1]},{self.v[2]},{self.v[3]}]"


if __name__ == '__main__':
	C2.N = 101

	x = C2(1,5,8,4)
	y = C2(1,0,0,0)

	print(x + y)
	print(x * y)
	print(x * 3)
	print(x ** 100)
	print(x.t())



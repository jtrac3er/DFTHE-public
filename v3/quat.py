"""
Hilfsmodul für Quaternionen über einem Ring
Soll diesmal auch Operator Overrides verwenden zur Einfachheit

Definition als a + bi + cj + dk

"""

class Quaternion:

	N = None

	def __init__(self, a, b, c, d):
		self.q = [a,b,c,d]
		self._mod(Quaternion.N)

	def _mod(self, n):
		if n: self.q = [x % n for x in self.q]

	def __add__(self, o):
		if not type(o) == type(self):
			raise ValueError("Cannot add non-quaternion to Quaternion")
		return Quaternion(*[x + y for x,y in zip(self.q, o.q)])

	def __sub__(self, o):
		return self + (o * -1)

	def __mul__(self, o):
		if type(o) == int:			# skalarmultiplikation
			return Quaternion(*[x * o for x in self.q])
		elif type(o) == type(self):	# Quaternion-Quaternion
			return Quaternion(
					self.q[0]*o.q[0] - self.q[1]*o.q[1] - self.q[2]*o.q[2] - self.q[3]*o.q[3],
					self.q[0]*o.q[1] + self.q[1]*o.q[0] + self.q[2]*o.q[3] - self.q[3]*o.q[2],
					self.q[0]*o.q[2] - self.q[1]*o.q[3] + self.q[2]*o.q[0] + self.q[3]*o.q[1],
					self.q[0]*o.q[3] + self.q[1]*o.q[2] - self.q[2]*o.q[1] + self.q[3]*o.q[0]
				)
		else:
			raise ValueError("Only scalar or quaternion multiplication possible")

	def __pow__(self, e):
		if not type(e) == int:
				raise ValueError("Exponent has to be integer")
		binary = [0 if b == '0' else 1 for b in bin(e)[2:]][::-1]
		start = self
		res = Quaternion(1,0,0,0)
		for b in binary:
			if b == 1:
				res = res * start
			start = start * start
		return res

	def __eq__(self, o):
		if not type(o) == type(self):
				raise ValueError("Can only compare Quaternion to Quaternion")
		return self.q == o.q

	def __mod__(self, m):
		if not type(m) == int:
			if Quaternion.N:
				raise ValueError("Can only modulo when Quaternion.N is None")
			q = self
			q._mod(m)
			return q
		else:
			raise ValueError("Can only modulo with integer by now")
		

	def t(self):
		return Quaternion(self.q[0], *[-x for x in self.q[1:]])

	def l(self):
		s = sum([x**2 for x in self.q])
		return s % Quaternion.N if Quaternion.N else s

	def Re(self):
		return self.q[0]

	def Im(self):
		return self.q[1:]

	def __str__(self):
		return f"Q[{self.q[0]},{self.q[1]},{self.q[2]},{self.q[3]}]"


if __name__ == '__main__':

	Quaternion.N = None
	q1 = Quaternion(1,2,0,1)
	q2 = Quaternion(1,2,3,4)
	qas = QUnit
	qas *= q2

	print(q1 - q2)
	print(q2 * 3)
	print(q1 * q2)
	print(q2 ** 3)
	print(qas)
	print(q2.t())
	print(q1.l())
	print(QUnit == QZero)
	print(QUnit != QZero)



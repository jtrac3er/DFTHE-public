from complex import *

def sum(l):
	res = CZero
	for i in range(0, len(l)):
		res += l[i]
	return res


def gauss_elimination(A, b):
	"""
	Löst ein lineares Gleichungssystem A * x = b mittels Gauss-Elimination.
	
	:param A: Koeffizientenmatrix (List of Lists)
	:param b: Rechter Seitenvektor (List)
	:return: Lösung des Gleichungssystems (List)
	"""
	n = len(b)
	
	# Erstelle eine erweiterte Matrix (A|b)
	Ab = [row + [b[i]] for i, row in enumerate(A)]
	
	# Durchführung der Gauss-Elimination
	for i in range(n):
		# Suche die Pivot-Zeile
		
		#max_row = i + max(range(n - i), key=lambda k: abs(Ab[i + k][i]))
		max_row = i	 # scheiss egal, ist eh diskret
		
		# Zeile tauschen
		Ab[i], Ab[max_row] = Ab[max_row], Ab[i]
		
		# Normiere die Pivot-Zeile
		pivot = Ab[i][i]
		Ab[i] = [x / pivot for x in Ab[i]]
		
		# Eliminiere die anderen Zeilen
		for j in range(n):
			if i != j:
				factor = Ab[j][i]
				Ab[j] = [Ab[j][k] - factor * Ab[i][k] for k in range(n + 1)]
	
	# Rückwärtssubstitution
	x = [0] * n
	for i in range(n - 1, -1, -1):
		x[i] = Ab[i][-1] - sum([Ab[i][j] * x[j] for j in range(i + 1, n)])
	
	return x


def matrix_mul(A,x):
	result = [CZero for i in range(len(A))]
	for i in range(len(A)):
		for j in range(len(x)):
			result[i] += A[i][j] * x[j]
	return result


def convolve_matrix(x):
	res = []
	for i in range(len(x)):
		res.append( [x[(i-j) % len(x)] for j in range(len(x))] )
	return res


def pp_vec(v):
	for q in v: print(q)

def pp_mat(m):
	for r in m:
		print("[", end="")
		for e in r:
			print(e, end=", ")
		print("]")


if __name__ == '__main__':

	# tests, ob man diesen Datentyp auch für Numpy verwenden kann
	from lgs import *
	Complex.N = 11

	A = [[Complex(2,0), Complex(2,0)], [Complex(2,1), Complex(3,0)]]
	b = [Complex(3,3), Complex(7,0)]

	x = gauss_elimination(A,b)
	pp_vec(x)


	B = matrix_mul(A,x)
	print()
	pp_vec(B)

	pp_mat(convolve_matrix([1,2,3]))




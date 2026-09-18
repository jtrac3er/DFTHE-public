import numpy as np

def lgs_solve(A,b):
	A = np.array(A, dtype=float)
	b = np.array(b, dtype=float)
	return np.linalg.solve(A, b).tolist()

def matrix_mul(A,x):
	result = [None for i in range(len(A))]
	for i in range(len(A)):
		for j in range(len(x)):
			if result[i] is not None: result[i] += A[i][j] * x[j]
			else: result[i] = A[i][j] * x[j]
	return result


def convolve_matrix(x):
	res = []
	for i in range(len(x)):
		res.append( [x[(i-j) % len(x)] for j in range(len(x))] )
	return res

def transpose_matrix(M):
	n = len(M)
	res = [[None for i in range(n)] for i in range(n)]
	for i in range(n):
		for j in range(n):
			res[i][j] = M[j][i]
	return res

def pp_vec(v):
	print("[", end="")
	for q in v: print(q, end=",")
	print("]")


def pp_mat(m):
	for r in m:
		print("[", end="")
		for e in r:
			print(e, end=", ")
		print("]")


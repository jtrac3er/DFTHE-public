"""
Ich muss die Parameter besser analysieren um wirklich herauszufinden, für welche Werte die Methode
konvergiert und wie schnell sie konvergiert. Weil im Moment tut sie das nicht immer, und das ist 
auch ein Problem

Und ich will folgende Parameter verwenden: 
	- Komponenten von CV sollen komplett kontrolliert werden, nur n CVs
	- Es soll numerisch stabil sein, also arbitrary precision integers verwenden und nicht floats
	- 

"""

import numpy as np
from random import randint
from lgs import *

def oracle_norm(x, c, V):
	r = c - V @ x
	return np.dot(r, r)


def round_to_int(v):
	return np.array([int(x) for x in v])


def gradient_descent(
			oracle, n, 
			alpha,
			alpha_increase,
			alpha_decrease,
			max_iter,
		):
	
	x = np.zeros(n, dtype=object)

	for iteration in range(max_iter):

		gradient = np.zeros(n, dtype=object)

		for i in range(n):
			x_plus = x.copy()
			x_minus = x.copy()
			x_plus[i] += 1
			x_minus[i] -= 1
			grad_estimate = (oracle(x_plus) - oracle(x_minus)) / 2
			gradient[i] = grad_estimate

		x_new = round_to_int(x - gradient // alpha)

		if oracle(x_new) < oracle(x):
			x = x_new
			alpha //= alpha_increase
		else:
			alpha *= alpha_decrease
		
		if oracle(x) < threshold: 
			break


def round_approximation(V, c):
	
		

def testcases():

	max_exponent = 100
	min_exponent = 10

	n = 3	# vektor grösse
	m = 3	# anzahl correctional vectors

	while True:
		c = randint(0, 10**randint(min_exponent, max_exponent // 2))
		V = np.array([
				[randint(0, 10**randint(min_exponent, max_exponent // 2)) for i in range(n)]
					for j in range(m)
			])

		gradient_descent

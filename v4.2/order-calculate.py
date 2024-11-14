"""
Kurzer Test, um den Order zu bestimmen
"""

from complex import *
from primes import *

def generatePrimes(low, high):
	for i in range(low, high):
		for num in range(2, i):
			if i % num == 0:
				break
		else:
			yield i

def find_order(a, p):
	for i in range(1, p**2):
		if a**i == CUnit:
			return i
	return -1

def decide_z2(p):
	if STonelli(-(((p+1)//2)**2), p) != -1:
		return True
	return False


for p in generatePrimes(10, 100):

	orders = {}
	Complex.N = p

	for x in range(p):
		for y in range(p):
			 
			 c = Complex(x,y)
			 o = find_order(c, p)
			 if not o in orders:
			 	orders[o] = 1
			 else:
			 	orders[o] += 1

	print(p, decide_z2(p), orders)


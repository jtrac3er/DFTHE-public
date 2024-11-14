"""
Hier soll ein bisschen das Verhalten von Quaternionen erforscht werden bei
verschiedenen Primzahlen
"""

from quat import * 
from quathelper import *
import itertools

def generatePrimes(low, high):
	for i in range(low, high):
		for num in range(2, i):
			if i % num == 0:
				break
		else:
			yield i

def quat_gen(N):
	for liste in itertools.product(range(N+1), repeat=4):
		yield Quaternion(*list(liste))


def order(q, N):
	for i in range(1,N**2):
		if q**i == QUnit:
			return i
	return -1

for N in generatePrimes(2,100):
	Quaternion.N = N
	print(f"Primzahl ist {N}")
	for q in quat_gen(N):
		o = order(q, N)
		print(o)


from quat import *
from random import randint
from itertools import product
from primes import mod_inverse


QUnit = Quaternion(1,0,0,0)
QZero = Quaternion(0,0,0,0)


def quat_gen(N, nonzero=False):
	for liste in product(range(N), repeat=4):
		res = Quaternion(*list(liste))
		if nonzero and res == QZero: continue
		yield res

def quat_gen_random(N, k):
	for i in range(k):
		yield Quaternion(*[randint(0,N) for j in range(4)])

def quat_inv(q, phi=None):
	if q.l() == 0: return None
	if not phi: return q.t() * mod_inverse(q.l(), Quaternion.N)
	else: return q.t() * pow(q.l(), phi-1, Quaternion.N)



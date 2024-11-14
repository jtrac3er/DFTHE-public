from quat import * 
from quathelper import *
from random import randint
from primes import *
from keygen import keygen


def qft(qu, v, s=1):
	n = len(v)
	assert(qu**n == QUnit)
	res = [QZero for i in range(n)]
	for i in range(n):
		for j in range(n):
			res[i] += (qu**(i*j)) * v[j]
		res[i] *= s
	return res

def enc(k, ml):
	e = [k.q0*x + k.q1*y for x,y in ml]
	return qft(k.qu, e, pow(k.n, k.p-2, k.p))

def dec(k, cl):
	e = qft(k.qu.t(), cl, 1)
	inv = pow((k.p+1) // 2, k.p-2, k.p)
	return [((qe*k.q0).Re()*inv % k.p , (qe*k.q1).Re()*inv % k.p) for qe in e]


def hom_mul(c1, c2):
	n = len(c1)
	result = [QZero for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[(i+j) % n] += c1[i] * c2[j]
	return result


def hom_add(c1, c2):
	return [x + y for x,y in zip(c1,c2)]


def pp_vec(v):
	for q in v: print(q)


if __name__ == '__main__':

	n = 3
	k = keygen(n, 61235746925250212479)
	Quaternion.N = k.p

	m1 = [(randint(0,10), randint(0,10)) for i in range(n)]
	m2 = [(randint(0,10), randint(0,10)) for i in range(n)]

	print("m1")
	pp_vec(m1)
	print("\nm2")
	pp_vec(m2)
	

	c1 = enc(k, m1)
	c2 = enc(k, m2)

	print("\nadd")
	pp_vec(dec(k, hom_add(c1, c2)))
	print("\nmul")
	pp_vec(dec(k, hom_mul(c1, c2)))






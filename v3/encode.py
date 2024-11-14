"""

"""

from quat import * 
from quathelper import *
from random import randint
import itertools
from primes import *

# Q[16,0,2,9] Q[16,23,18,21] Q[1,23,20,30]

p = 31
Quaternion.N = p
q1 = Quaternion(16,0,2,9)
q2 = Quaternion(16,23,18,21)
qn = q1 + q2

def enc(m1, m2):
	return q1*m1 + q2*m2

def dec(c):
	e1 = c * q1
	e2 = c * q2
	p2_inv = pow((p+1) // 2, p-2, p)
	return (e1.Re() * p2_inv) % p, (e2.Re() * p2_inv) % p


t = enc(5,5)
print(t)
print(dec(t))

print(dec(t**2), t**2)
print(dec(t*2), t*2)

print("\n\n")

t1 = enc(3,3)
t2 = enc(4,4)
print(dec(t1 + t2), t1 + t2)
print(dec(t1 * t2), t1 * t2)
print(dec(t2 * t1), t2 * t1, (t2 * t1).l())

# Q[16,0,4,10] Q[16,28,25,28] Q[1,28,29,7]
print("\n\n")

q1 = Quaternion(16,0,4,10)
q2 = Quaternion(16,28,25,28)
print(dec(t1))
print(dec(t2))
print(dec(t1 + t2), t1 + t2)
print(dec(t1 * t2), t1 * t2)
print(dec(t2 * t1), t2 * t1, (t2 * t1).l())
from keygen import *
from primes import *
from dft import *

from random import randint, uniform
from lgs import *

from convnum import *
from modnum import *
from complex import *


"""
Zuerst geht es darum, ob man überhaup reelle werte verwenden kann für dft: Nein, kann man nicht!

k = keygen(3, 1e10, 9e10)

def norm(c): return sum([e.l() for e in c.l])

def random_encrypt(k):
	e = [Complex(ModNum(randint(0, int(k.N**0.5 // 100)), k.N), ModNum(0, k.N)) for i in range(k.n)]
	return ConvNum(e), ConvNum(fourier_transform(k.U, k.n, mod_inverse(k.n, k.N), e))

def decrypt(k, c):
	return ConvNum(fourier_transform(k.U.t(), k.n, 1, c.l))


m,c = random_encrypt(k)

print(k.N)
print(m, norm(m))
print(decrypt(k, c), norm(c)*k.n)

"""

M = 100
m = 3

t_max = 1_000

c = m + 10*M 
c_res = 1

for i in range(4):
	c_res = c_res*c
	if abs(c_res) > t_max:
		c_res -= (c_res // M + 1) * M 
		print(c_res)

while c_res < 0:
	c_res += M 

print(c_res % M)
"""
Ich will nur kurz testen, ob es möglich ist, dass wenn m=0 dass dann |c|=0 sein muss
"""

from C2 import *
from primes import *
from random import *

while True:
	p = randint(0,1000)
	a = (p+1)//2
	if rabinMiller(p) and (b := STonelli(-(a**2), p)) != -1:
		break

C2.N = p
print(f"p={p}")

base = [0 for i in range(4)]
base[0] = C2(a*a,  a*b,  a*b,  b*b)
base[1] = C2(a*a, -a*b,  a*b, -b*b)
base[2] = C2(a*a,  a*b, -a*b, -b*b)
base[3] = C2(a*a, -a*b, -a*b,  b*b)

m = 1

c = m*base[0] + m*base[1] + randint(0,p)*base[2] + randint(0,p)*base[3]

print(c)
print(c.l())

"""
stimmt audh alles, kein Problem

for i in range(4):
	for j in range(4):

		print()
		print(i,j)
		print(base[i]*base[j])
"""

"""
Und ja es stimmt, es ergibt wirklich immer (0,0)
"""
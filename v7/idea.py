from complex import *
from modnum import *
from primes import *
from random import randint

while True:
	p = randint(1,1e4)
	if (u := STonelli(-(((p+1)//2)**2), p)) != -1:
		break

z1 = Complex(ModNum((p+1)//2, p), ModNum(u,p))
z2 = Complex(ModNum((p+1)//2, p), ModNum(-u,p))
assert z1.l() == 0
assert z2.l() == 0


a = 10
b = 10
x = a*z1 + b*z2
print(x.l(), x.Re()*2)

a = -10
b = 10
x = a*z1 + b*z2
print(x.l(), x.Re()*2)

a = 10
b = -10
x = a*z1 + b*z2
print(x.l(), x.Re()*2)

a = -10
b = -10
x = a*z1 + b*z2
print(x.l(), x.Re()*2)

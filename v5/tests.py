from crypt2 import *

from complex import *
from convnum import *
from modnum import *

from lgs import *

n = 3
m = 0
key = init_key(keygen(n, min_rand=1e3, max_rand=9e3))

ifft = lambda v : fourier_transform(key.u**-1, key.n, 1, v)
ffft = lambda v : fourier_transform(key.u, key.n, mod_inverse(key.n, key.N), v)

e = Complex(ConvNum([1 for i in range(n)]), ConvNum([1 for i in range(n)]))
c = encrypt(key, m)
c2 = c + e

ratio = c2.Re() / c2.Im()
re = ratio.l[0] * ConvNum([1 for i in range(n)])
ratio2 = ratio - re

print(ratio2)
pp_vec(ifft(ratio2.l))
print((key.a / key.b)**2 + 1)
print_key(key)
print(-ratio2.l[1]*((key.N+1)//2), ratio2.l[1]**2)

exit()
print("\n")

# ich glaube es ist dasselbe wie zuerst komplex dann transform
def complex_to_convnum(c):
	return ConvNum([Complex(a,b) for a,b in zip(c.Re().l, c.Im().l)])

nzero = ModNum(0, key.N)

ifft = lambda v : fourier_transform(Complex(key.u**-1, nzero), key.n, 1, v)
ffft = lambda v : fourier_transform(Complex(key.u, nzero), key.n, mod_inverse(key.n, key.N), v)

c = encrypt(key, m)
c2 = complex_to_convnum(c) + ConvNum([Complex(1,0) for i in range(3)])

print(c)
print(c2)

e = ifft(c2.l)

b0 = Complex(key.a, key.b)
b1 = Complex(key.a, -key.b)
z1 = e[1]
z2 = e[2]

# x*a = z  <==>  x = z / a
m1 = (z1*b0).Re() / key.a
r1 = (z1*b1).Re() / key.a
r2 = (z2*b0).Re() / key.a
m2 = (z2*b1).Re() / key.a

print(m1,m2,r1,r2)
print("\n")

# ist es auch. Aber ist es auch wirklich unsicher in dieser Konstellation?
mm = Complex(ModNum(m, key.N),nzero)

A = [(c2**i).l for i in range(1,4)]
b = [mm**i for i in range(1,4)]
x = gauss_elimination(A, b)

pp_vec(x)
print((x[1] * b1).Re() / key.a)
print((x[2] * b1).Re() / key.a)
print((x[1] * b0).Re() / key.a)
print((x[2] * b0).Re() / key.a)

u1 = x[1]
u2 = x[2]
print(u1 / u2, u1**2, u1*u2, sum(x))
s = x[1].Im() - x[2].Im()

print(s**2)
print_key(key)

# und wenn man dann eine andere Zahl noch decoded? 
c2 = complex_to_convnum(encrypt(key, 13))
dec = sum([x*y for x,y in zip(c2.l, x)])
print(dec)
print("\n")

# Ja absolut UNSICHER, man kann mit diesem x Vektor dann alle anderen
# Zahlen auch decoden. Macht auch Sinn, und zwar weil man quasi dann
# Einen shift und inverse dft gleichzeitig macht

# x = links_shift  [pw-mul]  decode

# Und somit shiftet man zuerst m auf m, sodass (m,0) ensteht, welches
# man dann decoded und dann sofort den richtigen wert m kriegt. Also man
# leakt zwar weder b noch u, aber man kann trotzdem alles decoden


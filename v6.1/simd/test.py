from primes import *

p = 101

x = 44
y = 33

c1 = (x, x**2)
c2 = (y, y**2)

c_add = ((c1[0]+c2[0]) % p, (c1[1]+c2[1] + 2*c1[0]*c2[0]) % p)
c_mul = ((c1[0]*c2[0]) % p, (c1[1]*c2[1]) % p)

print(c_add, (c_add[1]*mod_inverse(c_add[0], p)) % p, (x+y) % p, STonelli(c_add[1], p))
print(c_mul, (c_mul[1]*mod_inverse(c_mul[0], p)) % p, (x*y) % p, STonelli(c_mul[1], p))


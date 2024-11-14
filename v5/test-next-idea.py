from dft import *
from keygen import *
from modnum import *
from crypt import *
from lgs import *

m = 3
n = 5

key = init_key(keygen(m*n, min_rand=1e2, max_rand=9e2))

ifft = lambda v : fourier_transform(key.u**-1, key.n, 1, v)
ffft = lambda v : fourier_transform(key.u, key.n, mod_inverse(key.n, key.N), v)

x = [i+1 for i in range(m*n)]

v = ffft(x)
vn = [None for i in range(m*n)]

for i in range(m*n):
	if vn[i % m] is not None: vn[]

pp_vec(x)
pp_vec(vn)


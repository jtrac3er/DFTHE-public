"""
Ein einfacher helper für das andere library
"""
 
from crypt2 import *
from timeit import default_timer as timer

TRUE = 1
FALSE = 0

def AND(x,y): return normalize(x*y)

def OR(x,y): return normalize(x+y - x*y)

def NOT(x): return normalize((x-ConvNum([1,0,0]))**2)

def encrypt_bitvector(v): return [encrypt(e) for e in v]

def decrypt_bitvector(c): return [decrypt(e) for e in c]

if __name__ == '__main__':
	a = encrypt(FALSE)
	b = encrypt(TRUE)
	print(decrypt(AND(a,b)))
	print(decrypt(OR(a,b)))
	print(decrypt(NOT(a)))
	print(a,b)

	start = timer()
	res = AND(a,b)
	end = timer()

	print(f"time for single logic gate: {end - start}s")

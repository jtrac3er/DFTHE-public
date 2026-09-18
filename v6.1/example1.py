from crypt import *
from convnum import *
from timeit import default_timer as timer

TRUE = 1
FALSE = 0

c_one = ConvNum([1,0,0])


def AND(x,y): return mul(x,y)

def OR(x,y): return add(add(x,y), smul(-1, mul(x,y)))

def NOT(x): return pot(add(x, smul(-1, c_one)), 2)

def encrypt_bitvector(v): return [encrypt_ex(e) for e in v]

def decrypt_bitvector(c): return [decrypt_ex(e) for e in c]


def half_adder(x, y):
	S = OR(AND(x, NOT(y)), AND(NOT(x), y))
	Carry = AND(x, y)
	return S, Carry

def full_adder(x, y, Carry_in):
	S1, Carry1 = half_adder(x, y)
	S, Carry2 = half_adder(S1, Carry_in)
	Carry_out = OR(Carry1, Carry2)
	return S, Carry_out

def add_8bit(a, b):
	result = [None] * 8  
	Carry = FALSE_encrypted
	result[0], Carry = full_adder(a[0], b[0], Carry)
	for i in range(1, 8):
		result[i], Carry = full_adder(a[i], b[i], Carry)

	return result, Carry 


if __name__ == '__main__':

	SK,HK,PK,_ = keygen(3, 96)

	mul = lambda x,y : hom_mul(HK,x,y)
	add = lambda x,y : hom_add(HK,x,y)
	pot = lambda x,e : hom_pot(HK,x,e)
	smul = lambda s,c : hom_mul(HK,s,c)

	encrypt_ex = lambda v: encrypt(SK, v)
	decrypt_ex = lambda v: decrypt(SK, v)

	FALSE_encrypted = encrypt_ex(FALSE)
	TRUE_encrypted = encrypt_ex(TRUE)

	x = encrypt_bitvector([1,1,0,0,0,0,1,0])
	y = encrypt_bitvector([1,0,0,0,1,1,1,1])

	start = timer()
	res = add_8bit(x, y)[0]
	end = timer()

	print("TRA scheme has run with SK:")
	print_key(SK)
	print("\nAnd with correctional vectors:")
	print_cv(HK.CVL)
	print(f"\nresult of addition: {decrypt_bitvector(res)}")
	print(f"sample ciphertext: {res[0]}")
	print(f"elapsed time: {end - start}s")
	
	





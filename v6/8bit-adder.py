from helper import *
from crypt2 import *
from timeit import default_timer as timer

def half_adder(x, y):
	S = OR(AND(x, NOT(y)), AND(NOT(x), y))  # XOR-Funktion
	Carry = AND(x, y)
	return S, Carry

def full_adder(x, y, Carry_in):
	S1, Carry1 = half_adder(x, y)
	S, Carry2 = half_adder(S1, Carry_in)
	Carry_out = OR(Carry1, Carry2)
	return S, Carry_out

def add_8bit(a, b):
	# a und b sind Listen von 8 Bits [a7, a6, ..., a0] und [b7, b6, ..., b0]
	result = [None] * 8  	# Ergebnis der 8-Bit-Addition
	Carry = encrypt(FALSE)  # Anfangsübertrag ist 0

	# Addition des niederwertigsten Bits (Bit 0)
	result[0], Carry = full_adder(a[0], b[0], Carry)

	# Addition der restlichen Bits (Bit 1 bis Bit 7)
	for i in range(1, 8):
		result[i], Carry = full_adder(a[i], b[i], Carry)

	return result, Carry  # Carry enthält den letzten Übertrag


if __name__ == '__main__':
	x = encrypt_bitvector([1,0,0,0,0,0,1,1])
	y = encrypt_bitvector([1,0,0,0,1,1,1,1])

	start = timer()
	res = add_8bit(x, y)[0]
	end = timer()

	print(decrypt_bitvector(res))
	print(res[0])
	print(f"elapsed time: {end - start}s")
	print




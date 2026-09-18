from crypt import *
from convnum import *
from timeit import default_timer as timer

if __name__ == '__main__':

	SK,HK,PK,EK = keygen(3, 64)

	mul = lambda x,y : hom_mul(HK,x,y)
	add = lambda x,y : hom_add(HK,x,y)
	pot = lambda x,e : hom_pot(HK,x,e)
	smul = lambda s,c : hom_mul(HK,s,c)
	evaluate = lambda c: hom_eval(EK, c)

	encrypt_ex = lambda v: encrypt(SK, v)
	decrypt_ex = lambda v: decrypt(SK, v)

	m1 = encrypt_ex(2)
	m2 = encrypt_ex(2)
	res = encrypt_ex(0)
	NO_OPS = 10

	start = timer()
	for i in range(NO_OPS):
		#print(evaluate(res))
		res = add(res, m2)
		res = mul(res, m1)
	end = timer()

	print("TRA scheme has been run with SK:")
	print_key(SK)
	print("\nAnd with correctional vectors:")
	print_cv(HK.CVL)
	#print("\nAnd with evaluation List:")
	#print(EK.gl)
	print(f"\nresult for {2*NO_OPS} operations: {decrypt_ex(res)}")
	print(f"result ciphertext: {res}")
	print(f"elapsed time: {end - start}s")

	
# Allgemeine Variante für FFT
# u = n-te unity root
# n = Grad, vektorlänge
# s = scale
# v = vektor

def fourier_transform(u,n,s,v):
	res = [None for i in range(n)]
	for i in range(n):
		for j in range(n):
			if res[i] is not None:
				res[i] += (u**(i*j)) * v[j]
			else:
				res[i]  = (u**(i*j)) * v[j]
		res[i] *= s
	return res




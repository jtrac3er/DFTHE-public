"""
Modul für imaginäre Zahlen
"""

def mul(x,y,p):
	return ((x[0]*y[0] - x[1]*y[1]) % p, (x[0]*y[1] + x[1]*y[0]) % p)

def add(x,y,p):
	return ((x[0]+y[0]) % p, (x[1]+y[1]) % p)

def t(x,p):
	return (x[0], (-x[1]) % p)

def l(x,p):
	return (x[0]**2 + x[1]**2) % p

def smul(s,x,p):
	return mul((s,0), x, p)

def Im(x):
	return x[1]

def Re(x):
	return x[0]

def old_pot(x,n,p):
	res = (1,0)
	for i in range(n):
		res = mul(res, x, p)
	return res

# sqam pot
def pot(x,n,p):
	binary = [0 if b == '0' else 1 for b in bin(n)[2:]][::-1]
	start = x
	res = (1,0)

	for b in binary:
		if b == 1:
			res = mul(res, start, p)
		start = mul(start, start, p)

	return res


if __name__ == '__main__':
	# test, ob sqam pot auch stimmt
	p = 23
	for i in range(p):
		for j in range(p):
			rand = (i,j)
			for n in range(p):
				assert(pot(rand, n, p) == old_pot(rand, n, p))

	# Es stimmt, diese Version funktioniert

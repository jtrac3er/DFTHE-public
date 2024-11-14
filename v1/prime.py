"""
Modul für Primzahlen 
"""

import random
from math import gcd

# Chatgpt code
def rabinMiller(n, k=40):
	"""
	Testet, ob eine Zahl n eine Primzahl ist, mit der Rabin-Miller-Methode.
	
	:param n: Die zu testende Zahl.
	:param k: Die Anzahl der Testdurchläufe (Standard: 5).
	:return: True, wenn n wahrscheinlich eine Primzahl ist, False, wenn n zusammengesetzt ist.
	"""
	if n <= 1:
		return False
	if n <= 3:
		return True
	if n % 2 == 0:
		return False

	# Schreibe n-1 als 2^r * d mit d ungerade
	r, d = 0, n - 1
	while d % 2 == 0:
		r += 1
		d //= 2
	
	def is_composite(a):
		"""Helferfunktion, die prüft, ob a ein Zeuge dafür ist, dass n zusammengesetzt ist."""
		x = pow(a, d, n)
		if x == 1 or x == n - 1:
			return False
		for _ in range(r - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				return False
		return True
	
	# Führe den Test k Mal durch
	for _ in range(k):
		a = random.randrange(2, n - 1)
		if is_composite(a):
			return False
	
	return True




# Chatgpt code
def mod_inverse(x, N):
	""" Berechne das multiplikative Inverse von x modulo N """

	def extended_gcd(a, b):
		""" Erweiterten euklidischen Algorithmus implementieren """
		if a == 0:
			return b, 0, 1
		gcd, x1, y1 = extended_gcd(b % a, a)
		x = y1 - (b // a) * x1
		y = x1
		return gcd, x, y

	gcd, inv, _ = extended_gcd(x, N)
	if gcd != 1:
		raise ValueError(f"Das multiplikative Inverse existiert nicht, weil gcd({x}, {N}) = {gcd} ist, nicht 1.")
	else:
		# Da inv auch negativ sein kann, nehmen wir inv % N, um es positiv zu machen
		return inv % N




# Main function for finding the
# modular square root 
def STonelli(n, p): 

	# Returns k such that b^k = 1 (mod p) 
	def order(p, b): 
		if (gcd(p, b) != 1):
			#print("p and b are not co-prime.\n"); 
			return -1; 
		k = 3; 
		while (True): 
			if (pow(b, k, p) == 1): 
				return k; 
			k += 1; 

	def convertx2e(x):
		z = 0; 
		while (x % 2 == 0):
			x = x // 2; 
			z += 1; 
		return [x, z]; 

	if (gcd(n, p) != 1): #print("a and p are not coprime\n"); 
		return -1; 

	if (pow(n, (p - 1) // 2, p) == (p - 1)): #print("no sqrt possible\n"); 
		return -1; 

	# expressing p - 1, in terms of s * 2^e, 
	# where s is odd number 
	ar = convertx2e(p - 1);
	s = ar[0];
	e = ar[1];

	# finding smallest q such that 
	# q ^ ((p - 1) / 2) (mod p) = p - 1 
	q = 2; 
	while (True):
		if (pow(q, (p - 1) // 2, p) == (p - 1)): 
			break;
		q += 1;

	x = pow(n, (s + 1) // 2, p); 
	b = pow(n, s, p); 
	g = pow(q, s, p); 
	r = e; 

	while (True):
		m = 0; 
		while (m < r):
			if (order(p, b) == -1): 
				return -1; 
			if (order(p, b) == pow(2, m)): 
				break;
			m += 1;

		if (m == 0): 
			return x; 

		x = (x * pow(g, pow(2, r - m - 1), p)) % p; 
		g = pow(g, pow(2, r - m), p); 
		b = (b * g) % p; 

		if (b == 1): 
			return x; 
		r = m; 


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



# Python3 program to implement Shanks Tonelli
# algorithm for finding Modular Square Roots 

# utility function to find pow(base, 
# exponent) % modulus 
def pow1(base, exponent, modulus): 

	result = 1; 
	base = base % modulus; 
	while (exponent > 0): 
		if (exponent % 2 == 1):
			result = (result * base) % modulus; 
		exponent = int(exponent) >> 1; 
		base = (base * base) % modulus; 

	return result; 



def tonelli(n, p):

	def legendre(a, p):
		return pow(a, (p - 1) // 2, p)

	if legendre(n, p) != 1:
		return -1
		
	q = p - 1
	s = 0
	while q % 2 == 0:
		q //= 2
		s += 1
	if s == 1:
		return pow(n, (p + 1) // 4, p)
	for z in range(2, p):
		if p - 1 == legendre(z, p):
			break
	c = pow(z, q, p)
	r = pow(n, (q + 1) // 2, p)
	t = pow(n, q, p)
	m = s
	t2 = 0
	while (t - 1) % p != 0:
		t2 = (t * t) % p
		for i in range(1, m):
			if (t2 - 1) % p == 0:
				break
			t2 = (t2 * t2) % p
		b = pow(c, 1 << (m - i - 1), p)
		r = (r * b) % p
		c = (b * b) % p
		t = (t * c) % p
		m = i
	return r
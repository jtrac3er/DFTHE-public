def mod_inverse(a, n):
	"""Berechnet das modulare Inverse von a modulo n mithilfe des erweiterten euklidischen Algorithmus."""
	t, new_t = 0, 1
	r, new_r = n, a
	while new_r != 0:
		quotient = r // new_r
		t, new_t = new_t, t - quotient * new_t
		r, new_r = new_r, r - quotient * new_r
	if r > 1:
		raise ValueError("Kein inverses Element vorhanden.")
	if t < 0:
		t = t + n
	return t

def montgomery_reduction(a, b, N):
	"""Führt die Montgomery-Multiplikation von a und b modulo N aus."""
	
	# Bestimme R als die nächstgrößere Potenz von 2 größer als N
	R = 1
	while R <= N:
		R <<= 1

	# Berechne N' = -N^(-1) mod R
	N_inv = mod_inverse(N, R)
	N_prime = R - N_inv  # N' = -N^(-1) mod R

	# Konvertiere a und b in die Montgomery-Darstellung
	a_R = (a * R) % N
	b_R = (b * R) % N

	# Schritt 1: Berechne t = a_R * b_R
	t = a_R * b_R

	# Schritt 2: Berechne m = (t * N') % R
	m = (t * N_prime) % R

	# Schritt 3: Berechne u = (t + m * N) / R
	u = (t + m * N) // R

	# Schritt 4: Falls u >= N, setze u = u - N
	if u >= N:
		u = u - N

	# Rückumwandlung in die normale Darstellung
	u = (u * mod_inverse(R, N)) % N
	
	return u

# Beispiel
a = 23
b = 27
N = 105

# Berechne (a * b) mod N unter Verwendung der Montgomery-Multiplikation
result = montgomery_reduction(a, b, N)
print(f"Das Ergebnis der Montgomery-Multiplikation von {a} und {b} modulo {N} ist: {result}")
print(f"Das Ergebnis der Modularen-Multiplikation von {a} und {b} modulo {N} ist: {a*b % N}")

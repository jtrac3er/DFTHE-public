"""
Die Analyse soll einige Ciphertext Paare analysieren und deren gleichverteilung beweisen

"""
from crypt import *

SK,HK,PK = keygen(3, 64, N=36576485279740230949)

mul = lambda x,y : hom_mul(HK,x,y)
add = lambda x,y : hom_add(HK,x,y)
pot = lambda x,e : hom_pot(HK,x,e)
smul = lambda s,c : hom_mul(HK,s,c)

encrypt_ex = lambda v: encrypt(SK, v)
decrypt_ex = lambda v: decrypt(SK, v)

import numpy as np
from scipy.stats import chisquare

def check_uniform_distribution(L, N, bin_size=1000):
	"""
	Überprüft, ob Vektoren in Liste L gleichverteilt in {0, ..., N}^3 sind.

	Parameter:
	L (list): Liste von Vektoren (jeder Vektor ist eine Liste oder ein Array von drei Werten).
	N (int): Maximale Größe des Gitterraums (z.B. 2^64).
	bin_size (int): Die Anzahl der Intervalle, in die jede Dimension unterteilt wird.

	Rückgabe:
	tuple: (Chi2-Statistik, p-Wert)
	"""

	# Konvertiere die Liste der Vektoren in ein numpy-Array
	L = np.array(L)
	
	# Berechne die Anzahl der Vektoren
	num_vectors = len(L)
	
	# Bestimme die Bins für jede Dimension, indem du die Vektoren auf [0, bin_size)^3 skalierst
	bins = np.linspace(0, N, bin_size + 1)

	# Erstelle ein 3D-Histogramm, um die Anzahl der Vektoren in jeder Zelle des Gitters zu zählen
	counts, edges = np.histogramdd(L, bins=[bins, bins, bins])

	# Flach das Histogramm in einen 1D-Vektor von Zellhäufigkeiten um
	observed_counts = counts.flatten()

	# Berechne die erwarteten Häufigkeiten unter der Annahme einer Gleichverteilung
	expected_counts = np.full(observed_counts.shape, num_vectors / len(observed_counts))

	# Führe den Chi-Quadrat-Test durch
	chi2_stat, p_value = chisquare(observed_counts, expected_counts)

	return chi2_stat, p_value

num_vectors = 100
L = []

r = encrypt_ex(0)
for i in range(num_vectors):
	r = mul(r,r)
	L.append(r.l)

# Überprüfe die Gleichverteilung
chi2_stat, p_value = check_uniform_distribution(np.array(L), SK.N)

print(f"Chi2-Statistik: {chi2_stat}, p-Wert: {p_value}")

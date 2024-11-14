"""
Finde Quaternionenpaare, die erfüllen, dass q1**2 == q1

Und was habe ich herausgefunden? Es sieht so aus, als ob Quaternionen wirklch ähnlich sind wie
Komplexe Zahlen, auf jeden Fall, vielleicht gibt es noch Annomalien, aber was sicher ist

 - für jede Primzahl p gibt es sehr viele Quaternionenpaare q/q' welche die Gleichungen erfüllen:
 	q + q' = QUnit
 	q * q' = QZero 

Das könnte doch schon zur verschlüsselung genutzt werden? Nein ist dasselbe Problem wie bei komplexen
Zahlen. Man kann diesmal zwar auswählen, welche q/q' man nimmt, aber wenn eines der beiden =0 ist, dann
kann man trotdem das andere rausfinden, denn etwas was immer gleich bleibt ist, dass der Realteil (also q[0])
auch hier immer p+1/2 ist. So kann man schnell den richtigen Wert herausfinden. Da auch hier division einfach
ist, hilft auch eine DFT nichts

Alles, was helfen könnte ist, dass es noch annomalien gibt wie bei den Komplexen zahlen, also dass man 4 Zahlen
anstatt 2 Zahlen encoden kann. In diesem Falle erhält man vielleicht etwas krasses, und zwar dass man 4 a Elemente
hat, a1 bis a4 welche folgendes erfüllen:
    
    a1 + a2 + a3 + a4 = QUnit
    an ^ 2 = an
    ai * aj = 0 	(wenn i != j)

das wären die Eigenschaften die ich brauche. Und das könnte es eigentlich schon geben, aber vlt auch nicht, denn 
Quaternionen sind ja nicht mal kommutativ, aber naja, keine Ahnung wie das alles zusammenhängt. Vielleicht gibt es 
auch nur 3 a Elemente, aber das wäre auch schon gut

Wieso bringt das was, wenn es mehr als 2 a Elemente sind?

 - Weil dann, wenn man einen Wert kennt, kennt man 2/3 Werte nicht und dann hat man zuviele Variablen um alles zu
   decoden. 

Wievlee Nullelemente gibt es pro Primzahl?
#no = p^2 + p = p(p+1)

"""

from quat import * 
from quathelper import *
from random import randint
import itertools
from primes import *


def generatePrimes(low, high):
	for i in range(low, high):
		for num in range(2, i):
			if i % num == 0:
				break
		else:
			yield i


"""
for N in generatePrimes(2,100):
	Quaternion.N = N
	ctr = 0
	for q in quat_gen(N):
		if q**2 == q:
			ctr += 1
	print(f"Für Primzahl p={N} gibt es {ctr} a2-Elemente")
"""

"""
for N in generatePrimes(2,100):
	Quaternion.N = N
	print()
	print(f"Primzahl ist {N}")
	for q in quat_gen(N):
		if q**2 == q and q.l() == 0:
			for q2 in quat_gen(N):
				if q+q2 == QUnit and q*q2 == QZero:
					print(q,q2)

"""



for N in generatePrimes(2,100):
	Quaternion.N = N
	print()
	print(f"Primzahl ist {N}")
	for q1 in quat_gen(N):
		if q1 != QZero and q1.l() == 0 and q1**2 == q1:
			for q2 in quat_gen(N):
				if q2 != QZero and q2 != q1.t() and q1 * q2 == QZero and q2**2 == q2: # and (q1 + q2).l() != 1:
					print(q1,q2, q1 + q2)


"""
def same_phase(q1, q2):
	return q2 * q1.l() == q1 * q2.l()

for N in generatePrimes(60,1000):
	Quaternion.N = N
	print()
	print(f"Primzahl ist {N}")
	for q1 in quat_gen_random(N, N**2):
		if same_phase(q1**2, q1):
			qn = q1 * STonelli(q1.l(), N)
			if qn**2 == qn and qn.l() != 0:
				print(qn)
"""


"""
for N in generatePrimes(2,100):
	Quaternion.N = N
	print()
	print(f"Primzahl ist {N}")
	for q1 in quat_gen(N):
		if q1 != QUnit and q1.l() != 0 and q1**2 == q1:
			print(q1)
"""

"""
for N in generatePrimes(2,100):
	Quaternion.N = N
	ctr = 0
	print()
	for q1 in quat_gen(N):
		if q1 != QZero and q1.l() == 0 and q1**2 == q1:
			ctr += 1

	print(f"Primzahl {N} hat {ctr} a2-Elemente")
"""

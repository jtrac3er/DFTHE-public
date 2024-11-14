"""
Der Keygen muss folgendes erstellen:
 - eine Primzahl p wählen
 - ein Quternionenpaar finden, sodass qenc[1]/q2 encoding möglich ist
 - ein Quaternion qu finden, sodass qu eine n-te unity root ist

"""

from quat import * 
from quathelper import *
from random import randint
from primes import *

def keygen(n, p):

	# Also die Schritte sind folgende: 
	# Finde eine normale Unity root
	# Finde ein quaternion u_1, wo Re(x) = 1 ist --> |Im(x)| = 0 
	# Finde irgend ein quaternion, welches q_1**2 = q_1 erfüllt
	# Berechne daraus q_2 = u_1 - q_1

	if not (p-1) % n == 0:
		raise ValueError("Für Primzahl p muss gelten, dass n|p-1")

	Quaternion.N = p

	while True:
		#qu = Quaternion(*[randint(0,p) for i in range(4)]) ** ((p-1) // n)
		qu = Quaternion(pow(randint(0,p),(p-1)//n,p),0,0,0)
		if qu**n != QUnit:
			continue
		for i in range(1,n):
			if qu == QUnit:
				qu = None
				break
		if qu:
			break

	while True:
		r = [randint(0,p) for i in range(2)]
		a = tonelli( -(sum([x**2 for x in r]) + ((p+1)//2)**2), p)
		q0 = Quaternion(((p+1)//2), a, *r)
		if q0.l() == 0 and q0**2 == q0:
			break

	while True:
		r = [randint(0,p) for i in range(2)]
		a = tonelli( -sum([x**2 for x in r]), p)
		qs = Quaternion(1, a, *r) ** (p-1 // n)

		q1 = qs - q0
		if q1.l() == 0 and q1**2 == q1 and q1 != q0.t():
			break

	# modifikation
	print(qs)
	qu = qs * qu

	assert(qu**n == QUnit)
	assert(q0**2 == q0 and q1**2 == q1)
	assert(q0 * q1 == QZero)

	class Key: pass 
	k = Key()
	k.n = n
	k.p = p
	k.q0 = q0
	k.q1 = q1
	k.qu = qu

	return k


if __name__ == '__main__':
	key = keygen(3, 61235746925250212479)
	print(f"Keygen hat key erstellt für n={key.n}. Bestehend aus (p,q0,q1,qu)")
	print(f"{key.p}\n{key.q1}\n{key.q0}\n{key.qu}")


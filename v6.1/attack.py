from keygen import *
from lgs_ex import *
from rational import *
from math import gcd

SK,HK,PK,_ = keygen(3, 96)


for i in range(2):
	for j in range(3):
		HK.CVL[i][j] = HK.CVL[i][j].l
		for k in range(3):
			HK.CVL[i][j][k] = Rational(HK.CVL[i][j][k], 1)

A = HK.CVL[0]
pp_mat(A)
print()

x = gauss_elimination(A, [Rational(1,1) for i in range(3)])
pp_vec(x)
print()

denominator = 1
for e in x:
	denominator *= e.b

print(SK.N)
print(denominator % SK.N)

# Also: Busted! Der Denominator ist ein Vielfaches von SK.N - Der Denominator ist zwar gross, aber
# besteht nicht zwangsläufig aus grossen Primfaktoren, weshalb man den denominator grundsätzlich auch
# einfach zerlegen kann und N herausfinden.
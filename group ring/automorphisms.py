from group import *
from ring import *
from helper import *

for k in range(10):
	G = ComplexGroup ** k
	print(len(G), calc_automorphisms(G))
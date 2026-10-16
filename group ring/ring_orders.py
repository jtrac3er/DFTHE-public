from itertools import product
from math import gcd, prod
from operator import index
from random import Random

from group import ComplexGroup, QuaternionGroup, DidierGruppe5
from ring import GroupRing, GroupRingElement
from ring import Zmod, ZmodElement

from helper import *

for p in primes_in_range(1, 100):

	R = Zmod(p)
	RH = GroupRing(R, ComplexGroup)

	for a in all_group_ring_elements(RH):
		if (a**2) == a and a != RH.one and a != RH.zero:
			print(f"Identity found for {p}: {a}")
			break
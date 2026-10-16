from group import *
from ring import *


G = QuaternionGroup ** 3
R = Zmod(7) ** 2

print("hallo")

RH = GroupRing(R, G)

print(2 * RH.one)
print(R(1,2)  * RH.one)
print(RH.zero)

print(len(G))
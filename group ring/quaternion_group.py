"""Quaternion group Q_8: i^2=j^2=k^2=ijk=-1.

Labels are strings because Python's complex numbers cannot represent all
quaternion units. Row times column gives the corresponding table entry.
"""

from group import FiniteGroup


QUATERNION_ELEMENTS = ('1', '-1', 'i', '-i', 'j', '-j', 'k', '-k')

CAYLEY_TABLE = (
    # 1     -1    i     -i    j     -j    k     -k
    ('1',  '-1', 'i',  '-i', 'j',  '-j', 'k',  '-k'),  # 1
    ('-1', '1',  '-i', 'i',  '-j', 'j',  '-k', 'k'),   # -1
    ('i',  '-i', '-1', '1',  'k',  '-k', '-j', 'j'),   # i
    ('-i', 'i',  '1',  '-1', '-k', 'k',  'j',  '-j'),  # -i
    ('j',  '-j', '-k', 'k',  '-1', '1',  'i',  '-i'),  # j
    ('-j', 'j',  'k',  '-k', '1',  '-1', '-i', 'i'),   # -j
    ('k',  '-k', 'j',  '-j', '-i', 'i',  '-1', '1'),   # k
    ('-k', 'k',  '-j', 'j',  'i',  '-i', '1',  '-1'),  # -k
)


def quaternion_group() -> FiniteGroup:
    """Return Q_8 under quaternion multiplication."""
    return FiniteGroup(QUATERNION_ELEMENTS, CAYLEY_TABLE)


if __name__ == '__main__':
    from ring import GroupRing, Zmod

    H = quaternion_group()
    i, j = H('i'), H('j')
    print('i * j =', i * j)
    print('j * i =', j * i)
    RH = GroupRing(Zmod(17), H)
    print('a =', RH((2, i), (3, j)))

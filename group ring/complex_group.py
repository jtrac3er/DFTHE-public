"""The fourth roots of unity as a group under complex multiplication.

All nonzero complex numbers form an infinite multiplicative group, so they
cannot be supplied as a finite Cayley table. The subgroup {1, i, -1, -i}
is closed and uses exactly representable complex numbers.
"""

from group import FiniteGroup


# Rows and columns use this same order: 1, i, -1, -i.

COMPLEX_ELEMENTS = (1, 1j, -1, -1j)

CAYLEY_TABLE = (
    (1 + 0j,  1j,      -1 + 0j, -1j),
    (1j,      -1 + 0j, -1j,      1 + 0j),
    (-1 + 0j, -1j,      1 + 0j,  1j),
    (-1j,      1 + 0j,  1j,     -1 + 0j),
)


def complex_unit_group() -> FiniteGroup:
    """Return C_4 with complex labels and complex multiplication."""
    return FiniteGroup(COMPLEX_ELEMENTS, CAYLEY_TABLE)


if __name__ == '__main__':
    from ring import GroupRing, Zmod

    H = complex_unit_group()
    i = H(1j)
    print('i * i =', i * i)
    print('i ** 4 =', i ** 4)
    RH = GroupRing(Zmod(7), H)
    a = RH((2, H.one), (3, i))
    print('a =', a)
    print('a * a =', a * a)

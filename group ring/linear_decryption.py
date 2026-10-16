"""Explore sections 1.1 and 3 of 'Grup Ring FHE Construction v1.0.pdf'.

F(x) = <pi(x), z>; D(x) = F(x*a). Search/solve over Zmod(m), including
composite m. No floating point, field-only Gaussian elimination, or dependencies.
Run: python linear_decryption.py
"""

from itertools import product
from math import gcd, prod
from operator import index
from random import Random

from group import ComplexGroup, QuaternionGroup, DidierGruppe5
from ring import GroupRing, GroupRingElement
from ring import Zmod, ZmodElement

from helper import *


"""
Also. Der Test soll folgendes sein. Ich habe einen zufälligen Gruppering und probiere linear zu decoden
"""

def run_test(H, M):
    R = Zmod(M)
    RH = GroupRing(R, H)

    k = totient(M)

    print(f"Totient-Function phi({M}) = {k}")

    TEST_MUL_LEN = 1000
    TEST_ADD_LEN = 100


    A = []
    b = []

    """
    i = 1
    s = set()
    while True:
        r = random_element(RH)
        test = r ** k

        if test in s:
            continue

        s.add(test)

        print(f"testvalue for {i} is {test}")
        A.append(test.coefficients)
        b.append(1)

        solution = solve_modular(A,b,M)

        if solution is not None and solution.count == 1:
            break

        i += 1
    """

    while True:

        for i in range(len(H)):
            r = random_element(RH)
            test = r ** k
            test = (test + RH.one) ** k
            A.append(test.coefficients)
            b.append(1)

        if (solution := solve_modular(A,b,M)) is not None:
            break

    print("\nparticular solution:")
    print(solution.particular)       # Eine konkrete Lösung
    print(f"\nOther solution vectors ({len(solution.generators)}):")
    print(solution.generators)       # Richtungen weiterer Lösungen

    def f(num): return scalar_prod(num.coefficients, solution.particular)

    """
    x = random_element(RH)
    if not f(x ** k) == R.one or f(x ** k) == R.zero:
        raise ValueError(f"f(r^k) = {f(x ** k)} which is not equal to 1 or 0")
    """

    for i in range(TEST_ADD_LEN):
        x = random_element(RH)
        y = random_element(RH)
        assert f(x) + f(y) == f(x+y)

    for i in range(TEST_MUL_LEN):
        x = random_element(RH)
        y = random_element(RH)
        if not f(x) * f(y) == f(x*y):
            raise ValueError(f"Multiplicative Homomorphic property violated for {x} and {y}. "
                             f"f(x)*f(y) := {f(x) * f(y)} != {f(x*y)} =: f(x*y)")



for p in primes_in_range(17, 100):
    run_test(ComplexGroup, p)
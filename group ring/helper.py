from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from math import gcd, prod
from operator import index
from random import Random

from group import CyclicGroup, FiniteGroup, Group
from ring import GroupRing, GroupRingElement
from ring import Zmod, ZmodElement

from math import isqrt
from operator import index


def count_automorphisms(group: Group) -> int:
    """Return the exact number |Aut(group)| for an enumerable finite group.

    An automorphism is a bijection f with f(x*y)=f(x)*f(y). The identity
    is fixed. Backtracking assigns images of new generators and propagates
    both ordered products through the generated subgroup. Element orders
    and centralizer sizes prune impossible images. Commutativity is not assumed.

    Uses O(n^2) memory for the multiplication table. Search time can grow
    exponentially; intended for small groups. The input must already satisfy
    the group axioms (as validated by FiniteGroup for a Cayley table).
    """
    return _count_automorphisms(group, stabilizer_chain=False)


def calc_automorphisms(group: Group) -> int:
    """Count automorphisms using an orbit-stabilizer chain, exactly.

    Works for any valid enumerable finite Group, including nonabelian groups.
    At each level, compute the orbit of one element under automorphisms fixing
    the previously chosen elements. Multiply the orbit sizes. Finding a single
    witness automorphism per unknown orbit target suffices: the algorithm does
    not enumerate all automorphisms. Witness permutations generate known orbit
    points, avoiding redundant searches. Product constraints propagate in both
    orders, with element order and centralizer size used as invariants.

    This is a pure-Python table-based algorithm, not a full implementation of
    specialized computer-algebra algorithms. Some groups still require an
    expensive backtracking search; it is not guaranteed faster on every group.
    Uses O(n^2) memory plus search state. Assumes the input satisfies group axioms.
    """
    return _count_automorphisms(group, stabilizer_chain=True)


def _count_automorphisms(group: Group, *, stabilizer_chain: bool) -> int:
    """Shared multiplication data and partial-isomorphism search."""
    if not isinstance(group, Group):
        raise TypeError('Expected an object implementing the Group interface.')
    labels = tuple(group.elements)
    positions = {label: i for i, label in enumerate(labels)}
    n = len(labels)
    if not n or len(positions) != n:
        raise ValueError('Group labels must be nonempty and distinct.')
    try:
        identity = positions[group.normalize(group.identity)]
        table = tuple(tuple(positions[group.normalize(group.multiply(a, b))]
                            for b in labels) for a in labels)
    except KeyError as exc:
        raise ValueError('Identity and products must belong to group.elements.') from exc

    signatures = []
    for a in range(n):
        power = identity
        for order in range(1, n + 1):
            power = table[power][a]
            if power == identity:
                break
        else:
            raise ValueError('Invalid finite group: an element has no finite order.')
        centralizer_size = sum(table[a][b] == table[b][a] for b in range(n))
        signatures.append((order, centralizer_size))
    targets = [tuple(b for b in range(n) if signatures[b] == signatures[a])
               for a in range(n)]

    def extend(mapping, reverse, source, target):
        pending = [(source, target)]
        while pending:
            a, image = pending.pop()
            if mapping[a] != -1:
                if mapping[a] != image:
                    return False
                continue
            if reverse[image] != -1 or signatures[a] != signatures[image]:
                return False
            mapping[a], reverse[image] = image, a
            for b, image_b in enumerate(mapping):
                if image_b != -1:
                    pending.append((table[a][b], table[image][image_b]))
                    pending.append((table[b][a], table[image_b][image]))
        return True

    def choose_source(mapping, reverse):
        source, candidates = None, None
        for a in range(n):
            if mapping[a] == -1:
                available = [b for b in targets[a] if reverse[b] == -1]
                if not available:
                    return a, []
                if candidates is None or len(available) < len(candidates):
                    source, candidates = a, available
        return source, candidates

    def search(mapping, reverse):
        source, candidates = choose_source(mapping, reverse)
        if source is None:
            return 1
        count = 0
        for target in candidates:
            next_mapping, next_reverse = mapping.copy(), reverse.copy()
            if extend(next_mapping, next_reverse, source, target):
                count += search(next_mapping, next_reverse)
        return count

    def find_witness(mapping, reverse):
        """Return one full automorphism extending the partial mapping, or None."""
        source, candidates = choose_source(mapping, reverse)
        if source is None:
            return mapping
        # Identity images are often an immediate completion for a stabilizer.
        candidates.sort(key=lambda target: target != source)
        for target in candidates:
            next_mapping, next_reverse = mapping.copy(), reverse.copy()
            if extend(next_mapping, next_reverse, source, target):
                witness = find_witness(next_mapping, next_reverse)
                if witness is not None:
                    return witness
        return None

    def count_by_stabilizers(mapping, reverse):
        result = 1
        while True:
            source, candidates = choose_source(mapping, reverse)
            if source is None:
                return result
            orbit, witnesses = {source}, []
            for target in candidates:
                if target in orbit:
                    continue
                next_mapping, next_reverse = mapping.copy(), reverse.copy()
                if not extend(next_mapping, next_reverse, source, target):
                    continue
                witness = find_witness(next_mapping, next_reverse)
                if witness is None:
                    continue
                witnesses.append(witness)
                # Close the orbit under all known witness permutations. Because
                # these are permutations of a finite set, forward closure also
                # contains the action of their inverses.
                pending = list(orbit)
                while pending:
                    point = pending.pop()
                    for permutation in witnesses:
                        image = permutation[point]
                        if image not in orbit:
                            orbit.add(image)
                            pending.append(image)
            result *= len(orbit)
            # Pass to the pointwise stabilizer. Fixing the chosen generators
            # forces their entire generated subgroup to be fixed too.
            if not extend(mapping, reverse, source, source):
                raise ValueError('Invalid group: identity mapping is inconsistent.')

    mapping, reverse = [-1] * n, [-1] * n
    if not extend(mapping, reverse, identity, identity):
        raise ValueError('Invalid group identity or multiplication.')
    if stabilizer_chain:
        return count_by_stabilizers(mapping, reverse)
    return search(mapping, reverse)


def primes_in_range(start: int, stop: int):
    """Yield primes p with start <= p < stop, in ascending order.

    Like range(), stop is excluded. Bounds must be integers. An empty
    interval yields nothing; values below 2 are skipped.
    """
    start, stop = index(start), index(stop)
    if start <= 2 < stop:
        yield 2
    first = max(start, 3)
    if first % 2 == 0:
        first += 1
    for candidate in range(first, stop, 2):
        if all(candidate % divisor for divisor in range(3, isqrt(candidate) + 1, 2)):
            yield candidate


def all_group_ring_elements(algebra):
    """Yield every element of Z_m[H] exactly once, including zero.

    Coefficient vectors follow algebra.group.elements and are enumerated
    lexicographically: the last coefficient changes fastest. There are
    m**len(H) elements. Elements are generated lazily, not collected in a list.
    """
    if not isinstance(algebra, GroupRing) or not isinstance(algebra.base_ring, Zmod):
        raise TypeError('Expected a GroupRing with base ring Zmod(m).')
    for coefficients in product(range(algebra.base_ring.modulus),
                                repeat=len(algebra.group.elements)):
        yield algebra.from_coefficients(coefficients)


def random_element(algebra, seed=None) -> GroupRingElement:
    """Random element of Z_m[H], with independent uniform coefficients.

    With no arguments, use the RH defined in this module. Pass a different
    GroupRing as `algebra` if needed. A seed makes the result reproducible.
    Zero coefficients are allowed.
    """
    if not isinstance(algebra, GroupRing) or not isinstance(algebra.base_ring, Zmod):
        raise TypeError('Expected a GroupRing with base ring Zmod(m).')
    rng = Random(seed)
    return algebra.from_coefficients(
        rng.randrange(algebra.base_ring.modulus)
        for _ in algebra.group.elements
    )

def totient(m):
    """Euler phi(m), including phi(1)=1."""
    m = index(m)
    if m < 1:
        raise ValueError('Modulus must be positive.')
    result, remainder, p = m, m, 2
    while p * p <= remainder:
        if remainder % p == 0:
            result -= result // p
            while remainder % p == 0:
                remainder //= p
        p += 1
    if remainder > 1:
        result -= result // remainder
    return result


def scalar_prod(a,b):
    """Scalar product of nonempty, equally sized vectors in matching order."""
    try:
        a, b = tuple(a), tuple(b)
    except TypeError as exc:
        raise TypeError('Both arguments must be iterable coefficient vectors.') from exc
    if len(a) != len(b):
        raise ValueError(f'Vectors must have the same length; got {len(a)} and {len(b)}.')
    if not a:
        raise ValueError('Coefficient vectors must not be empty.')
    res = a[0] * b[0]
    for i in range(1, len(a)):
        res += a[i] * b[i]
    return res


def solve_modular(matrix, rhs, modulus):
    """Solve A*z=rhs modulo m; return None iff the system is inconsistent.

    Parameters
    ----------
    matrix : iterable of iterables of integers or ZmodElement objects
        Nonempty rectangular matrix, typically a list of lists. The outer
        list contains ROWS (equations), the inner lists contain their column
        entries (coefficients of the unknowns). Indexing is row-first:
        matrix[i][j] = A_ij = coefficient of z[j] in equation i (zero-based).
        This specifies logical row-major nesting, not a physical memory layout.
        Example: [[2, 3], [4, 5]] represents the equations
        2*z[0] + 3*z[1] = rhs[0] and 4*z[0] + 5*z[1] = rhs[1], modulo m.
        For the paper's system, row i contains the coefficient vector of
        a**(i+1); column j corresponds to a.variables[j].
    rhs : iterable of integers or ZmodElement objects
        One right-hand-side value per row: len(rhs) == number of rows.
        For A*z=1, use [1] * len(matrix).
    modulus : positive integer or Zmod
        The modulus m or the coefficient ring Zmod(m).
        All equations are interpreted modulo m.

    Returns
    -------
    ModularSolutions or None
        Solution vectors use COLUMN order: z[j] belongs to column j of A.
        particular, generators and vectors() contain ZmodElement objects,
        so scalar_prod(row, solution.particular) computes directly in Zmod(m).
        None means that no solution exists modulo m.

    Integer unimodular row/column operations diagonalize A. This works for
    composite m and nonunit pivots. It is not a division algorithm over a field.
    A full Smith divisibility chain is unnecessary for solving congruences.
    """

    @dataclass(frozen=True)
    class ModularSolutions:
        """All solutions of a modular linear system.

        Each solution is particular + sum(t_i * generators[i]) modulo modulus,
        with 0 <= t_i < orders[i]. Vector coordinates follow matrix column order.
        """
        modulus: int
        particular: tuple[ZmodElement, ...]
        generators: tuple[tuple[ZmodElement, ...], ...]
        orders: tuple[int, ...]

        @property
        def count(self) -> int:
            """Number of solutions represented by the independent generators."""
            return prod(self.orders)

        def vectors(self):
            """Yield every solution as a tuple in column order."""
            for parameters in product(*(range(order) for order in self.orders)):
                yield tuple(
                    value + sum(t * generator[i]
                                for t, generator in zip(parameters, self.generators))
                    for i, value in enumerate(self.particular)
                )



    R = modulus if isinstance(modulus, Zmod) else Zmod(index(modulus))
    m = R.modulus
    B = [[R.normalize(v) for v in row] for row in matrix]
    b = [R.normalize(v) for v in rhs]
    if not B or len(B) != len(b) or not B[0] or any(len(row) != len(B[0]) for row in B):
        raise ValueError('Expected a nonempty rectangular matrix and matching RHS.')
    rows, cols = len(B), len(B[0])
    V = [[int(i == j) for j in range(cols)] for i in range(cols)]

    def swap_rows(i, j):
        B[i], B[j] = B[j], B[i]
        b[i], b[j] = b[j], b[i]

    def swap_cols(i, j):
        for row in B:
            row[i], row[j] = row[j], row[i]
        for row in V:
            row[i], row[j] = row[j], row[i]

    rank = 0
    for k in range(min(rows, cols)):
        positions = [(abs(B[i][j]), i, j) for i in range(k, rows)
                     for j in range(k, cols) if B[i][j]]
        if not positions:
            break
        _, i, j = min(positions)
        swap_rows(k, i)
        swap_cols(k, j)
        while True:
            i = next((i for i in range(k + 1, rows) if B[i][k]), None)
            if i is not None:
                q = B[i][k] // B[k][k]
                B[i] = [v - q * w for v, w in zip(B[i], B[k])]
                b[i] -= q * b[k]
                if B[i][k]:
                    swap_rows(k, i)
                continue
            j = next((j for j in range(k + 1, cols) if B[k][j]), None)
            if j is not None:
                q = B[k][j] // B[k][k]
                for row in B:
                    row[j] -= q * row[k]
                for row in V:
                    row[j] -= q * row[k]
                if B[k][j]:
                    swap_cols(k, j)
                continue
            break
        rank += 1
    if any(b[i] % m for i in range(rank, rows)):
        return None
    y = [0] * cols
    steps = []
    for i in range(cols):
        if i >= rank:
            if m > 1:
                steps.append((i, 1, m))
            continue
        d = B[i][i]
        g = gcd(d, m)
        if b[i] % g:
            return None
        reduced = m // g
        y[i] = (b[i] // g * pow(d // g, -1, reduced)) % reduced
        if g > 1:
            steps.append((i, reduced, g))
    particular = tuple(R(sum(V[i][j] * y[j] for j in range(cols))) for i in range(cols))
    generators = tuple(tuple(R(V[i][j] * step) for i in range(cols))
                       for j, step, _ in steps)
    return ModularSolutions(m, particular, generators, tuple(order for _, _, order in steps))

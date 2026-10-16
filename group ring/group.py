from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass, field
from operator import index
from itertools import product
from types import MappingProxyType
from collections.abc import Hashable
from typing import Any, Protocol, TypeVar, runtime_checkable


def format_group_label(label):
    """Compact group labels, including j/-j without signed-zero artifacts."""
    if isinstance(label, tuple):
        entries = ', '.join(format_group_label(value) for value in label)
        return '(' + entries + (',' if len(label) == 1 else '') + ')'
    if isinstance(label, complex):
        if label.imag == 0:
            return str(int(label.real)) if label.real.is_integer() else str(label.real)
        if label.real == 0:
            if label.imag == 1:
                return 'j'
            if label.imag == -1:
                return '-j'
            magnitude = str(int(label.imag)) if label.imag.is_integer() else str(label.imag)
            return magnitude + 'j'
    return str(label)



@runtime_checkable
class Group(Protocol):
    """An enumerable finite group, independent of any Cayley table storage."""

    @property
    def elements(self) -> tuple[Hashable, ...]: ...

    @property
    def identity(self) -> Hashable: ...

    def normalize(self, element: Any) -> Hashable: ...
    def multiply(self, left: Hashable, right: Hashable) -> Hashable: ...
    def inverse(self, element: Hashable) -> Hashable: ...



class GroupPowers:
    """Optional mixin providing direct products G*H and powers G**n.

    G*H uses pair labels (g, h). Nested products retain nested tuple labels:
    (G*H)*K has labels ((g, h), k).
    """

    def __mul__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return DirectProductGroup((self, other))

    def __rmul__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return DirectProductGroup((other, self))

    def __pow__(self, exponent):
        exponent = index(exponent)
        if exponent < 0:
            raise ValueError('Direct group powers require a nonnegative exponent.')
        if exponent == 1:
            return self
        return DirectProductGroup((self,) * exponent)


@dataclass(frozen=True, init=False)
class FiniteGroup(GroupPowers):
    """Rows and columns follow `elements`; entries are element labels.

    Construction validates closure, identity, inverses and associativity.
    Validation takes O(|H|^3) time. Labels must be distinct and hashable.
    """

    elements: tuple
    table: tuple
    identity: Hashable
    _indices: Mapping = field(repr=False, compare=False, hash=False)

    def __init__(self, elements: Sequence[Hashable], cayley_table: Sequence[Sequence[Hashable]]):
        labels = tuple(elements)
        if not labels:
            raise ValueError("A group must contain at least one element.")
        lookup = {label: i for i, label in enumerate(labels)}
        if len(lookup) != len(labels):
            raise ValueError("Group labels must be distinct.")
        rows = tuple(tuple(row) for row in cayley_table)
        n = len(labels)
        if len(rows) != n or any(len(row) != n for row in rows):
            raise ValueError(f"Expected a {n} x {n} Cayley table.")
        try:
            table = tuple(tuple(lookup[label] for label in row) for row in rows)
        except KeyError as exc:
            raise ValueError(f"Unknown label in Cayley table: {exc.args[0]!r}") from exc
        identities = [e for e in range(n) if all(table[e][a] == a and table[a][e] == a for a in range(n))]
        if len(identities) != 1:
            raise ValueError("The table must have a unique two-sided identity.")
        e = identities[0]
        if any(not any(table[a][b] == e and table[b][a] == e for b in range(n)) for a in range(n)):
            raise ValueError("Every group element must have a two-sided inverse.")
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    if table[table[a][b]][c] != table[a][table[b][c]]:
                        raise ValueError(f"Table is not associative at {(labels[a], labels[b], labels[c])!r}.")
        object.__setattr__(self, "elements", labels)
        object.__setattr__(self, "table", table)
        object.__setattr__(self, "identity", labels[e])
        object.__setattr__(self, "_indices", MappingProxyType(lookup))

    def multiply(self, left: Hashable, right: Hashable) -> Hashable:
        left, right = self._label(left), self._label(right)
        return self.elements[self.table[self._indices[left]][self._indices[right]]]

    def inverse(self, element: Hashable) -> Hashable:
        element = self._label(element)
        a, e = self._indices[element], self._indices[self.identity]
        return next(self.elements[b] for b in range(len(self.elements)) if self.table[a][b] == e)

    def _label(self, element):
        if isinstance(element, GroupElement):
            if element.group != self:
                raise ValueError("Elements belong to different groups.")
            element = element.label
        if element not in self._indices:
            raise ValueError(f"Unknown group label: {element!r}")
        return element

    def normalize(self, element) -> Hashable:
        return self._label(element)

    def __call__(self, label: Hashable) -> "GroupElement":
        return GroupElement(self, self._label(label))

    @property
    def one(self) -> "GroupElement":
        return self(self.identity)

    def __len__(self) -> int:
        return len(self.elements)


@dataclass(frozen=True)
class GroupElement:
    group: Group
    label: Hashable

    def __post_init__(self):
        if not isinstance(self.group, Group):
            raise TypeError("group must implement the Group interface.")
        object.__setattr__(self, 'label', self.group.normalize(self.label))

    def __mul__(self, other):
        if not isinstance(other, GroupElement):
            return NotImplemented
        if other.group != self.group:
            raise ValueError("Elements belong to different groups.")
        return GroupElement(self.group, self.group.multiply(self.label, other.label))

    def inverse(self):
        return GroupElement(self.group, self.group.inverse(self.label))

    def __pow__(self, exponent):
        exponent = index(exponent)
        base = self
        if exponent < 0:
            base, exponent = self.inverse(), -exponent
        result = GroupElement(self.group, self.group.identity)
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result

    def __str__(self):
        return format_group_label(self.label)

    def __repr__(self):
        return str(self)


@dataclass(frozen=True)
class CyclicGroup(GroupPowers):
    """C_n with labels 0,...,n-1; composition is addition modulo n."""

    order: int

    def __post_init__(self):
        n = index(self.order)
        if n < 1:
            raise ValueError("Group order must be positive.")
        object.__setattr__(self, 'order', n)

    @property
    def elements(self):
        return tuple(range(self.order))

    @property
    def identity(self):
        return 0

    def normalize(self, element):
        if isinstance(element, GroupElement):
            if element.group != self:
                raise ValueError("Elements belong to different groups.")
            return element.label
        return index(element) % self.order

    def multiply(self, left, right):
        return (self.normalize(left) + self.normalize(right)) % self.order

    def inverse(self, element):
        return -self.normalize(element) % self.order

    def __call__(self, label):
        return GroupElement(self, self.normalize(label))

    @property
    def one(self):
        return self(self.identity)

    def __len__(self):
        return self.order


@dataclass(frozen=True)
class DirectProductGroup(GroupPowers):
    """Direct product of finite groups, with tuple labels.

    Operations and inverses act componentwise and preserve operand order.
    Elements follow itertools.product order (last component changes fastest).
    The empty product is the trivial group with sole element (). No Cayley
    table is built; only the tuple of all labels is materialized.
    """

    factors: tuple[Group, ...]
    _elements: tuple = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        factors = tuple(self.factors)
        if any(not isinstance(group, Group) for group in factors):
            raise TypeError('Each factor must implement the Group interface.')
        object.__setattr__(self, 'factors', factors)
        object.__setattr__(self, '_elements',
                           tuple(product(*(group.elements for group in factors))))

    @property
    def elements(self):
        return self._elements

    @property
    def identity(self):
        return tuple(group.identity for group in self.factors)

    def normalize(self, element):
        if isinstance(element, GroupElement):
            if element.group != self:
                raise ValueError('Elements belong to different groups.')
            element = element.label
        if not isinstance(element, tuple) or len(element) != len(self.factors):
            raise ValueError(f'Expected a tuple of {len(self.factors)} group labels.')
        return tuple(group.normalize(value) for group, value in zip(self.factors, element))

    def multiply(self, left, right):
        left, right = self.normalize(left), self.normalize(right)
        return tuple(group.multiply(a, b) for group, a, b in zip(self.factors, left, right))

    def inverse(self, element):
        element = self.normalize(element)
        return tuple(group.inverse(value) for group, value in zip(self.factors, element))

    def __call__(self, label):
        return GroupElement(self, self.normalize(label))

    @property
    def one(self):
        return self(self.identity)

    def __len__(self):
        return len(self._elements)



COMPLEX_ELEMENTS = (1, 1j, -1, -1j)
CAYLEY_TABLE_COMPLEX = (
    (1,   1j,  -1, -1j),
    (1j,  -1, -1j,   1),
    (-1, -1j,   1,  1j),
    (-1j,  1,  1j,  -1),
)

QUATERNION_ELEMENTS = ('1', '-1', 'i', '-i', 'j', '-j', 'k', '-k')
CAYLEY_TABLE_QUATERNION = (
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


D5_ELEMENTS = ('e', 'r', 'r2', 'r3', 'r4','s', 'rs', 'r2s', 'r3s', 'r4s')
CAYLEY_TABLE_D5 = (
    ('e',  'r',  'r2', 'r3', 'r4', 's',   'rs',  'r2s', 'r3s', 'r4s'),
    ('r',  'r2', 'r3', 'r4', 'e',  'rs',  'r2s', 'r3s', 'r4s', 's'),
    ('r2', 'r3', 'r4', 'e',  'r',  'r2s', 'r3s', 'r4s', 's',   'rs'),
    ('r3', 'r4', 'e',  'r',  'r2', 'r3s', 'r4s', 's',   'rs',  'r2s'),
    ('r4', 'e',  'r',  'r2', 'r3', 'r4s', 's',   'rs',  'r2s', 'r3s'),
    ('s',   'r4s', 'r3s', 'r2s', 'rs',  'e',  'r4', 'r3', 'r2', 'r'),
    ('rs',  's',   'r4s', 'r3s', 'r2s', 'r',  'e',  'r4', 'r3', 'r2'),
    ('r2s', 'rs',  's',   'r4s', 'r3s', 'r2', 'r',  'e',  'r4', 'r3'),
    ('r3s', 'r2s', 'rs',  's',   'r4s', 'r3', 'r2', 'r',  'e',  'r4'),
    ('r4s', 'r3s', 'r2s', 'rs',  's',   'r4', 'r3', 'r2', 'r',  'e'),
)


ComplexGroup = FiniteGroup(COMPLEX_ELEMENTS, CAYLEY_TABLE_COMPLEX)
QuaternionGroup = FiniteGroup(QUATERNION_ELEMENTS, CAYLEY_TABLE_QUATERNION)
DidierGruppe5 = FiniteGroup(D5_ELEMENTS, CAYLEY_TABLE_D5)


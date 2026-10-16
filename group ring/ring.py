"""Rings, ring elements and generic group rings R[H]."""
from __future__ import annotations

from collections.abc import Hashable, Mapping
from dataclasses import dataclass, field
from fractions import Fraction
from operator import index
from types import MappingProxyType
from typing import Generic, TypeVar
from collections.abc import Hashable
from typing import Any, Protocol, TypeVar, runtime_checkable
from group import Group, format_group_label

C = TypeVar('C')


@runtime_checkable
class Ring(Protocol[C]):
    """A unital ring; normalize returns its canonical coefficient type."""

    def normalize(self, value: Any) -> C: ...
    def add(self, left: C, right: C) -> C: ...
    def multiply(self, left: C, right: C) -> C: ...
    def negate(self, value: C) -> C: ...
    def is_zero(self, value: C) -> bool: ...
    
    @property
    def zero(self) -> Any: ...

    @property
    def one(self) -> Any: ...




class RingElement:
    """Reusable operators for elements of a Ring implementation.

    Subclasses expose `ring`; their parent normalizes them to canonical values.
    The parent must be callable to build result elements. No implicit conversion
    between different parent rings; embedding into a group ring is supported.
    """

    def _coerce(self, other):
        if isinstance(other, RingElement) and other.ring != self.ring:
            if getattr(other.ring, 'base_ring', None) == self.ring:
                return NotImplemented
            raise ValueError('Elements belong to different rings.')
        try:
            return self.ring.normalize(other)
        except TypeError:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, GroupRingElement) and other.ring.base_ring == self.ring:
            return other.__add__(self)
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self.ring(self.ring.add(self.ring.normalize(self), other))

    __radd__ = __add__

    def __neg__(self):
        return self.ring(self.ring.negate(self.ring.normalize(self)))

    def __sub__(self, other):
        if isinstance(other, GroupRingElement) and other.ring.base_ring == self.ring:
            return other.__rsub__(self)
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self.ring(self.ring.add(self.ring.normalize(self), self.ring.negate(other)))

    def __rsub__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self.ring(self.ring.add(other, self.ring.negate(self.ring.normalize(self))))

    def __mul__(self, other):
        if isinstance(other, GroupRingElement) and other.ring.base_ring == self.ring:
            return other.__rmul__(self)
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self.ring(self.ring.multiply(self.ring.normalize(self), other))

    def __rmul__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self.ring(self.ring.multiply(other, self.ring.normalize(self)))

    def __pow__(self, exponent):
        exponent = index(exponent)
        if exponent < 0:
            raise ValueError('Only nonnegative powers are supported.')
        result, base = self.ring(self.ring.one), self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result

    def __bool__(self):
        return not self.ring.is_zero(self.ring.normalize(self))

    def random(self):
        return NotImplemented

    def __repr__(self):
        return str(self)


@dataclass(frozen=True, repr=False)
class ScalarRingElement(RingElement):
    ring: Ring
    value: object

    def __post_init__(self):
        if not callable(getattr(self.ring, 'normalize', None)):
            raise TypeError('ring must provide normalize().')
        object.__setattr__(self, 'value', self.ring.normalize(self.value))

    def __str__(self):
        return str(self.value)



@dataclass(frozen=True, repr=False)
class ZmodElement(ScalarRingElement):
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True, repr=False)
class IntegerElement(ScalarRingElement):
    def __int__(self):
        return self.value



@dataclass(frozen=True, repr=False)
class RationalElement(ScalarRingElement):
    pass


class RingProducts:
    """Direct products R*S and repeated direct products R**n."""

    def __mul__(self, other):
        if not isinstance(other, Ring):
            return NotImplemented
        return DirectProductRing((self, other))

    def __rmul__(self, other):
        if not isinstance(other, Ring):
            return NotImplemented
        return DirectProductRing((other, self))

    def __pow__(self, exponent):
        exponent = index(exponent)
        if exponent < 0:
            raise ValueError('Direct ring powers require a nonnegative exponent.')
        if exponent == 1:
            return self
        return DirectProductRing((self,) * exponent)


class ScalarRing(RingProducts):
    """Optional mixin for Ring implementations represented by scalar values.

    Override normalize and element_type. The Ring Protocol remains structural.
    """

    element_type = ScalarRingElement

    def _unwrap(self, value):
        if isinstance(value, RingElement):
            if value.ring != self:
                raise ValueError('Elements belong to different coefficient rings.')
            return value.value
        return value

    def __call__(self, value=0):
        if isinstance(value, self.element_type) and value.ring == self:
            return value
        return self.element_type(self, self.normalize(value))

    def add(self, left, right):
        return self.normalize(self.normalize(left) + self.normalize(right))

    def multiply(self, left, right):
        return self.normalize(self.normalize(left) * self.normalize(right))

    def negate(self, value):
        return self.normalize(-self.normalize(value))

    def is_zero(self, value):
        return self.normalize(value) == self.normalize(0)

    @property
    def zero(self):
        return self(0)

    @property
    def one(self):
        return self(1)


@dataclass(frozen=True)
class Zmod(ScalarRing):
    """Z/mZ, for any positive integer m, including composite moduli."""
    modulus: int
    element_type = ZmodElement

    def __post_init__(self):
        m = index(self.modulus)
        if m < 1:
            raise ValueError('modulus must be positive.')
        object.__setattr__(self, 'modulus', m)

    def normalize(self, value):
        return index(self._unwrap(value)) % self.modulus


@dataclass(frozen=True)
class IntegerRing(ScalarRing):
    """Z, with IntegerElement objects and exact integer coefficients."""
    element_type = IntegerElement

    def normalize(self, value):
        return index(self._unwrap(value))


@dataclass(frozen=True)
class RationalRing(ScalarRing):
    """Q, with exact Fraction coefficients; floating point input is rejected."""
    element_type = RationalElement

    def normalize(self, value):
        value = self._unwrap(value)
        if isinstance(value, Fraction):
            return value
        return Fraction(index(value))


@dataclass(frozen=True, repr=False)
class DirectProductRingElement(ScalarRingElement):
    """Tuple of canonical coefficients with componentwise ring operations."""

    @property
    def components(self):
        """Component elements, each belonging to its corresponding factor ring."""
        return tuple(ring(value) for ring, value in zip(self.ring.factors, self.value))

    def __getitem__(self, position):
        return self.components[position]

    def __iter__(self):
        return iter(self.components)

    def __len__(self):
        return len(self.value)

    def __str__(self):
        entries = ', '.join(str(component) for component in self.components)
        return '(' + entries + (',' if len(self.value) == 1 else '') + ')'


@dataclass(frozen=True)
class DirectProductRing(RingProducts):
    """R_1 x ... x R_n, with componentwise operations and tuple values.

    Construct elements with P((a,b)) or P(a,b). Integers embed diagonally:
    P(k) = (k*1_R, k*1_S). R*S*T retains nested pairs ((r,s),t), whereas
    R**3 uses triples. The empty direct product is the one-element zero ring.
    """

    factors: tuple[Ring, ...]

    def __post_init__(self):
        factors = tuple(self.factors)
        if any(not isinstance(ring, Ring) for ring in factors):
            raise TypeError('Each factor must implement the Ring interface.')
        object.__setattr__(self, 'factors', factors)

    def normalize(self, value):
        if isinstance(value, RingElement):
            if value.ring != self:
                raise ValueError('Elements belong to different rings.')
            value = value.value
        if isinstance(value, tuple):
            if len(value) != len(self.factors):
                raise ValueError(f'Expected {len(self.factors)} components, got {len(value)}.')
            return tuple(ring.normalize(component)
                         for ring, component in zip(self.factors, value))
        scalar = index(value)
        return tuple(ring.normalize(scalar) for ring in self.factors)

    def __call__(self, value=0, *components):
        if components:
            value = (value,) + components
        if isinstance(value, DirectProductRingElement) and value.ring == self:
            return value
        return DirectProductRingElement(self, self.normalize(value))

    def add(self, left, right):
        left, right = self.normalize(left), self.normalize(right)
        return tuple(ring.add(a, b) for ring, a, b in zip(self.factors, left, right))

    def multiply(self, left, right):
        left, right = self.normalize(left), self.normalize(right)
        return tuple(ring.multiply(a, b) for ring, a, b in zip(self.factors, left, right))

    def negate(self, value):
        return tuple(ring.negate(component)
                     for ring, component in zip(self.factors, self.normalize(value)))

    def is_zero(self, value):
        return all(ring.is_zero(component)
                   for ring, component in zip(self.factors, self.normalize(value)))

    @property
    def zero(self):
        return self(tuple(ring.normalize(ring.zero) for ring in self.factors))

    @property
    def one(self):
        return self(tuple(ring.normalize(ring.one) for ring in self.factors))


@dataclass(frozen=True)
class GroupRing(RingProducts, Generic[C]):
    """R[H] for any Ring implementation and enumerable finite Group."""

    base_ring: Ring[C]
    group: Group
    _elements: tuple = field(init=False, repr=False, compare=False)
    _indices: Mapping = field(init=False, repr=False, compare=False, hash=False)
    _table: tuple = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        if not isinstance(self.base_ring, Ring):
            raise TypeError("base_ring must implement the Ring interface.")
        if not isinstance(self.group, Group):
            raise TypeError("group must implement the Group interface.")
        labels = tuple(self.group.elements)
        lookup = {h: i for i, h in enumerate(labels)}
        if not labels or len(lookup) != len(labels):
            raise ValueError("Group labels must be nonempty and distinct.")
        if self.group.normalize(self.group.identity) not in lookup:
            raise ValueError("Group identity is not in elements.")
        try:
            table = tuple(tuple(lookup[self.group.normalize(self.group.multiply(h, k))]
                                for k in labels) for h in labels)
        except KeyError as exc:
            raise ValueError("Group multiplication is not closed on elements.") from exc
        object.__setattr__(self, '_elements', labels)
        object.__setattr__(self, '_indices', MappingProxyType(lookup))
        object.__setattr__(self, '_table', table)

    @property
    def modulus(self) -> int:
        """Convenience for modular base rings; other rings have no modulus."""
        return getattr(self.base_ring, 'modulus')

    def from_coefficients(self, values) -> "GroupRingElement[C]":
        """Explicit ordered-vector constructor, including tuple-valued rings."""
        return GroupRingElement(self, tuple(values))

    def from_terms(self, *terms) -> "GroupRingElement[C]":
        """Build from (coefficient, group label/element) pairs; combine repeats."""
        R = self.base_ring
        values = [R.normalize(R.zero)] * len(self._elements)
        for term in terms:
            if not isinstance(term, tuple) or len(term) != 2:
                raise TypeError('Each term must be a (coefficient, group element) tuple.')
            coefficient, label = term
            i = self._indices[self.group.normalize(label)]
            values[i] = R.add(values[i], R.normalize(coefficient))
        return self.from_coefficients(values)

    def __call__(self, coefficients=None, *terms) -> "GroupRingElement":
        """Build from (coefficient, group) terms, a mapping, vector, or scalar.

        A scalar means scalar times the group identity, not every basis element.
        A single 2-tuple is a term unless the base ring accepts it as a scalar.
        Use from_terms/from_coefficients to resolve tuple-valued ambiguities.
        """
        if terms:
            return self.from_terms(coefficients, *terms)
        if isinstance(coefficients, tuple) and len(coefficients) == 2:
            try:
                self.base_ring.normalize(coefficients)
            except TypeError:
                return self.from_terms(coefficients)
        if isinstance(coefficients, GroupRingElement) and coefficients.ring == self:
            return coefficients
        if coefficients is None:
            values = [self.base_ring.normalize(self.base_ring.zero)] * len(self._elements)
        elif isinstance(coefficients, Mapping):
            values = [self.base_ring.normalize(self.base_ring.zero)] * len(self._elements)
            for label, value in coefficients.items():
                i = self._indices[self.group.normalize(label)]
                values[i] = self.base_ring.add(values[i], self.base_ring.normalize(value))
        else:
            try:
                scalar = self.base_ring.normalize(coefficients)
            except TypeError:
                values = tuple(coefficients)
            else:
                values = [self.base_ring.normalize(self.base_ring.zero)] * len(self._elements)
                values[self._indices[self.group.normalize(self.group.identity)]] = scalar
        return self.from_coefficients(values)

    def normalize(self, value):
        return self(value)

    def add(self, left, right):
        return self(left) + self(right)

    def multiply(self, left, right):
        return self(left) * self(right)

    def negate(self, value):
        return -self(value)

    def is_zero(self, value):
        return not bool(self(value))

    def basis(self, label: Hashable) -> "GroupRingElement":
        return self({label: self.base_ring.one})

    @property
    def zero(self) -> "GroupRingElement":
        return self()

    @property
    def one(self) -> "GroupRingElement":
        return self({self.group.identity: self.base_ring.one})


@dataclass(frozen=True, repr=False)
class GroupRingElement(RingElement, Generic[C]):
    """Immutable element sum_h a_h h with canonical coefficients in R."""

    ring: GroupRing[C]
    coefficients: tuple[C, ...]

    def __post_init__(self):
        if not isinstance(self.ring, GroupRing):
            raise TypeError("ring must be a GroupRing.")
        values = tuple(self.ring.base_ring.normalize(v) for v in self.coefficients)
        if len(values) != len(self.ring._elements):
            raise ValueError("Coefficient vector must have one entry per group element.")
        object.__setattr__(self, "coefficients", values)

    def _coerce(self, other):
        if isinstance(other, RingElement):
            if other.ring == self.ring:
                return self.ring(other)
            if getattr(other.ring, 'base_ring', None) == self.ring:
                return NotImplemented
            if other.ring != self.ring.base_ring:
                raise ValueError("Elements belong to different rings.")
        try:
            scalar = self.ring.base_ring.normalize(other)
        except TypeError:
            return NotImplemented
        return self.ring({self.ring.group.identity: scalar})

    def __getitem__(self, label: Hashable) -> C:
        group = self.ring.group
        return self.coefficients[self.ring._indices[group.normalize(label)]]

    @property
    def variables(self) -> tuple[Hashable, ...]:
        """All group labels, in the same order as coefficients."""
        return self.ring.group.elements

    def as_dict(self) -> dict:
        """Return the nonzero coefficients keyed by group labels."""
        return {h: a for h, a in zip(self.ring._elements, self.coefficients)
                if not self.ring.base_ring.is_zero(a)}

    def __add__(self, other):
        if isinstance(other, GroupRingElement) and other.ring.base_ring == self.ring:
            return other.__add__(self)
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        R = self.ring.base_ring
        return self.ring.from_coefficients(R.add(a, b) for a, b in zip(self.coefficients, other.coefficients))

    __radd__ = __add__

    def __neg__(self):
        return self.ring.from_coefficients(self.ring.base_ring.negate(a) for a in self.coefficients)

    def __sub__(self, other):
        if isinstance(other, GroupRingElement) and other.ring.base_ring == self.ring:
            return other.__rsub__(self)
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self + (-other)

    def __rsub__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return other + (-self)

    def scale(self, scalar, *, left=False):
        """Multiply every coefficient by a scalar from the base ring R.

        left=False: (a_h) -> (a_h * scalar), as in self * scalar.
        left=True:  (a_h) -> (scalar * a_h), as in scalar * self.
        The order matters when R is noncommutative. Group labels stay fixed.
        """
        R = self.ring.base_ring
        if isinstance(scalar, RingElement) and scalar.ring != R:
            raise ValueError('Scalar must belong to the group ring\'s base ring.')
        scalar = R.normalize(scalar)
        if left:
            values = (R.multiply(scalar, coefficient) for coefficient in self.coefficients)
        else:
            values = (R.multiply(coefficient, scalar) for coefficient in self.coefficients)
        return self.ring.from_coefficients(values)

    def __mul__(self, other):
        if isinstance(other, GroupRingElement) and other.ring.base_ring == self.ring:
            return other.__rmul__(self)
        if not isinstance(other, GroupRingElement) or other.ring != self.ring:
            try:
                return self.scale(other)
            except TypeError:
                return NotImplemented
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        R = self.ring.base_ring
        values = [R.normalize(R.zero)] * len(self.ring._elements)
        table = self.ring._table
        for i, a in enumerate(self.coefficients):
            if not R.is_zero(a):
                for j, b in enumerate(other.coefficients):
                    if not R.is_zero(b):
                        k = table[i][j]
                        values[k] = R.add(values[k], R.multiply(a, b))
        return self.ring.from_coefficients(values)

    def __rmul__(self, other):
        if not isinstance(other, GroupRingElement) or other.ring != self.ring:
            try:
                return self.scale(other, left=True)
            except TypeError:
                return NotImplemented
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return other * self

    def __pow__(self, exponent):
        exponent = index(exponent)
        if exponent < 0:
            raise ValueError("Only nonnegative powers are supported.")
        result, base = self.ring.one, self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result

    def __bool__(self):
        return any(not self.ring.base_ring.is_zero(a) for a in self.coefficients)

    def __str__(self):
        return " + ".join(f"{a}·[{format_group_label(h)}]"
                          for h, a in self.as_dict().items()) or "0"



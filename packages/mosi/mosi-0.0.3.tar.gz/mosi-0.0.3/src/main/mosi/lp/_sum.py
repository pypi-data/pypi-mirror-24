#!/usr/bin/env python

from decimal import Decimal

from ..common import BaseModel, BaseSum, BaseVariable, CoefficientMap, ConstraintTypes, raise_operand_error
from ._constraint import LinearConstraint


class LinearSum(BaseSum):

    def __init__(self, model, coefficient_map, constant=0):
        self._model = BaseModel.pass_instance(model)
        self._map = CoefficientMap.parse(coefficient_map)
        self._const = float(constant)

    def __iter__(self):
        return iter(self._map)

    def __contains__(self, item):
        return item in self._map

    def __getitem__(self, item):
        return self._map[item]

    def __setitem__(self, key, value):
        self._map[key] = value

    def __pos__(self):
        return self

    def __neg__(self):
        self._multiply(-1)
        self._const *= -1
        return self

    def __add__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._add_constant(other)
        elif isinstance(other, BaseVariable):
            return self._add_variable(other)
        elif isinstance(other, LinearSum):
            return self._add_summation(other)
        else:
            raise_operand_error(self, other, "+")

    def __iadd__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._add_constant(other)
        elif isinstance(other, BaseVariable):
            return self._add_variable(other)
        elif isinstance(other, LinearSum):
            return self._add_summation(other)
        else:
            raise_operand_error(self, other, "+=")

    def __radd__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._add_constant(other)
        elif isinstance(other, BaseVariable):
            return self._add_variable(other)
        elif isinstance(other, LinearSum):
            return self._add_summation(other)
        else:
            raise_operand_error(other, self, "+")

    def __sub__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._add_constant(-other)
        elif isinstance(other, BaseVariable):
            return self._add_variable(other, multiplier=-1)
        elif isinstance(other, LinearSum):
            return self._add_summation(other, multiplier=-1)
        else:
            raise_operand_error(self, other, "-")

    def __isub__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._add_constant(-other)
        elif isinstance(other, BaseVariable):
            return self._add_variable(other, multiplier=-1)
        elif isinstance(other, LinearSum):
            return self._add_summation(other, multiplier=-1)
        else:
            raise_operand_error(other, self, "-=")

    def __rsub__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._add_constant(-other)
        elif isinstance(other, BaseVariable):
            return (-self)._add_variable(other)
        elif isinstance(other, LinearSum):
            return other._add_summation(self, multiplier=-1)
        else:
            raise_operand_error(other, self, "-")

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._multiply(other)
        else:
            # TODO - raise non-linear exception
            raise_operand_error(self, other, "*")

    def __imul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._multiply(other)
        else:
            # TODO - raise non-linear exception
            raise_operand_error(self, other, "*=")

    def __rmul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._multiply(other)
        else:
            # TODO - raise non-linear exception
            raise_operand_error(other, self, "*")

    def __truediv__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._multiply(1 / other)
        else:
            # TODO - raise non-linear exception
            raise_operand_error(other, self, "/")

    def __idiv__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self._multiply(1 / other)
        else:
            # TODO - raise non-linear exception
            raise_operand_error(other, self, "/=")

    def __rdiv__(self, other):
        # TODO - raise non-linear exception
        raise_operand_error(other, self, "/")

    def __eq__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return LinearConstraint(self._model, self._map, other - self._const, ConstraintTypes.EQ)
        elif isinstance(other, BaseVariable):
            return LinearConstraint(self._model, self._map.copy() - other, -self._const, ConstraintTypes.EQ)
        elif isinstance(other, LinearSum):
            return LinearConstraint(self._model, self._map.copy() - other.get_map(), -self._const, ConstraintTypes.EQ)
        else:
            raise_operand_error(other, self, "==")

    def __ge__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return LinearConstraint(self._model, self._map, other - self._const, ConstraintTypes.GE)
        elif isinstance(other, BaseVariable):
            return LinearConstraint(self._model, self._map.copy() - other, -self._const, ConstraintTypes.GE)
        elif isinstance(other, LinearSum):
            return LinearConstraint(self._model, self._map.copy() - other.get_map(), -self._const, ConstraintTypes.GE)
        else:
            raise_operand_error(other, self, "<=")

    def __le__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return LinearConstraint(self._model, self._map, other - self._const, ConstraintTypes.LE)
        elif isinstance(other, BaseVariable):
            return LinearConstraint(self._model, self._map.copy() - other, -self._const, ConstraintTypes.LE)
        elif isinstance(other, LinearSum):
            return LinearConstraint(self._model, self._map.copy() - other.get_map(), -self._const, ConstraintTypes.LE)
        else:
            raise_operand_error(other, self, ">=")

    def _add_constant(self, constant):
        self._const += constant
        return self

    def _add_variable(self, variable, multiplier=1):
        self._map[variable] += multiplier
        return self

    def _add_summation(self, summation, multiplier=1):
        for var in summation:
            self._map[var] += multiplier * summation[var]
        return self._add_constant(multiplier * summation.get_constant())

    def _multiply(self, multiplier):
        for var in self:
            self[var] *= multiplier
        return self

    def get_constant(self):
        return self._const

    @property
    def constant(self):
        return self._const

    def get_map(self):
        return self._map

    @property
    def map(self):
        return self._map

    def get_model(self):
        return self._model

    @property
    def model(self):
        return self._model

    def get_value(self):
        return self._const + sum(variable.get_value() * self[variable] for variable in self)

    @property
    def value(self):
        return self._const + sum(variable.get_value() * self[variable] for variable in self)

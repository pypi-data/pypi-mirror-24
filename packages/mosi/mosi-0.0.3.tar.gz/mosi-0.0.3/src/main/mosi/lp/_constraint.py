#!/usr/bin/env python

from ..common import BaseConstraint, BaseModel, CoefficientMap, ConstraintTypes


class LinearConstraint(BaseConstraint):

    def __init__(self, model, lhs_map, rhs_constant, constraint_type):
        self._model = BaseModel.pass_instance(model)
        self._uid = None

        if float(rhs_constant) < 0:
            self._map = CoefficientMap() - lhs_map
            self._const = -float(rhs_constant)
            self._type = ~ConstraintTypes.parse(constraint_type)

        else:
            self._map = CoefficientMap.parse(lhs_map)
            self._const = float(rhs_constant)
            self._type = ConstraintTypes.parse(constraint_type)

        if self._model.is_auto():
            self._model.add_constraint(self)

    def __contains__(self, item):
        return item in self._map

    def __getitem__(self, item):
        return self._map[item]

    def __iter__(self):
        return iter(self._map)

    def get_constant(self):
        return self._const

    @property
    def constant(self):
        return self._const

    def get_uid(self):
        return self._uid

    @property
    def uid(self):
        return self._uid

    def get_type(self):
        return self._type

    @property
    def type(self):
        return self._type

    def remove(self):
        for variable in self:
            variable.remove_objective()

    def set_uid(self, uid):
        self._uid = uid

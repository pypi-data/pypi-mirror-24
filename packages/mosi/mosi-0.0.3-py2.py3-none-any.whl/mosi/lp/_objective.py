#!/usr/bin/env python

from ..common import ObjectiveTypes
from ._sum import LinearSum


class LinearObjective(LinearSum):

    def __init__(self, model, coefficient_map, constant=0, objective_type="min"):
        super().__init__(model, coefficient_map, constant)
        self._type = ObjectiveTypes.parse(objective_type)

    def __copy__(self):
        return self.__class__(self._model, self._map, self._const, self._type)

    def __invert__(self):
        for variable in self:
            self[variable] = - self[variable]
        self._type = ~self._type
        return self

    def remove(self):
        for variable in self:
            variable.remove_objective()

    def get_type(self):
        return self._type

    @property
    def type(self):
        return self._type

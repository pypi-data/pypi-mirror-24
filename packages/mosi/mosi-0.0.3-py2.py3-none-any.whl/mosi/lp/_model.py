#!/usr/bin/env python

from decimal import Decimal

from ..common import BaseModel, ModelStatus
from ._objective import LinearObjective
from ._sum import LinearSum
from ._variable import DecisionVariable


class Model(BaseModel):

    def __init__(self, name=None, auto=False, error=True):
        self._name = self._parse_model_name(name)
        self._auto = bool(auto)
        self._error = bool(error)
        self._objective = None
        self._constraints = set()
        self._variables = set()
        self._variable_map = dict()
        self._no_variables = 0
        self._status = ModelStatus.UNSOLVED

        self.set_objective(LinearObjective(self, {DecisionVariable(self, name="dummy"): 0}))

    @staticmethod
    def _parse_model_name(name):
        if isinstance(name, str):
            return name
        if isinstance(name, (int, float, Decimal)):
            return "model%s" % name
        else:
            return "model"

    def _remove_variable(self, variable):
        self._variables.remove(variable)
        if variable.has_uid():
            del self._variable_map[variable.get_uid()]

    def add_constraint(self, constraint):
        self._constraints.add(constraint)
        for variable in constraint:
            self._variables.add(variable)
            variable.add_constraint(constraint)

    def add_constraints(self, constraints):
        for constraint in constraints:
            self.add_constraint(constraint)

    def clear(self):
        self._status = ModelStatus.UNSOLVED
        for variable in self._variables:
            variable.clear()

    def get_constraints(self):
        return self._constraints

    @property
    def constraints(self):
        return self._constraints

    def get_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    def get_objective(self):
        return self._objective

    @property
    def objective(self):
        return self._objective

    def get_status(self):
        return self._status

    @property
    def status(self):
        return self._status

    def get_variables(self):
        return self._variables

    @property
    def variables(self):
        return self._variables

    def get_variable(self, key):
        return self._variable_map[key]

    def is_auto(self):
        return self._auto

    def max(self, objective):
        self.set_objective(objective, "max")

    def maximise(self, objective):
        self.set_objective(objective, "max")

    def maximize(self, objective):
        self.set_objective(objective, "max")

    def min(self, objective):
        self.set_objective(objective)

    def minimise(self, objective):
        self.set_objective(objective)

    def minimize(self, objective):
        self.set_objective(objective)

    def parse_variable_name(self, name=None):
        if name is not None:
            return str(name)
        else:
            self._no_variables += 1
            return "x_%s" % self._no_variables

    def remove_constraint(self, constraint):
        self._constraints.remove(constraint)
        for variable in constraint:
            self.remove_variables(variable)
            variable.remove_constraint(constraint)

    def remove_objective(self):
        objective = self._objective
        self._objective = None
        objective.remove()

    def remove_variables(self, variable, safe=True):
        if safe:
            if not variable.is_in_constraint() and not variable.is_in_objective():
                self._remove_variable(variable)
        else:
            self._remove_variable(variable)

    def set_objective(self, objective, objective_type="min"):
        if isinstance(objective, LinearObjective):
            self._objective = objective
        elif isinstance(objective, LinearSum):
            self._objective = LinearObjective(self, objective.get_map(), objective.get_constant(), objective_type)
        elif isinstance(objective, DecisionVariable):
            self._objective = LinearObjective(self, {objective: 1}, objective_type=objective_type)
        elif isinstance(objective, (Decimal, float, int)):
            self._objective = LinearObjective(self, {}, objective)
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception")

        for variable in self._objective:
            variable.set_objective(objective)

    def set_status(self, status):
        self._status = ModelStatus.parse(status)

    def set_variable_key(self, variable, key):
        variable.set_uid(key)
        self._variable_map[key] = variable

    def set_variable_value(self, key, value):
        if key in self._variable_map:
            self._variable_map[key].set_value(value)

    def subject_to(self, *constraints):
        self.add_constraints(constraints)

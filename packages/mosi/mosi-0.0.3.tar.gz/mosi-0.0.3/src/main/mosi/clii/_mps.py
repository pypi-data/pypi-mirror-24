#!/usr/bin/env python
from copy import copy
from io import StringIO

from ..common import BaseObject, BaseEnum, ModelFile, ObjectiveTypes
from ._serializers import IndexSerializer, NumberSerializer


class MpsBoundTypes(BaseEnum):
    LO = "LO"
    UP = "UP"
    FX = "FX"
    FR = "FR"
    MI = "MI"


class MpsFile(ModelFile):

    def __init__(self, model, directory=None, name=None, delete=True):
        super().__init__(model, directory, name, ".mps", delete)


class MpsWriter(BaseObject):

    def __init__(self, index_parser=IndexSerializer(), value_parser=NumberSerializer()):
        self._index_parser = index_parser
        self._value_parser = value_parser
        self._get_model_file = lambda model: MpsFile(model)

    def __call__(self, model):
        model_file = self._get_model_file(model)

        variables_file = StringIO()

        with model_file.write() as file:
            self._write_prefix(file, model)
            self._write_variables(variables_file, model)
            self._write_rows(file, model)
            self._write_columns(file, model)
            self._write_rhs(file, model)
            file.write(variables_file.getvalue())
            self._write_suffix(file)

        variables_file.close()

        return model_file

    @staticmethod
    def _get_bounds(variable):
        bound_format = " %s bound     %s  %s\n"
        bounds = []

        if variable.get_lower_bound() == 0 and variable.get_upper_bound() == float("inf"):
            pass

        elif variable.has_value() or (variable.get_lower_bound() == variable.get_upper_bound()):
            bounds.append(bound_format % (MpsBoundTypes.FX.value, variable.get_uid(), variable.get_value()))

        elif variable.get_lower_bound() >= 0:

            if variable.get_lower_bound() > 0:
                bounds.append(bound_format % (MpsBoundTypes.LO.value, variable.get_uid(), variable.get_lower_bound()))

            if variable.get_upper_bound() < float("inf"):
                bounds.append(bound_format % (MpsBoundTypes.UP.value, variable.get_uid(), variable.get_upper_bound()))

        elif variable.get_upper_bound() <= 0:
            bounds.append(bound_format % (MpsBoundTypes.MI.value, variable.get_uid(), ""))

            if variable.get_lower_bound() > -float("inf"):
                variable.set_lower_bound_constraint()

            if variable.get_upper_bound() < 0:
                variable.set_upper_bound_constraint()

        else:
            bounds.append(bound_format % (MpsBoundTypes.FR.value, variable.get_uid(), ""))

            if variable.get_lower_bound() > -float("inf"):
                variable.set_lower_bound_constraint()

            if variable.get_upper_bound() < float("inf"):
                variable.set_upper_bound_constraint()

        return bounds

    @staticmethod
    def _write_prefix(file, model):
        file.write("NAME          %s\n" % model.get_name())

    @staticmethod
    def _write_suffix(file):
        file.write("ENDATA\n")

    def _write_rows(self, file, model):
        file.write("ROWS\n N  obj\n")

        for (index, constraint) in enumerate(model.get_constraints()):
            constraint.set_uid("c" + self._index_parser(index))
            file.write(" %s  %s\n" % (constraint.get_type().to_mps(), constraint.get_uid()))

    def _write_columns(self, file, model):
        file.write("COLUMNS\n")
        objective = copy(model.get_objective())

        if objective.get_type() == ObjectiveTypes.MAX:
            _ = ~objective
            inverse = True
        else:
            inverse = False

        for (column_index, variable) in enumerate(model.get_variables()):
            key = "x" + self._index_parser(column_index)
            model.set_variable_key(variable, key)

            if variable.is_in_objective():
                new_line = False
                file.write("    %s  obj       %s" % (key, self._value_parser(objective[variable])))
            else:
                new_line = True

            for constraint in variable.get_constraints():
                if new_line:
                    file.write(
                        "    %s  %s  %s" % (key, constraint.get_uid(), self._value_parser(constraint[variable]))
                    )
                    new_line = False

                else:
                    file.write("   %s  %s\n" % (constraint.get_uid(), self._value_parser(constraint[variable])))
                    new_line = True

            if not new_line:
                file.write("\n")

        if inverse:
            _ = ~objective

    def _write_rhs(self, file, model):
        file.write("RHS\n")
        new_line = True

        for (index, constraint) in enumerate(model.get_constraints()):
            if new_line:
                file.write(
                    "    rhs       %s  %s" % (constraint.get_uid(), self._value_parser(constraint.get_constant()))
                )
                new_line = False
            else:
                file.write("   %s  %s\n" % (constraint.get_uid(), self._value_parser(constraint.get_constant())))
                new_line = True

        if not new_line:
            file.write("\n")

    def _write_variables(self, file, model):
        file.write("BOUNDS\n")

        for (index, variable) in enumerate(model.get_variables()):
            index = "x" + self._index_parser(index)
            variable.set_uid(index)
            bounds = self._get_bounds(variable)

            for bound in bounds:
                file.write(bound)

    def set(self, directory=None, name=None, delete=True):
        self._get_model_file = lambda model: MpsFile(model, directory, name, delete)
        return self

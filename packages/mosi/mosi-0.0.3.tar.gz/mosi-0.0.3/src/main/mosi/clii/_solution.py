#!/usr/bin/env python
from xml.etree.ElementTree import parse, ParseError

from ..common import BaseModel, BaseSolutionReader, ModelFile, ModelStatus


class CbcSolutionFile(ModelFile):

    def __init__(self, model, directory=None, name=None, delete=True):
        super().__init__(model, directory, name, ".sol.cbc", delete)


class CplexSolutionFile(ModelFile):

    def __init__(self, model, directory=None, name=None, delete=True):
        super().__init__(model, directory, name, ".sol", delete)


class GlpkSolutionFile(ModelFile):

    def __init__(self, model, directory=None, name=None, delete=True):
        super().__init__(model, directory, name, ".sol.glpk", delete)


class LpSolveSolutionFile(ModelFile):

    def __init__(self, model, directory=None, name=None, delete=True):
        super().__init__(model, directory, name, ".sol.lp", delete)


class TxtSolutionReader(BaseSolutionReader):
    __DELIMITER__ = " "
    __NEWLINE__ = "\n"

    def __call__(self, solution_file):
        if isinstance(self._model, BaseModel):
            solution_file = ModelFile.pass_instance(solution_file)

            with solution_file.read() as file:
                lines = file.readlines()

                for line in lines:
                    self._parse_line(line)

            return self._model

        else:
            # TODO - raise better exception
            raise Exception("raise better exception")

    def _parse_line(self, line):
        pass


class CbcSolutionReader(TxtSolutionReader):
    __STATUS__ = {
        "Optimal": ModelStatus.OPTIMAL,
        "Unbounded": ModelStatus.UNBOUND,
        "Infeasible": ModelStatus.INFEASIBLE
    }

    def _parse_line(self, line):
        cells = line.replace(self.__NEWLINE__, "").split(self.__DELIMITER__)
        cells = [cell for cell in cells if cell != ""]

        try:
            self._model.set_variable_value(self.__KEY_PARSER__(cells[1]), self.__VALUE_PARSER__(cells[2]))
        except (ValueError, IndexError):
            pass

        try:
            self._model.set_status(self._read_status(cells[0]))
        except KeyError:
            pass


class CplexSolutionReader(BaseSolutionReader):
    __STATUS__ = {
        "optimal": ModelStatus.OPTIMAL
    }

    def __call__(self, solution_file):
        if isinstance(self._model, BaseModel):
            solution_file = ModelFile.pass_instance(solution_file)

            try:
                root_node = parse(solution_file.get_path()).getroot()
                for node in root_node:
                    if node.tag == "header":
                        self._model.set_status(self.__KEY_PARSER__(node.attrib["solutionStatusString"]))

                    if node.tag == "variables":
                        for child_node in node:
                            self._parse_node(child_node)
            except ParseError:
                self._model.set_status(ModelStatus.UNDEFINED)

            return self._model

    def _parse_node(self, node):
        attributes = node.attrib
        self._model.set_variable_value(
            self.__KEY_PARSER__(attributes["name"]), self.__VALUE_PARSER__(attributes["value"])
        )


class GlpkSolutionReader(TxtSolutionReader):
    __STATUS__ = {
        "OPTIMAL": ModelStatus.OPTIMAL,
        "UNDEFINED": ModelStatus.UNDEFINED
    }

    def _parse_line(self, line):
        cells = line.replace(self.__NEWLINE__, "").split(self.__DELIMITER__)
        cells = [cell for cell in cells if cell != ""]

        try:
            self._model.set_variable_value(self.__KEY_PARSER__(cells[1]), self.__VALUE_PARSER__(cells[3]))
        except (ValueError, IndexError):
            pass

        try:
            self._model.set_status(self._read_status(self.__KEY_PARSER__(cells[1])))
        except (KeyError, IndexError):
            pass


class LpSolveSolutionReader(TxtSolutionReader):
    __STATUS__ = {
        "Actual values of the variables:": ModelStatus.OPTIMAL,
        "This problem is unbounded": ModelStatus.UNBOUND,
        "This problem is infeasible": ModelStatus.INFEASIBLE
    }

    def _parse_line(self, line):
        cells = line.replace(self.__NEWLINE__, "").split(self.__DELIMITER__)
        cells = [cell for cell in cells if cell != ""]

        try:
            self._model.set_variable_value(self.__KEY_PARSER__(cells[0]), self.__VALUE_PARSER__(cells[1]))
        except (ValueError, IndexError):
            pass

        try:
            self._model.set_status(self._read_status(line.replace(self.__NEWLINE__, "")))
        except (KeyError, IndexError):
            pass

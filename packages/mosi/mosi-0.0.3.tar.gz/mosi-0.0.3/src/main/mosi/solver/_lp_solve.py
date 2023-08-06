#!/usr/bin/env python
from subprocess import Popen

from ..clii import LpSolveSolutionFile, LpSolveSolutionReader, LpsWriter, MpsWriter
from ._base import FileTypes, CliSolver


class LpSolveCliSolver(CliSolver):

    def __init__(self, path, file_type="mps"):
        file_type = FileTypes.parse(file_type, False)

        if file_type == FileTypes.lp:
            super().__init__(path, model_writer=LpsWriter(), solution_reader=LpSolveSolutionReader())
        elif file_type == FileTypes.mps:
            super().__init__(path, "-mps", model_writer=MpsWriter(), solution_reader=LpSolveSolutionReader())
        else:
            super().__init__(path, "-mps", model_writer=MpsWriter(), solution_reader=LpSolveSolutionReader())

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **kwargs):
        self._model_writer.set(directory, name, delete)
        self._solution_reader.set(model)

        model_file = self._model_writer(model)
        solution_file = LpSolveSolutionFile(model, model_file.get_directory(), model_file.get_name(), delete)

        args = [
            self.get_path(), model_file.get_path(),
            *self._cli_args
        ]

        with solution_file.write() as output_file:
            Popen(args, executable=self.get_path(), stdout=output_file).wait()

        self._solution_reader(solution_file)

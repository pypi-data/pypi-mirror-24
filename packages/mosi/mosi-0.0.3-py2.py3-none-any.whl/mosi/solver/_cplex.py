#!/usr/bin/env python
from os import remove

from ..clii import CplexSolutionFile, CplexSolutionReader, LpWriter, MpsWriter
from ._base import FileTypes, CliSolver


class CplexCliSolver(CliSolver):
    def __init__(self, path, file_type="mps"):
        file_type = FileTypes.parse(file_type, False)

        if file_type == FileTypes.lp:
            super().__init__(path, model_writer=LpWriter(), solution_reader=CplexSolutionReader())
        elif file_type == FileTypes.mps:
            super().__init__(path, model_writer=MpsWriter(), solution_reader=CplexSolutionReader())
        else:
            super().__init__(path, model_writer=MpsWriter(), solution_reader=CplexSolutionReader())

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **kwargs):
        self._model_writer.set(directory, name, delete)
        self._solution_reader.set(model)

        model_file = self._model_writer(model)
        solution_file = CplexSolutionFile(model, model_file.get_directory(), model_file.get_name(), delete)

        args = [
            self.get_path(), "-c",
            "read", model_file.get_path(),
            *self._cli_args,
            "optimize",
            "write", solution_file.get_path(), "y",
            "quit"
        ]

        self._run(args, message_callback)
        remove("cplex.log")
        self._solution_reader(solution_file)

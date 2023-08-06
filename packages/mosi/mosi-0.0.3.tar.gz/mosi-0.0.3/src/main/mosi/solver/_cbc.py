#!/usr/bin/env python
from ..clii import CbcSolutionFile, CbcSolutionReader, LpWriter, MpsWriter
from ._base import FileTypes, CliSolver


class CbcCliSolver(CliSolver):

    def __init__(self, path, file_type="mps"):
        file_type = FileTypes.parse(file_type, False)

        if file_type == FileTypes.lp:
            super(CbcCliSolver, self).__init__(path, model_writer=LpWriter(), solution_reader=CbcSolutionReader())
        elif file_type == FileTypes.mps:
            super(CbcCliSolver, self).__init__(path, model_writer=MpsWriter(), solution_reader=CbcSolutionReader())
        else:
            super(CbcCliSolver, self).__init__(path, model_writer=MpsWriter(), solution_reader=CbcSolutionReader())

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **kwargs):
        self._model_writer.set(directory, name, bool(delete))
        self._solution_reader.set(model)

        model_file = self._model_writer(model)
        solution_file = CbcSolutionFile(model, model_file.get_directory(), model_file.get_name(), delete)

        args = [
            self.get_path(), model_file.get_path(),
            *self._cli_args,
            "solve",
            "solu", solution_file.get_path(),
        ]

        self._run(args, message_callback)
        self._solution_reader(solution_file)

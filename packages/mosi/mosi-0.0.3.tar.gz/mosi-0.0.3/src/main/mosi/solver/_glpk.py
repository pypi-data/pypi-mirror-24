#!/usr/bin/env python
from ..clii import GlpkSolutionFile, GlpkSolutionReader, LpWriter, MpsWriter
from ._base import FileTypes, CliSolver


class GlpkCliSolver(CliSolver):
    def __init__(self, path, file_type="mps"):
        file_type = FileTypes.parse(file_type, False)

        if file_type == FileTypes.lp:
            super().__init__(path, "--lp", model_writer=LpWriter(), solution_reader=GlpkSolutionReader())
        elif file_type == FileTypes.mps:
            super().__init__(path, "--mps", model_writer=MpsWriter(), solution_reader=GlpkSolutionReader())
        else:
            super().__init__(path, "--mps", model_writer=MpsWriter(), solution_reader=GlpkSolutionReader())

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **kwargs):
        self._model_writer.set(directory, name, delete)
        self._solution_reader.set(model)

        model_file = self._model_writer(model)
        solution_file = GlpkSolutionFile(model, model_file.get_directory(), model_file.get_name(), delete)

        args = [
            self.get_path(), model_file.get_path(),
            *self._cli_args,
            "--output", solution_file.get_path()
        ]

        self._run(args, message_callback)
        self._solution_reader(solution_file)

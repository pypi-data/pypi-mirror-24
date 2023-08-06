#!/usr/bin/env python
from pathlib import Path
from subprocess import Popen, PIPE

from ..common import BaseEnum, BaseObject


class FileTypes(BaseEnum):
    lp = "lp"
    mps = "mps"


class CliSolver(BaseObject):
    __HELP__ = "-h"

    def __init__(self, path, *args, model_writer=None, solution_reader=None):
        self._solver_path = Path(path)
        self._model_writer = model_writer
        self._solution_reader = solution_reader
        self._cli_args = args

    @staticmethod
    def _run(args, message_callback):
        process = Popen(args, stdout=PIPE, universal_newlines=True)

        while process.poll() is None:
            stdout = process.stdout.readline()
            if stdout != "":
                stdout = stdout.replace("\n", "")
                if stdout != "":
                    message_callback(stdout)

        stdout = process.stdout.readline()
        while stdout != "":
            stdout = stdout.replace("\n", "")
            if stdout != "":
                message_callback(stdout)
            stdout = process.stdout.readline()

    def get_help(self, message_callback=print):
        self._run(self.__HELP__, message_callback)

    def get_path(self):
        return str(self._solver_path.resolve())

    def solve(self, model, directory=None, name=None, delete=True, **kwargs):
        pass

""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pypenelopetools.program import ExecutableProgram
from pypenelopetools.penelope.process import PenelopeMainProcess

# Globals and constants variables.

class PenelopeMainProgram(ExecutableProgram):

    def execute(self, input, index_table, dirpath, *args, **kwargs):
        process = PenelopeMainProcess(self, input, index_table, dirpath)
        process.start()
        return process


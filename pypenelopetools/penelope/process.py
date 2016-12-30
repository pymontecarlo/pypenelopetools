""""""

# Standard library modules.
import os
import io

# Third party modules.

# Local modules.
from pypenelopetools.process import ProgramProcessSubprocessWithInput

# Globals and constants variables.

class PenelopeMainProcess(ProgramProcessSubprocessWithInput):

    def __init__(self, program, input, index_table, dirpath):
        super().__init__(program)
        self.input = input
        self.index_table = index_table
        self.dirpath = dirpath

    def _create_process_kwargs(self):
        kwargs = super()._create_process_kwargs()
        kwargs['cwd'] = self.dirpath
        return kwargs

    def _create_input_lines(self):
        # Write on file
        filepath = os.path.join(self.dirpath, self.input.filename)
        with open(filepath, 'w') as fileobj:
            self.input.write(fileobj, self.index_table)

        # Write in memory
        fileobj = io.StringIO()
        self.input.write(fileobj, self.index_table)
        lines = fileobj.getvalue().splitlines()
        fileobj.close()

        return lines

""""""

# Standard library modules.
import os

# Third party modules.

# Local modules.
from pypenelopetools.program import ExecutableProgram
from pypenelopetools.material.process import MaterialProcess

# Globals and constants variables.

class _MaterialProgram(ExecutableProgram):

    NAME = 'material'

    CONFIG_OPTION_PENDBASE_PATH = 'pendbase_path'

    def __init__(self, executable_path, pendbase_path):
        super().__init__(executable_path)
        self.pendbase_path = pendbase_path

    @classmethod
    def from_config(cls, parser, section):
        cls._check_config(parser, section)

        executable_path = parser.get(section, cls.CONFIG_OPTION_EXECUTABLE_PATH)
        pendbase_path = parser.get(section, cls.CONFIG_OPTION_PENDBASE_PATH)

        return cls(executable_path, pendbase_path)

    def to_config(self, parser, section):
        super().to_config(parser, section)
        parser.set(section, self.CONFIG_OPTION_PENDBASE_PATH, self.pendbase_path)

    def execute(self, material, outdirpath, *args, **kwargs):
        process = MaterialProcess(self, material, outdirpath)
        process.start()
        return process

    @property
    def pendbase_path(self):
        """
        Path to the pendbase folder.
        """
        return self._pendbase_path

    @pendbase_path.setter
    def pendbase_path(self, path):
        if not os.path.exists(path):
            raise ValueError('Path does not exist: {0}'.format(path))
        if not os.path.isdir(path):
            raise ValueError('Path must be a directory: {0}'.format(path))
        self._pendbase_path = path


class Material2014Program(_MaterialProgram):

    VERSION = '2014'


"""
Definition of program
"""

# Standard library modules.
import os
import abc

# Third party modules.

# Local modules.

# Globals and constants variables.

class Program(metaclass=abc.ABCMeta):

    CONFIG_OPTION_NAME = 'name'
    CONFIG_OPTION_VERSION = 'version'

    NAME = None
    VERSION = None

    @classmethod
    def _check_config(cls, parser, section):
        name = parser.get(section, cls.CONFIG_OPTION_NAME)
        if name != cls.NAME:
            raise IOError('Program name does not match: {0} != {1}'
                          .format(name, cls.NAME))

        version = parser.get(section, cls.CONFIG_OPTION_VERSION)
        if version != cls.VERSION:
            raise IOError('Program version does not match: {0} != {1}'
                          .format(version, cls.VERSION))

    @abc.abstractclassmethod
    def from_config(self, parser, section): #pragma: no cover
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, *args, **kwargs): #pragma: no cover
        """
        Starts the program with the specified arguments and returns a 
        :class:`ProgramProcess <pypenelopetools.process.ProgramProcess>`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_config(self, parser, section):
        parser.set(section, self.CONFIG_OPTION_NAME, self.NAME)
        parser.set(section, self.CONFIG_OPTION_VERSION, self.VERSION)

class ExecutableProgram(Program):

    CONFIG_OPTION_EXECUTABLE_PATH = 'executable_path'

    def __init__(self, executable_path):
        self.executable_path = executable_path

    @classmethod
    def from_config(cls, parser, section):
        cls._check_config(parser, section)

        executable_path = parser.get(section, cls.CONFIG_OPTION_EXECUTABLE_PATH)

        return cls(executable_path)

    def to_config(self, parser, section):
        super().to_config(parser, section)
        parser.set(section, self.CONFIG_OPTION_EXECUTABLE_PATH, self.executable_path)

    @property
    def executable_path(self):
        """
        Path to program executable.
        """
        return self._executable_path

    @executable_path.setter
    def executable_path(self, path):
        if not os.path.exists(path):
            raise ValueError('Path does not exist: {0}'.format(path))
        if not os.access(path, os.X_OK):
            raise ValueError('Program is not executable: {0}'.format(path))
        self._executable_path = path

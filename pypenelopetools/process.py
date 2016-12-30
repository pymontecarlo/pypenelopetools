"""
Definition of a program process
"""

# Standard library modules.
import os
import abc
import sys
import subprocess
import threading
import tempfile
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.

# Globals and constants variables.

class ProgramProcess(metaclass=abc.ABCMeta):

    def __init__(self, program):
        self._program = program

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError

    @abc.abstractmethod
    def join(self):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError

    @abc.abstractmethod
    def is_running(self):
        raise NotImplementedError

    @abc.abstractproperty
    def progress(self):
        raise NotImplementedError

    @abc.abstractproperty
    def status(self):
        raise NotImplementedError

    @property
    def program(self):
        return self._program

def _parse_process_stdout(process, callback):
    with process:
        for line in iter(process.stdout.readline, b""):
            line = line.decode('ascii').rstrip()
            callback(line)

class ProgramProcessSubprocess(ProgramProcess):

    def __init__(self, program):
        super().__init__(program)
        self._process = None
        self._progress = 0.0
        self._status = ""

    def _create_process_args(self):
        return (self.program.executable_path,)

    def _create_process_kwargs(self):
        kwargs = {}

        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            kwargs['startupinfo'] = startupinfo

        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT

        return kwargs

    def _create_process(self):
        args = self._create_process_args()
        kwargs = self._create_process_kwargs()

        logger.debug('args: %s' % subprocess.list2cmdline(args))
        process = subprocess.Popen(*args, **kwargs)

        return process

    def _parse_stdout(self, line):
        logger.debug(line)
        self._status = line

    def _join_process(self):
        self._process.wait()
        return self._process.returncode

    def start(self):
        if self._process is not None:
            raise RuntimeError('Process already running. Call join()')

        self._progress = 0.0

        self._process = self._create_process()

        thread = threading.Thread(target=_parse_process_stdout,
                                  args=(self._process, self._parse_stdout))
        thread.start()

    def join(self):
        returncode = self._join_process()
        self._process = None
        self._progress = 1.0
        logger.debug('returncode: %s' % returncode)
        return returncode

    def stop(self):
        if self._process is not None:
            self._process.kill()
        self._progress = 0.0
        self._status = ""

    def is_running(self):
        if self._process is None:
            return False
        return self._process.poll() is None

    @property
    def progress(self):
        return self._progress

    @property
    def status(self):
        return self._status

class ProgramProcessSubprocessWithInput(ProgramProcessSubprocess):

    def __init__(self, program):
        super().__init__(program)
        self._input_file = None

    def _create_process_kwargs(self):
        kwargs = super()._create_process_kwargs()

        self._input_file = self._create_input_file()
        kwargs['stdin'] = self._input_file

        return kwargs

    def _create_input_file(self):
        input_file = tempfile.TemporaryFile()

        lines = self._create_input_lines()
        input_file.write(os.linesep.join(lines).encode('ascii'))

        input_file.seek(0)

        return input_file

    @abc.abstractmethod
    def _create_input_lines(self):
        raise NotImplementedError

    def _join_process(self):
        returncode = super()._join_process()
        self._input_file.close()
        return returncode

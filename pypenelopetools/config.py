"""
Configuration of pyPENELOPEtools
"""

# Standard library modules.
import os
import configparser
import importlib
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.

# Globals and constants variables.

class Configuration:

    def __init__(self):
        self._programs = {}

    def _resolve_program(self, parser, section):
        modulename, classname = section.split(":")

        module = importlib.import_module(modulename)
        clasz = getattr(module, classname)

        return clasz.from_config(parser, section)

    def read(self, fileobj):
        self.clear_programs()

        parser = configparser.ConfigParser()
        parser.read_file(fileobj)

        for section in parser.sections():
            try:
                program = self._resolve_program(parser, section)
            except:
                logger.exception('Could not import {0}'.format(section))
            else:
                self.add_program(program)

    def write(self, fileobj):
        parser = configparser.ConfigParser()

        for program in self.get_programs():
            section = '{0}:{1}'.format(program.__module__,
                                       program.__class__.__name__)
            parser.add_section(section)
            program.to_config(parser, section)

        parser.write(fileobj)

    def add_program(self, program):
        name = program.NAME
        version = program.VERSION
        if (name, version) in self._programs:
            raise ValueError('Program already added')
        self._programs[(name, version)] = program

    def remove_program(self, program):
        self._programs.pop((program.NAME, program.VERSION))

    def clear_programs(self):
        self._programs.clear()

    def get_programs(self):
        return tuple(self.get_program(name, version)
                     for name, version in sorted(self._programs))

    def get_program(self, name, version=None):
        if version is not None:
            try:
                return self._programs[(name, version)]
            except KeyError:
                raise ValueError('Could not find program {0} with version {1}'
                                 .format(name, version))

        else:
            programs = [(v, program) for (n, v), program in self._programs.items()
                        if n == name]
            if not programs:
                raise ValueError('Could not find program {0}'.format(name))

            programs.sort()
            return programs[0]

    def has_program(self, name, version):
        try:
            self.get_program(name, version)
            return True
        except ValueError:
            return False

def get_configuration(develop=False):
    """
    Search for the configuration file
    """
    config = Configuration()

    if develop:
        filepath = os.path.join(os.path.dirname(__file__),
                                '..', 'pypenelopetools.cfg')
    else:
        filepath = os.path.join(os.path.expanduser('~'),
                                '.pypenelopetools', 'pypenelopetools.cfg')

    if os.path.exists(filepath):
        with open(filepath, 'r') as fp:
            config.read(fp)

    return config



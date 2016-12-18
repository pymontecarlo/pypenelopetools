#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import tempfile
import shutil

# Third party modules.

# Local modules.
from pypenelopetools.config import Configuration
from pypenelopetools.program import Program

# Globals and constants variables.

class MockProgram(Program):

    NAME = 'mock'
    VERSION = '1.0'

    @classmethod
    def from_config(cls, parser, section):
        return cls()

    def to_config(self, parser, section):
        super().to_config(parser, section)

    def execute(self, *args, **kwargs):
        pass

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.config = Configuration()
        self.config.add_program(MockProgram())

        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def testwrite(self):
        filepath = os.path.join(self.tmpdir, 'pypenelopetools.cfg')
        with open(filepath, 'w') as fp:
            self.config.write(fp)

    def testread(self):
        filepath = os.path.join(self.tmpdir, 'pypenelopetools.cfg')
        with open(filepath, 'w') as fp:
            self.config.write(fp)

        with open(filepath, 'r') as fp:
            self.config.read(fp)

        programs = list(self.config.get_programs())
        self.assertEqual(1, len(programs))
        self.assertEqual('mock', programs[0].NAME)
        self.assertEqual('1.0', programs[0].VERSION)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()

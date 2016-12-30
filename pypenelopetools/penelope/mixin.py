""""""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class FilenameMixin:

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if len(filename) > 20:
            raise ValueError("Filename is too long. Maximum 20 characters")
        self._filename = filename

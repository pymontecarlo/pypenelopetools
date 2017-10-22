""""""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

FILENAME_MAXLENGTH = 20

class FilenameMixin:

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if len(filename) > FILENAME_MAXLENGTH:
            raise ValueError("Filename is too long. Maximum {0} characters"
                             .format(FILENAME_MAXLENGTH))
        self._filename = filename

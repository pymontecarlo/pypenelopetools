""""""

# Standard library modules.
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.

# Globals and constants variables.

class LineIterator(object):
    """
    Based on more_itertools.peekable
    """

    _marker = object()

    def __init__(self, iterable):
        self._it = iter(iterable)

    def __iter__(self):
        return self

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def peek(self, default=_marker):
        if not hasattr(self, '_peek'):
            try:
                self._peek = next(self._it)

                while self._peek.startswith(' ' * 7):
                    self._peek = next(self._it)

            except StopIteration:
                if default is self._marker:
                    raise
                return default

        return self._peek

    def __next__(self):
        ret = self.peek()
        del self._peek
        return ret

class PenelopeInput:

    def read(self, fileobj):
        line_iterator = LineIterator(fileobj)

        for keyword in self.get_keywords():
            line = line_iterator.peek().rstrip()
            success = keyword.read(line_iterator)
            if success:
                logger.debug('Parsed "{0}"'.format(line))

    def write(self, fileobj, index_table):
        lines = []
        for keyword in self.get_keywords():
            lines += keyword.write(index_table)

        fileobj.write('\n'.join(lines))

    def get_keywords(self):
        return []

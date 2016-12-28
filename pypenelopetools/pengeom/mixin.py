""""""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class DescriptionMixin(object):

    @property
    def description(self):
        """
        Description of the surface.
        """
        return self._description

    @description.setter
    def description(self, desc):
        self._description = desc

class ModuleMixin(object):

    def add_module(self, module):
        if module == self:
            raise ValueError("Cannot add this module to this module.")
        self._modules.add(module)

    def pop_module(self, module):
        self._modules.discard(module)

    def clear_modules(self):
        self._modules.clear()

    def get_modules(self):
        return list(self._modules)
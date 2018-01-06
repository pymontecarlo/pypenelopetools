"""
Mixins used to create geometry objects.
"""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class DescriptionMixin(object):
    """
    Mixin that adds a description property.
    """

    @property
    def description(self):
        """str: Description of the geometry object."""
        return self._description

    @description.setter
    def description(self, desc):
        self._description = desc

class ModuleMixin(object):
    """
    Mixin that adds methods to add, pop and clear modules.
    """

    def add_module(self, module):
        """
        Adds a module.
        
        Args:
            module (:obj:`Module <pypenelopetools.pengeom.module.Module>`):
                Module to add.
        """
        if module == self:
            raise ValueError("Cannot add this module to this module.")
        self._modules.add(module)

    def pop_module(self, module):
        """
        Removes a module.
        
        Args:
            module (:obj:`Module <pypenelopetools.pengeom.module.Module>`):
                Module to remove.
        """
        self._modules.discard(module)

    def clear_modules(self):
        """
        Clear all modules.
        """
        self._modules.clear()

    def get_modules(self):
        """
        Returns:
            tuple: All modules.
        """
        return tuple(self._modules)
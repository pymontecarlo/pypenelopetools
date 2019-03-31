""""""

# Standard library modules.
import enum

# Third party modules.

# Local modules.

# Globals and constants variables.

class KPAR(enum.IntEnum):
    USER_DEFINED = 0
    ELECTRON = 1
    PHOTON = 2
    POSITRON = 3

    def __str__(self):
        return self.name.replace('_', ' ').lower()

class ICOL(enum.IntEnum):
    ARTIFICIAL_SOFT_EVENT = 1 # random hinge
    COHERENT_SCATTERING = 1 # Rayleigh
    HARD_ELASTIC = 2
    INCOHERENT_SCATTERING = 2 # Compton
    HARD_INELASTIC = 3
    PHOTOELECTRIC_ABSORPTION = 3
    HARD_BREMSSTRAHLUNG_EMISSION = 4
    ELECTRON_POSITRON_PAIR_PRODUCTION = 4
    INNER_SHELL_IMPACT_IONISATION = 5
    DELTA_INTERACTION = 7
    AUXILIARY_INTERACTION = 8

    def __str__(self):
        return self.name.replace('_', ' ').lower()

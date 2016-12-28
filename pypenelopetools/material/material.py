"""
Definition of material
"""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class Material:

    def __init__(self, name, composition, density_g_per_cm3,
                 mean_excitation_energy_eV=None,
                 oscillator_strength_fcb=None,
                 oscillator_energy_wcb_eV=None):
        self.name = name
        self.filename = name[:20]
        self.composition = composition.copy()
        self.density_g_per_cm3 = float(density_g_per_cm3)
        self.mean_excitation_energy_eV = mean_excitation_energy_eV
        self.oscillator_strength_fcb = oscillator_strength_fcb
        self.oscillator_energy_wcb_eV = oscillator_energy_wcb_eV

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if len(filename) > 20:
            raise ValueError("Filename is too long. Maximum 20 characters")
        self._filename = filename

VACUUM = Material("Vacuum", {}, 0.0)

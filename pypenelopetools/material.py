"""
Definition of material
"""

# Standard library modules.
import os

# Third party modules.
import pyxray

# Local modules.
from pypenelopetools.penelope.mixin import FilenameMixin

# Globals and constants variables.

class Material(FilenameMixin):

    def __init__(self, name, composition, density_g_per_cm3,
                 mean_excitation_energy_eV=None,
                 oscillator_strength_fcb=None,
                 oscillator_energy_wcb_eV=None):
        self.name = name
        self.filename = name[:16] + '.mat'
        self.composition = composition.copy()
        self.density_g_per_cm3 = float(density_g_per_cm3)
        self.mean_excitation_energy_eV = mean_excitation_energy_eV
        self.oscillator_strength_fcb = oscillator_strength_fcb
        self.oscillator_energy_wcb_eV = oscillator_energy_wcb_eV

    def __repr__(self):
        return '<{0}({1})>'.format(self.__class__.__name__, self.name)

    @classmethod
    def read_input(cls, fileobj):
        """
        Reads the input file created by this class 
        (see :meth:`write_input <.Material.write_input>`).
        
        :arg fileobj: file object opened with read access
        """
        composition_option = fileobj.readline().strip()
        assert composition_option == "1"

        name = fileobj.readline().strip()

        element_count = int(fileobj.readline())
        if element_count == 1:
            z = int(fileobj.readline())
            composition = {z: 1.0}
        else:
            wf_option = fileobj.readline().strip()
            assert wf_option == "2"

            composition = {}
            for _ in range(element_count):
                z, wf = fileobj.readline().split()
                composition[int(z)] = float(wf)

        mean_excitation_option = fileobj.readline().strip()
        if mean_excitation_option == "1":
            mean_excitation_energy_eV = float(fileobj.readline())
        else:
            mean_excitation_energy_eV = None

        density_g_per_cm3 = float(fileobj.readline())

        oscillator_option = fileobj.readline().strip()
        if oscillator_option == "1":
            oscillator_strength_fcb, oscillator_energy_wcb_eV = map(float, fileobj.readline().split())
        else:
            oscillator_strength_fcb = oscillator_energy_wcb_eV = None

        filename = fileobj.readline()

        material = cls(name, composition, density_g_per_cm3,
                       mean_excitation_energy_eV,
                       oscillator_strength_fcb,
                       oscillator_energy_wcb_eV)
        material.filename = filename

        return material

    @classmethod
    def read_material(cls, fileobj):
        """
        Reads a PENELOPE generated material file (.mat).
        
        :arg fileobj: file object opened with read access
        """
        first_line = fileobj.readline().strip()
        assert first_line[:8] == 'PENELOPE'

        line = fileobj.readline()
        _label, value = line.split()
        name = value.strip()

        line = fileobj.readline()
        _label, value = line.split('=')
        value, _unit = value.split()
        density_g_per_cm3 = float(value)

        line = fileobj.readline()
        _label, value = line.split('=')
        element_count = int(value)

        composition = {}
        totalatomicmass = 0.0
        for _ in range(element_count):
            line = fileobj.readline()
            part_z, part_af = line.split(',')

            _label, value = part_z.split('=')
            z = int(value)

            _label, value = part_af.split('=')
            atomicfraction = float(value)
            atomicmass = atomicfraction * pyxray.element_atomic_weight(z)

            composition[z] = atomicmass
            totalatomicmass += atomicmass

        for z, atomicmass in composition.items():
            composition[z] = atomicmass / totalatomicmass

        line = fileobj.readline()
        _label, value = line.split('=')
        value, _unit = value.split()
        mean_excitation_energy_eV = float(value)

        line = fileobj.readline()
        label, _value = line.split('=')
        assert label.strip() == 'Number of oscillators'

        line = fileobj.readline()
        _, value1, _, value2, _, _ = line.split()
        oscillator_strength_fcb = float(value1)
        oscillator_energy_wcb_eV = float(value2)

        return cls(name, composition, density_g_per_cm3,
                   mean_excitation_energy_eV,
                   oscillator_strength_fcb,
                   oscillator_energy_wcb_eV)

    def _create_lines(self):
        """
        Creates the lines of the input file of the material program.
    
        :arg material: definition of the material
        :type material: :class:`.Material`
        """
        lines = []

        elements_count = len(self.composition)
        density = self.density_g_per_cm3

        # Select the manual composition option.
        lines.append("1")

        # Material name.
        lines.append(str(self.name))

        lines.append(str(elements_count))

        # Case more than one element.
        if elements_count > 1:
            lines.append("2") # Select weight fraction option.

            for z, wf in self.composition.items():
                lines.append('{0:d} {1:.4f}'.format(z, wf))

        elif elements_count == 1:
            z = list(self.composition.keys())[0]
            lines.append('{0:d}'.format(z))

        else:
            raise ValueError("No elements are defined in the material.")

        # Mean excitation energy.
        if self.mean_excitation_energy_eV is not None:
            lines.append("1")
            lines.append("{0:f}".format(self.mean_excitation_energy_eV))
        else:
            lines.append("2")

        # Density
        lines.append("{0:f}".format(density))

        # Fcb and Wcb values.
        if self.oscillator_strength_fcb is not None and \
                self.oscillator_energy_wcb_eV is not None:
            lines.append("1")
            lines.append("{0:f} {1:f}".format(self.oscillator_strength_fcb,
                                              self.oscillator_energy_wcb_eV))
        else:
            lines.append("2")

        # set the name and path of the output file.
        lines.append(self.filename)

        return lines

    def write_input(self, fileobj):
        """
        Writes the input file to create this material.
        The material program should be called with this input file as standard input::
        
            material.exe < material.in
        
        :arg fileobj: file object opened with write access
        """
        lines = self._create_lines()
        fileobj.write(os.linesep.join(lines))

VACUUM = Material('Vacuum', {}, 0.0)

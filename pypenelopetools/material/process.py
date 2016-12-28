"""
Process to run material program
"""

# Standard library modules.
import os
import tempfile
import shutil

# Third party modules.

# Local modules.
from pypenelopetools.process import ProgramProcessSubprocess

# Globals and constants variables.

def _create_input_lines(material):
    """
    Creates the lines of the input file of the material program.

    :arg material: definition of the material
    :type material: :class:`.Material`
    """
    lines = []

    elements_count = len(material.composition)
    density = material.density_g_per_cm3

    # Select the manual composition option.
    lines.append("1")

    # Material name.
    lines.append(str(material.name))

    lines.append(str(elements_count))

    # Case more than one element.
    if elements_count > 1:
        lines.append("2") # Select weight fraction option.

        for z, wf in material.composition.items():
            lines.append('{0:d} {1:.4f}'.format(z, wf))

    elif elements_count == 1:
        z = list(material.composition.keys())[0]
        lines.append('{0:d}'.format(z))

    else:
        raise ValueError("No elements are defined in the material.")

    # Mean excitation energy.
    if material.mean_excitation_energy_eV is not None:
        lines.append("1")
        lines.append("{0:f}".format(material.mean_excitation_energy_eV))
    else:
        lines.append("2")

    lines.append("{0:f}".format(density))

    # Fcb and Wcb values.
    if material.oscillator_strength_fcb is not None and \
            material.oscillator_energy_wcb_eV is not None:
        lines.append("1")
        lines.append("{0:f} {1:f}".format(material.oscillator_strength_fcb,
                                          material.oscillator_energy_wcb_eV))
    else:
        lines.append("2")

    # set the name and path of the output file.
    lines.append(material.filename)

    return lines

class MaterialProgramProcess(ProgramProcessSubprocess):

    def __init__(self, program, material, outdirpath):
        super().__init__(program)
        self.material = material
        self.outdirpath = outdirpath
        self._input_file = None

    def _create_process_args(self):
        return (self.program.executable_path,)

    def _create_process_kwargs(self):
        kwargs = super()._create_process_kwargs()

        kwargs['cwd'] = self.program.pendbase_path

        self._input_file = self._create_input_file()
        kwargs['stdin'] = self._input_file

        return kwargs

    def _create_input_file(self):
        """
        Creates the input file for the material program.

        :arg material: definition of the material
        :type material: :class:`.Material`
        """
        input_file = tempfile.TemporaryFile()

        lines = _create_input_lines(self.material)
        input_file.write('\n'.join(lines).encode('ascii'))

        input_file.seek(0)

        return input_file

    def _join_process(self):
        returncode = super()._join_process()

        self._input_file.close()

        # Move file from pendbase directory to use outfilepath
        filename = self.material.filename
        src = os.path.join(self.program.pendbase_path, filename)
        dst = os.path.join(self.outdirpath, filename)
        shutil.move(src, dst)

        return returncode

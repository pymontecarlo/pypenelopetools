""""""

# Standard library modules.
import os

# Third party modules.
from uncertainties import ufloat

# Local modules.
from pypenelopetools.penelope.result import _PenelopeResultBase

# Globals and constants variables.

class PenepmaResult(_PenelopeResultBase):

    def __init__(self):
        self.simulation_time_s = ufloat(0.0, 0.0)
        self.simulation_speed_1_per_s = ufloat(0.0, 0.0)
        self.simulated_primary_showers = ufloat(0.0, 0.0)

        self.upbound_primary_particles = ufloat(0.0, 0.0)
        self.downbound_primary_particles = ufloat(0.0, 0.0)
        self.absorbed_primary_particles = ufloat(0.0, 0.0)

        self.upbound_fraction = ufloat(0.0, 0.0)
        self.downbound_fraction = ufloat(0.0, 0.0)
        self.absorbed_fraction = ufloat(0.0, 0.0)

        self.upbound_secondary_electron_generation_probabilities = ufloat(0.0, 0.0)
        self.downbound_secondary_electron_generation_probabilities = ufloat(0.0, 0.0)
        self.absorbed_secondary_electron_generation_probabilities = ufloat(0.0, 0.0)
        self.upbound_secondary_photon_generation_probabilities = ufloat(0.0, 0.0)
        self.downbound_secondary_photon_generation_probabilities = ufloat(0.0, 0.0)
        self.absorbed_secondary_photon_generation_probabilities = ufloat(0.0, 0.0)
        self.upbound_secondary_positron_generation_probabilities = ufloat(0.0, 0.0)
        self.downbound_secondary_positron_generation_probabilities = ufloat(0.0, 0.0)
        self.absorbed_secondary_positron_generation_probabilities = ufloat(0.0, 0.0)

        self.average_deposited_energy_eV = {}
        self.average_photon_energy_eV = {}

        self.last_random_seed1 = ufloat(0.0, 0.0)
        self.last_random_seed2 = ufloat(0.0, 0.0)

        self.reference_line_uncertainty = ufloat(0.0, 0.0)

    def read(self, fileobj):
        line = self._read_until_line_startswith(fileobj, 'Simulation time')
        val, = self._read_all_values(line)
        self.simulation_time_s = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, 'Simulation speed')
        val, = self._read_all_values(line)
        self.simulation_speed_1_per_s = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, 'Simulated primary showers')
        val, = self._read_all_values(line)
        self.simulated_primary_showers = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, 'Upbound primary particles')
        val, = self._read_all_values(line)
        self.upbound_primary_particles = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, 'Downbound primary particles')
        val, = self._read_all_values(line)
        self.downbound_primary_particles = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, 'Absorbed primary particles')
        val, = self._read_all_values(line)
        self.absorbed_primary_particles = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, 'Upbound fraction')
        val, unc = self._read_all_values(line)
        self.upbound_fraction = ufloat(val, unc / 3.0)

        line = self._read_until_line_startswith(fileobj, 'Downbound fraction')
        val, unc = self._read_all_values(line)
        self.downbound_fraction = ufloat(val, unc / 3.0)

        line = self._read_until_line_startswith(fileobj, 'Absorption fraction')
        val, unc = self._read_all_values(line)
        self.absorbed_fraction = ufloat(val, unc / 3.0)

        self._read_until_line_startswith(fileobj, 'Secondary-particle generation probabilities')
        fileobj.readline() # skip header
        fileobj.readline() # skip header

        fileobj.readline() # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.upbound_secondary_electron_generation_probabilities = ufloat(val_el, unc_el / 3.0)
        self.upbound_secondary_photon_generation_probabilities = ufloat(val_ph, unc_ph / 3.0)
        self.upbound_secondary_positron_generation_probabilities = ufloat(val_po, unc_po / 3.0)

        fileobj.readline() # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.downbound_secondary_electron_generation_probabilities = ufloat(val_el, unc_el / 3.0)
        self.downbound_secondary_photon_generation_probabilities = ufloat(val_ph, unc_ph / 3.0)
        self.downbound_secondary_positron_generation_probabilities = ufloat(val_po, unc_po / 3.0)

        fileobj.readline() # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.absorbed_secondary_electron_generation_probabilities = ufloat(val_el, unc_el / 3.0)
        self.absorbed_secondary_photon_generation_probabilities = ufloat(val_ph, unc_ph / 3.0)
        self.absorbed_secondary_positron_generation_probabilities = ufloat(val_po, unc_po / 3.0)

        self._read_until_line_startswith(fileobj, 'Average deposited energies (bodies)')
        line = fileobj.readline().strip()
        while line.startswith('Body'):
            body = int(line[5:9])
            val, unc, _effic = self._read_all_values(line)
            self.average_deposited_energy_eV[body] = ufloat(val, unc / 3.0)
            line = fileobj.readline().strip()

        self._read_until_line_startswith(fileobj, 'Average photon energy at the detectors')
        line = fileobj.readline().strip()
        while line.startswith('Detector'):
            detector = int(line[10:12])
            val, unc, _effic = self._read_all_values(line)
            self.average_photon_energy_eV[detector] = ufloat(val, unc / 3.0)
            line = fileobj.readline().strip()

        line = self._read_until_line_startswith(fileobj, 'Last random seeds')
        seed1, seed2 = map(int, line.split('=')[1].split(','))
        self.last_random_seed1 = ufloat(seed1, 0.0)
        self.last_random_seed2 = ufloat(seed2, 0.0)

        try:
            self._read_until_line_startswith(fileobj, 'Reference line')
            val, = self._read_all_values(fileobj.readline())
            self.reference_line_uncertainty = ufloat(val, 0.0)
        except IOError:
            self.reference_line_uncertainty = ufloat(0.0, 0.0)

    def read_directory(self, dirpath):
        filepath = os.path.join(dirpath, 'penepma-res.dat')
        with open(filepath, 'r') as fp:
            self.read(fp)

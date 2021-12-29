"""
Results of PENEPMA simulation.
"""

# Standard library modules.
import os

# Third party modules.
from uncertainties import ufloat, unumpy
import numpy as np
import pyxray

# Local modules.
from pypenelopetools.penelope.result import PenelopeResultBase
from pypenelopetools.penelope.enums import KPAR

# Globals and constants variables.


class PencylResult(PenelopeResultBase):
    """
    Results from ``pencyl-res.dat``.

    .. note::
       All results are expressed using the
       `uncertainties <https://pythonhosted.org/uncertainties>`_ package.
       The nominal value can be accessed with the property ``nominal_value`` or
       the abbreviation ``n``, whereas the standard deviation (1-sigma), with
       the property ``std_dev`` or ``s``.
       For example::

           result.simulation_time_s.n #-> 100.0
           result.simulation_time_s.s #-> 0.0

    Attributes:
        simulation_time_s (ufloat):
            Simulation time in seconds.
        simulation_speed_1_per_s (ufloat):
            Simulation speed in simulation per second.
        simulated_primary_showers (ufloat):
            Number of primary showers simulated.

        upbound_primary_particles (ufloat):
            Number of primary particles that exited the geometry upwards.
        downbound_primary_particles (ufloat):
            Number of primary particles that exited the geometry downwards.
        absorbed_primary_particles (ufloat):
            Number of primary particles that were absorbed within the geometry.

        upbound_fraction (ufloat):
            Fraction of primary particles that exited the geometry upwards.
        downbound_fraction (ufloat):
            Fraction of primary particles that exited the geometry downwards.
        absorbed_fraction (ufloat):
            Fraction of primary particles that were absorbed within the geometry.

        upbound_secondary_electron_generation_probabilities (ufloat):
            Probability of second generation electrons exited the geometry upwards.
        downbound_secondary_electron_generation_probabilities (ufloat):
            Probability of second generation electrons exited the geometry downwards.
        absorbed_secondary_electron_generation_probabilities (ufloat):
            Probability of second generation electrons absorbed within the geometry.
        upbound_secondary_photon_generation_probabilities (ufloat):
            Probability of second generation photons exited the geometry upwards.
        downbound_secondary_photon_generation_probabilities (ufloat):
            Probability of second generation photons exited the geometry downwards.
        absorbed_secondary_photon_generation_probabilities (ufloat):
            Probability of second generation photons absorbed within the geometry.
        upbound_secondary_positron_generation_probabilities (ufloat):
            Probability of second generation positrons exited the geometry upwards.
        downbound_secondary_positron_generation_probabilities (ufloat):
            Probability of second generation positrons exited the geometry downwards.
        absorbed_secondary_positron_generation_probabilities (ufloat):
            Probability of second generation positrons absorbed within the geometry.

        average_body_deposited_energy_eV (dict(int, ufloat)):
            Average deposited energy in each body.
            Dictionary where keys are indexes of body and
            values, the average deposited energy in eV.
        average_detector_deposited_energy_eV (dict(int, ufloat)):
            Average deposited energy in each energy detector.
            Dictionary where keys are indexes of energy detector and
            values, the average deposited energy in eV.

        last_random_seed1 (ufloat):
            Last first seed of the random number generator.
        last_random_seed2 (ufloat):
            Last second seed of the random number generator.
    """

    _PARTICLE_LOOKUP = {
        "electrons": KPAR.ELECTRON,
        "photos": KPAR.PHOTON,
        "positrons": KPAR.POSITRON,
    }

    def __init__(self):
        super().__init__()

        self.simulation_time_s = ufloat(0.0, 0.0)
        self.simulation_speed_1_per_s = ufloat(0.0, 0.0)
        self.simulated_primary_showers = ufloat(0.0, 0.0)
        self.primary_particle = None

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

        self.average_body_deposited_energy_eV = {}
        self.average_detector_deposited_energy_eV = {}

        self.last_random_seed1 = ufloat(0.0, 0.0)
        self.last_random_seed2 = ufloat(0.0, 0.0)

    def read(self, fileobj):
        line = self._read_until_line_startswith(fileobj, "Simulation time")
        (val,) = self._read_all_values(line)
        self.simulation_time_s = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, "Simulation speed")
        (val,) = self._read_all_values(line)
        self.simulation_speed_1_per_s = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, "Simulated primary particles")
        (val,) = self._read_all_values(line)
        self.simulated_primary_showers = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, "Primary particles")
        particle = line.split(":")[1].strip()
        self.primary_particle = self._PARTICLE_LOOKUP.get(particle)

        line = self._read_until_line_startswith(fileobj, "Upbound primary particles")
        (val,) = self._read_all_values(line)
        self.upbound_primary_particles = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, "Downbound primary particles")
        (val,) = self._read_all_values(line)
        self.downbound_primary_particles = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, "Absorbed primary particles")
        (val,) = self._read_all_values(line)
        self.absorbed_primary_particles = ufloat(val, 0.0)

        line = self._read_until_line_startswith(fileobj, "Upbound fraction")
        val, unc = self._read_all_values(line)
        self.upbound_fraction = ufloat(val, unc / 3)

        line = self._read_until_line_startswith(fileobj, "Downbound fraction")
        val, unc = self._read_all_values(line)
        self.downbound_fraction = ufloat(val, unc / 3)

        line = self._read_until_line_startswith(fileobj, "Absorption fraction")
        val, unc = self._read_all_values(line)
        self.absorbed_fraction = ufloat(val, unc / 3)

        self._read_until_line_startswith(
            fileobj, "Secondary-particle generation probabilities"
        )
        fileobj.readline()  # skip header
        fileobj.readline()  # skip header

        fileobj.readline()  # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.upbound_secondary_electron_generation_probabilities = ufloat(
            val_el, unc_el / 3
        )
        self.upbound_secondary_photon_generation_probabilities = ufloat(
            val_ph, unc_ph / 3
        )
        self.upbound_secondary_positron_generation_probabilities = ufloat(
            val_po, unc_po / 3
        )

        fileobj.readline()  # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.downbound_secondary_electron_generation_probabilities = ufloat(
            val_el, unc_el / 3
        )
        self.downbound_secondary_photon_generation_probabilities = ufloat(
            val_ph, unc_ph / 3
        )
        self.downbound_secondary_positron_generation_probabilities = ufloat(
            val_po, unc_po / 3
        )

        fileobj.readline()  # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.absorbed_secondary_electron_generation_probabilities = ufloat(
            val_el, unc_el / 3
        )
        self.absorbed_secondary_photon_generation_probabilities = ufloat(
            val_ph, unc_ph / 3
        )
        self.absorbed_secondary_positron_generation_probabilities = ufloat(
            val_po, unc_po / 3
        )

        self.average_body_deposited_energy_eV.clear()
        self._read_until_line_startswith(
            fileobj, "Average deposited energies (per primary shower)"
        )
        fileobj.readline()  # skip header
        line = fileobj.readline().strip()
        while line:  # until empty line
            body = int(line[:4])
            val, unc, _effic = self._read_all_values(line)
            self.average_body_deposited_energy_eV[body] = ufloat(val, unc / 3)
            line = fileobj.readline().strip()

        self.average_detector_deposited_energy_eV.clear()
        self._read_until_line_startswith(
            fileobj, "Average deposited energies (energy detectors)"
        )
        line = fileobj.readline().strip()
        while line:  # until empty line
            body = int(line[11:13])
            val, unc, _effic = self._read_all_values(line)
            self.average_detector_deposited_energy_eV[body] = ufloat(val, unc / 3)
            line = fileobj.readline().strip()

        line = self._read_until_line_startswith(fileobj, "Last random seeds")
        seed1, seed2 = map(int, line.split("=")[1].split(","))
        self.last_random_seed1 = ufloat(seed1, 0.0)
        self.last_random_seed2 = ufloat(seed2, 0.0)

    def read_directory(self, dirpath):
        filepath = os.path.join(dirpath, "pencyl-res.dat")
        with open(filepath, "r") as fp:
            self.read(fp)

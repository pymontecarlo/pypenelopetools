""""""

# Standard library modules.
import os

# Third party modules.
from uncertainties import ufloat, unumpy as unumpy

import pyxray

# Local modules.
from pypenelopetools.penelope.result import _PenelopeResultBase

# Globals and constants variables.

class PenepmaResult(_PenelopeResultBase):

    def __init__(self):
        super().__init__()

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
        self.upbound_fraction = ufloat(val, unc / 3)

        line = self._read_until_line_startswith(fileobj, 'Downbound fraction')
        val, unc = self._read_all_values(line)
        self.downbound_fraction = ufloat(val, unc / 3)

        line = self._read_until_line_startswith(fileobj, 'Absorption fraction')
        val, unc = self._read_all_values(line)
        self.absorbed_fraction = ufloat(val, unc / 3)

        self._read_until_line_startswith(fileobj, 'Secondary-particle generation probabilities')
        fileobj.readline() # skip header
        fileobj.readline() # skip header

        fileobj.readline() # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.upbound_secondary_electron_generation_probabilities = ufloat(val_el, unc_el / 3)
        self.upbound_secondary_photon_generation_probabilities = ufloat(val_ph, unc_ph / 3)
        self.upbound_secondary_positron_generation_probabilities = ufloat(val_po, unc_po / 3)

        fileobj.readline() # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.downbound_secondary_electron_generation_probabilities = ufloat(val_el, unc_el / 3)
        self.downbound_secondary_photon_generation_probabilities = ufloat(val_ph, unc_ph / 3)
        self.downbound_secondary_positron_generation_probabilities = ufloat(val_po, unc_po / 3)

        fileobj.readline() # skip header
        val_el, val_ph, val_po = self._read_all_values(fileobj.readline())
        unc_el, unc_ph, unc_po = self._read_all_values(fileobj.readline())
        self.absorbed_secondary_electron_generation_probabilities = ufloat(val_el, unc_el / 3)
        self.absorbed_secondary_photon_generation_probabilities = ufloat(val_ph, unc_ph / 3)
        self.absorbed_secondary_positron_generation_probabilities = ufloat(val_po, unc_po / 3)

        self.average_deposited_energy_eV.clear()
        self._read_until_line_startswith(fileobj, 'Average deposited energies (bodies)')
        line = fileobj.readline().strip()
        while line.startswith('Body'):
            body = int(line[5:9])
            val, unc, _effic = self._read_all_values(line)
            self.average_deposited_energy_eV[body] = ufloat(val, unc / 3)
            line = fileobj.readline().strip()

        self.average_photon_energy_eV.clear()
        self._read_until_line_startswith(fileobj, 'Average photon energy at the detectors')
        line = fileobj.readline().strip()
        while line.startswith('Detector'):
            detector = int(line[10:12])
            val, unc, _effic = self._read_all_values(line)
            self.average_photon_energy_eV[detector] = ufloat(val, unc / 3)
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

class _PenepmaPhotonDetectorResult(_PenelopeResultBase):

    def __init__(self, detector_index):
        super().__init__()
        self.detector_index = detector_index
        self.theta1_deg = ufloat(0.0, 0.0)
        self.theta2_deg = ufloat(0.0, 0.0)
        self.phi1_deg = ufloat(0.0, 0.0)
        self.phi2_deg = ufloat(0.0, 0.0)

    def read(self, fileobj):
        line = self._read_until_line_startswith(fileobj, '#  Results from PENEPMA. Output from photon detector')
        _, detector_index = line.rsplit('#', 1)
        detector_index = int(detector_index)
        if detector_index != self.detector_index:
            raise IOError('Mismatch of detector index (expected {}, found {})'
                          .format(self.detector_index, detector_index))

        line = self._read_until_line_startswith(fileobj, '#  Angular intervals :')
        theta1_deg, theta2_deg = self._read_all_values(line)
        self.theta1_deg = ufloat(theta1_deg, 0.0)
        self.theta2_deg = ufloat(theta2_deg, 0.0)

        line = fileobj.readline()
        phi1_deg, phi2_deg = self._read_all_values(line)
        self.phi1_deg = ufloat(phi1_deg, 0.0)
        self.phi2_deg = ufloat(phi2_deg, 0.0)

class PenepmaIntensityResult(_PenepmaPhotonDetectorResult):

    def __init__(self, detector_index):
        """
        Intensities of a detector. 
        """
        super().__init__(detector_index)

        self.primary_intensities_1_per_sr_electron = {}
        self.characteristic_fluorescence_intensities_1_per_sr_electron = {}
        self.bremsstrahlung_fluorescence_intensities_1_per_sr_electron = {}
        self.total_fluorescence_intensities_1_per_sr_electron = {}
        self.total_intensities_1_per_sr_electron = {}

    def read(self, fileobj):
        super().read(fileobj)

        self.primary_intensities_1_per_sr_electron.clear()
        self.characteristic_fluorescence_intensities_1_per_sr_electron.clear()
        self.bremsstrahlung_fluorescence_intensities_1_per_sr_electron.clear()
        self.total_fluorescence_intensities_1_per_sr_electron.clear()
        self.total_intensities_1_per_sr_electron.clear()
        self._read_until_line_startswith(fileobj, '# IZ S0 S1  E (eV)')
        for line in fileobj:
            z = int(line[3:5])
            dst = pyxray.atomic_subshell(line[6:8].strip())
            src = pyxray.atomic_subshell(line[9:11].strip())
            xrayline = pyxray.XrayLine(z, (src, dst))

            _e, val_p, unc_p, val_c, unc_c, val_b, unc_b, val_tf, unc_tf, val_t, unc_t = self._read_all_values(line)
            self.primary_intensities_1_per_sr_electron[xrayline] = ufloat(val_p, unc_p / 3)
            self.characteristic_fluorescence_intensities_1_per_sr_electron[xrayline] = ufloat(val_c, unc_c / 3)
            self.bremsstrahlung_fluorescence_intensities_1_per_sr_electron[xrayline] = ufloat(val_b, unc_b / 3)
            self.total_fluorescence_intensities_1_per_sr_electron[xrayline] = ufloat(val_tf, unc_tf / 3)
            self.total_intensities_1_per_sr_electron[xrayline] = ufloat(val_t, unc_t / 3)

    def read_directory(self, dirpath):
        filepath = os.path.join(dirpath, 'pe-intens-{:02d}.dat'.format(self.detector_index))
        with open(filepath, 'r') as fp:
            self.read(fp)

class PenepmaSpectrumResult(_PenepmaPhotonDetectorResult):

    def __init__(self, detector_index):
        super().__init__(detector_index)

        self.energy_window_start_eV = ufloat(0.0, 0.0)
        self.energy_window_end_eV = ufloat(0.0, 0.0)
        self.channel_width_eV = ufloat(0.0, 0.0)

        self.spectrum = unumpy.uarray([], [])

    def read(self, fileobj):
        super().read(fileobj)

        line = self._read_until_line_startswith(fileobj, '#  Energy window =')
        start_eV, end_eV = self._read_all_values(line)
        self.energy_window_start_eV = ufloat(start_eV, 0.0)
        self.energy_window_end_eV = ufloat(end_eV, 0.0)

        line = self._read_until_line_startswith(fileobj, '#  Channel width =')
        channel_width_eV, = self._read_all_values(line)
        self.channel_width_eV = ufloat(channel_width_eV, 0.0)

        spectrum = []
        spectrum_unc = []
        self._read_until_end_of_comments(fileobj)
        for line in fileobj:
            energy_eV, val, unc = self._read_all_values(line)
            spectrum.append([energy_eV, val])
            spectrum_unc.append([0.0, unc / 3])

        self.spectrum = unumpy.uarray(spectrum, spectrum_unc)

    def read_directory(self, dirpath):
        filepath = os.path.join(dirpath, 'pe-spect-{:02d}.dat'.format(self.detector_index))
        with open(filepath, 'r') as fp:
            self.read(fp)

    @property
    def energy_eV(self):
        return self.spectrum[:, 0]

    @property
    def intensities_1_per_sr_electron(self):
        return self.spectrum[:, 1]

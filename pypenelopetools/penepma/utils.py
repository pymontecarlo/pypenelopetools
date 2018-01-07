""""""

# Standard library modules.

# Third party modules.
import pyxray

# Local modules.

# Globals and constants variables.

_SUBSHELL_LOOKUP = \
    {pyxray.atomic_subshell('K'): 1,

     pyxray.atomic_subshell('L1'): 2,
     pyxray.atomic_subshell('L2'): 3,
     pyxray.atomic_subshell('L3'): 4,

     pyxray.atomic_subshell('M1'): 5,
     pyxray.atomic_subshell('M2'): 6,
     pyxray.atomic_subshell('M3'): 7,
     pyxray.atomic_subshell('M4'): 8,
     pyxray.atomic_subshell('M5'): 9,

     pyxray.atomic_subshell('N1'): 10,
     pyxray.atomic_subshell('N2'): 11,
     pyxray.atomic_subshell('N3'): 12,
     pyxray.atomic_subshell('N4'): 13,
     pyxray.atomic_subshell('N5'): 14,
     pyxray.atomic_subshell('N6'): 15,
     pyxray.atomic_subshell('N7'): 16,

     pyxray.atomic_subshell('O1'): 17,
     pyxray.atomic_subshell('O2'): 18,
     pyxray.atomic_subshell('O3'): 19,
     pyxray.atomic_subshell('O4'): 20,
     pyxray.atomic_subshell('O5'): 21,
     pyxray.atomic_subshell('O6'): 22,
     pyxray.atomic_subshell('O7'): 23,

     pyxray.atomic_subshell('P1'): 24,
     pyxray.atomic_subshell('P2'): 25,
     pyxray.atomic_subshell('P3'): 26,
     pyxray.atomic_subshell('P4'): 27,
     pyxray.atomic_subshell('P5'): 28,

     pyxray.atomic_subshell('Q1'): 29,
     }

def convert_xrayline_to_izs1s200(xrayline):
    """
    Converts a :class:`XrayLine` from 
    `pyxray <https://github.com/openmicroanalysis/pyxray>`_ package to 
    PENELOPE's IZS1S200 format.
    
    Args:
        xrayline (:obj:`XrayLine`): X-ray line
        
    Returns:
        int: Corresponding PENELOPE's IZS1S200
        
    Raises:
        ValueError: If the :class:`XrayLine` contains more than one transition.
        ValueError: If source or destination subshell are not supported.
    """
    iz = xrayline.atomic_number

    if len(xrayline.transitions) != 1:
        raise ValueError('XrayLine should only contain one transition.')
    transition = xrayline.transitions[0]

    s1 = _SUBSHELL_LOOKUP.get(transition.destination_subshell)
    if s1 is None:
        raise ValueError('Unsupported destination subshell: {}.'
                         .format(transition.destination_subshell))

    s2 = _SUBSHELL_LOOKUP.get(transition.source_subshell)
    if s2 is None:
        raise ValueError('Unsupported source subshell: {}.'
                         .format(transition.source_subshell))

    return int(iz * 1e6 + s1 * 1e4 + s2 * 1e2)

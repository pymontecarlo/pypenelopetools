Tutorial
========

PENEPMA
-------

In this tutorial, we will show how to create the 2nd example distributed with 
PENEPMA (``epma2.in``). 
It consists of a couple of copper on one side and iron on the other.
The materials, geometry (``.geo``) and input file (``.in``) will all be created
and the results will be analyzed using **pyPENELOPEtools**.
The complete code can also be found in the unit tests.

The tutorial assumes that:
    * **pyPENELOPEtools** is installed.
    * PENELOPE and PENEPMA are installed,
    * PENELOPE is located in a folder called ``/penelope`` and the material
      executable in ``/penelope/pendbase/material``,
    * PENEPMA is located in a folder called ``/penepma`` and the executable in
      ``/penepma/bin/penepma``, and
    * Simulation files are placed in the folder ``/simulation/epma2``.

Materials
^^^^^^^^^

First, let's create two :class:`Material <pypenelopetools.material.Material>` 
definitions.

.. code-block:: python

   from pypenelopetools.material import Material
   material_cu = Material('Cu', {29: 1.0}, 8.9)
   material_fe = Material('Fe', {26: 1.0}, 7.874)
    
To create the actual material files (``.mat``), we first need to export the
input file for the ``material`` executable.

.. code-block:: python

   with open('/penelope/pendbase/Cu.mat.in', 'w') as fp:
       material_cu.write_input(fp)
   with open('/penelope/pendbase/Fe.mat.in', 'w') as fp:
       material_fe.write_input(fp)
        
From a command prompt in the folder ``/penelope/pendbase``, run the following
commands to create the two material files (``Cu.mat`` and ``Fe.mat``):

.. code-block:: shell

   ./material < Cu.mat.in
   ./material < Fe.mat.in
   
The material files can now be copied in ``/simulation/epma2``.

Geometry
^^^^^^^^

PENGEOM geometries consist of surfaces and modules.
A :class:`SurfaceImplicit <pypenelopetools.pengeom.surface.SurfaceImplicit>` 
can be arbitrarily defined using quadratic equations, but **pyPENELOPEtools** 
also provides utility functions for simple cases.
A :class:`Module <pypenelopetools.pengeom.module.Module>` group different 
surfaces and other modules together forming an object with an associated 
:class:`Material <pypenelopetools.material.Material>`.

For this example, the couple geometry consists of a cylinder with three planes:
one defining the top surface, one for the bottom surface and a dividing plane
in the middle.
Let's create these surfaces using the utility functions:

.. code-block:: python
    
   from pypenelopetools.pengeom.surface import xplane, zplane, cylinder
   surface_top = zplane(0.0)
   surface_bottom = zplane(-0.1)
   surface_cylinder = cylinder(1.0)
   surface_divider = xplane(0.0)
    
All the dimensions are in centimeters, so the code above creates a cylinder with
a radius of 1cm and a depth of 100mm.
The couple is divided with a plane perpendicular to the x-axis.

Let's now construct our two modules, corresponding to the right and left halves
of the couple geometry:

.. code-block:: python
    
   from pypenelopetools.pengeom.module import Module, SidePointer
   module_right = Module(material_cu, 'Right half of the sample')
   module_right.add_surface(surface_top, SidePointer.NEGATIVE)
   module_right.add_surface(surface_bottom, SidePointer.POSITIVE)
   module_right.add_surface(surface_cylinder, SidePointer.NEGATIVE)
   module_right.add_surface(surface_divider, SidePointer.POSITIVE)

   module_left = Module(material_fe, 'Left half of the sample')
   module_left.add_surface(surface_top, SidePointer.NEGATIVE)
   module_left.add_surface(surface_bottom, SidePointer.POSITIVE)
   module_left.add_surface(surface_cylinder, SidePointer.NEGATIVE)
   module_left.add_module(module_right)

The side pointer specifies which side of the surface forms the enclosed module.
Note that the right module is added to the left module.
This tells PENGEOM that the two modules are touching each other and share a 
common interface. 

The two modules are put together into a 
:class:`Geometry <pypenelopetools.pengeom.geometry.Geometry>`:

.. code-block:: python

   geometry = Geometry('Cylindrical homogeneous foil')
   geometry.add_module(module_right)
   geometry.add_module(module_left)

Finally, the geometry can be saved as a ``.geo`` file. 
The filename should be remembered since it will be needed to construct the 
input file.

.. code-block:: python

   geofilename = 'epma2.geo'
   with open('/simulation/epma2/' + geofilename, 'w') as fp:
       index_lookup = geometry.write(fp)

The :meth:`write` method returns an important value, a lookup table with the
indexes that were associated with the modules and materials.
These indexes will be needed to construct the input file.

.. important::
   PENELOPE, PENGEOM and PENEPMA rely on indexes and properly ordered lines in
   the input file to identify the right materials or modules.
   This strategy does not work very well with object oriented programming (i.e.
   classes, objects, etc.), so **pyPENELOPEtools** uses an *index lookup* to try
   to link the two approaches.
   This way the user does not have to remember all the indexes, although the
   index-based approach can still be used if needed.

Input
^^^^^

Let's now create the input file (``.in``) for the simulation.
All the simulation parameters are stored in a 
`PenepmaInput <pypenelopetools.penepma.input.PenepmaInput>` object.

.. code-block:: python

   from pypenelopetools.penepma.input import PenepmaInput
   input = PenepmaInput()

The `PenepmaInput <pypenelopetools.penepma.input.PenepmaInput>` object contains
all the keywords available for a PENEPMA simulation.
Have a look at the documentation to see which ones are available and what are
their parameters.

First, we setup the title and electron beam definition: a 15kV electron beam 
with an initial position at ``x=20um`` and ``z=1cm`` pointing downwards.

.. code-block:: python

   input.TITLE.set('A CU-Fe couple')
   input.SENERG.set(15e3)
   input.SPOSIT.set(2e-5, 0.0, 1.0)
   input.SDIREC.set(180, 0.0)
   input.SAPERT.set(0.0)

Secondly, the materials and their simulation parameters. 
We use the *index_lookup* to find the index of the materials and the *filename*
property to find the filename of each material.

.. code-block:: python

   input.materials.add(index_lookup[material_cu], material_cu.filename, 1e3, 1e3, 1e3, 0.2, 0.2, 1e3, 1e3)
   input.materials.add(index_lookup[material_fe], material_fe.filename, 1e3, 1e3, 1e3, 0.2, 0.2, 1e3, 1e3)
    
Thirdly, the geometry definition and the maximum step length parameters.
Again here we use the *index_lookup* to find the index of the modules.

.. code-block:: python

   input.GEOMFN.set(geofilename)
   input.DSMAX.add(index_lookup[module_right], 1e-4)
   input.DSMAX.add(index_lookup[module_left], 1e-4)

Fourthly, the interaction forcings and splitting parameters.
This is a copy of the parameters in the PENEPMA example.

.. code-block:: python

   input.IFORCE.add(index_lookup[module_right], 1, 4, -5, 0.9, 1.0)
   input.IFORCE.add(index_lookup[module_right], 1, 5, -250, 0.9, 1.0)
   input.IFORCE.add(index_lookup[module_right], 2, 2, 10, 1e-3, 1.0)
   input.IFORCE.add(index_lookup[module_right], 2, 3, 10, 1e-3, 1.0)
   input.IFORCE.add(index_lookup[module_left], 1, 4, -5, 0.9, 1.0)
   input.IFORCE.add(index_lookup[module_left], 1, 5, -7, 0.9, 1.0)
   input.IFORCE.add(index_lookup[module_left], 2, 2, 10, 1e-3, 1.0)
   input.IFORCE.add(index_lookup[module_left], 2, 3, 10, 1e-3, 1.0)

   input.IBRSPL.add(index_lookup[module_right], 2)
   input.IBRSPL.add(index_lookup[module_left], 2)

   input.IXRSPL.add(index_lookup[module_right], 2)
   input.IXRSPL.add(index_lookup[module_left], 2)
    
Fifthly, the emerging particle distributions, photon detectors and
spatial distribution.

.. code-block:: python
   
   import pyxray
   from pypenelopetools.penepma.utils import convert_xrayline_to_izs1s200
   
   input.NBE.set(0, 0, 300)
   input.NBANGL.set(45, 30)
    
   input.photon_detectors.add(0, 90, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(5, 15, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(15, 25, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(25, 35, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(35, 45, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(45, 55, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(55, 65, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(65, 75, 0, 360, 0, 0.0, 0.0, 1000)
   input.photon_detectors.add(75, 85, 0, 360, 0, 0.0, 0.0, 1000)
   
   input.GRIDX.set(-1e-5, 5e-5, 60)
   input.GRIDY.set(-3e-5, 3e-5, 60)
   input.GRIDZ.set(-6e-5, 0.0, 60)
   input.XRLINE.add(convert_xrayline_to_izs1s200(pyxray.xray_line(26, 'Ka2')))
   input.XRLINE.add(convert_xrayline_to_izs1s200(pyxray.xray_line(29, 'Ka2')))

.. important::
   The theta angles of a photon detector are defined as angles from the 
   positive z-axis.
   This is different than the take-off angle usually used in 
   microanalysis.
   For a take-off angle of 30deg, theta would be 60deg.
   
.. hint::
   Use :func:`convert_xrayline_to_izs1s200 <pypenelopetools.penepma.utils.convert_xrayline_to_izs1s200>`
   to convert :class:`XrayLine` from 
   `pyxray <https://github.com/openmicroanalysis/pyxray>`_ library to 
   PENELOPE's ILB(4) notation.
   
Finally, the job properties.
The first random seed is negative to force the generation of a random seed
every time a simulation is started.
We also use the conversion function from :class:`XrayLine` to ILB(4) notation
for the relative uncertainty termination :class:`REFLIN`.
The simulation will terminate if the relative uncertainty (3-sigma) on the
Fe Ka2 total characteristic intensity detected by the first detector is less 
than 0.15%.

.. code-block:: python
   
   input.RESUME.set('dump2.dat')
   input.DUMPTO.set('dump2.dat')
   input.DUMPP.set(60)

   input.RSEED.set(-10, 1)
   input.REFLIN.set(convert_xrayline_to_izs1s200(pyxray.xray_line(26, 'Ka2')), 1, 1.5e-3)
   input.NSIMSH.set(2e9)
   input.TIME.set(2e9)
   
That completes all the parameters for the simulation.
The last step is to save them as a ``.in`` file.

.. code-block:: python

   with open('/simulation/epma2/epma2.in', 'w') as fp:
       input.write(fp)

From the ``/simulation/epma2`` folder, the simulation can be run using the
PENEPMA main program.

.. code-block:: shell

   penepma < epma2.in

Results
^^^^^^^

After the simulation has terminated or even after the first dump, the results
can be read using **pyPENELOPEtools**.
Each result has its own class that follows the same interface.
The next lines describe how to read the backscatter electron coefficient and 
plot the photon spectrum of the first detector.
For more information about the results, please refer to the :ref:`API <api>` 
section.

To read the simulation time, we create a 
:class:`PenepmaResult <pypenelopetools.penepma.results.PenepmaResult>` object 
and call its :meth:`read_directory` method.

.. code-block:: python

   from pypenelopetools.penepma.results import PenepmaResult
   result = PenepmaResult()
   result.read_directory('/simulation/epma2')

The backscatter electron coefficient is stored in the attribute 
:attr:`upbound_fraction` which returns a :class:`ufloat` object.
:class:`ufloat` objects are from the library
`uncertainties <https://pythonhosted.org/uncertainties>`_ which is designed
to handle values and their uncertainties.
Here is how to extract the nominal and standard deviation (1-sigma) of the
backscatter electron coefficient:

.. code-block:: python

   bse = result.upbound_fraction.nominal_value
   bse = result.upbound_fraction.n # alternative
   unc_bse = result.upbound_fraction.std_dev
   unc_bse = result.upbound_fraction.s # alternative

.. important::
   All results in **pyPENELOPEtools** are stored for consistency using 
   :class:`ufloat`, even those where the uncertainty is always 0.0 (e.g.
   total simulation time).

To plot the photon spectrum, we first create a 
:class:`PenepmaSpectrumResult <pypenelopetools.penepma.results.PenepmaSpectrumResult>`
object.
The class takes one argument, the index of the detector to read.
The first detector has an index of 1.

.. code-block:: python
   
   from pypenelopetools.penepma.results import PenepmaSpectrumResult
   result = PenepmaSpectrumResult(1)
   result.read_directory('/simulation/epma2')
   
To plot the spectrum, we use the library `matplotlib <http://matplotlib.org>`_.
The x-axis (energy axis) is stored in the attribute :attr:`energies_eV` whereas
the intensities in 1/(sr.electron) in the attribute 
:attr:`intensities_1_per_sr_electron`.

.. code-block:: python

   import matplotlib.pyplot as plt
   
   fig, ax = plt.subplots(1, 1)
   ax.plot(result.energies_eV, result.intensities_1_per_sr_electron, '-')
   plt.show()

This completes the PENEPMA tutorial.


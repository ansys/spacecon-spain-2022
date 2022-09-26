"""
.. _ref_pymapdl_tutorial

================
PyMAPDL Tutorial
================

In this tutorial, we will introduce some of the capabilities of
PyMAPDL applied to Aerospace students and advocates.

Content
=======

# To be added

* (Very) short introduction to Python
* (Very) short introduction to PyAnsys and PyMAPDL
* (Veeery) Short example on PyMAPDL.

"""

#########################################################
# Python + Ansys = PyAnsys
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# Pyansys is Ansys effort on making their products accessible
# using Python programming language.
#
# Today we will focus on PyMAPDL with is the Python library
# which exposes MAPDL (Ansys Structural)
#

##########################################################
# PyMAPDL
# ~~~~~~~
# MAPDL provides many tools and features which would require
# A LOT of time to explain, so let's have a quick overview

##########################################################
# Launching PyMAPDL
# -----------------
# But first, let's launch PyMAPDL.
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

print(mapdl)

############################################################
# Geometry
# --------
#
# PyMAPDL support points (keypoints), lines, areas, and volumes
# for geometry definition.
#
# You can plot an area using keypoints:
mapdl.prep7()  # entering in preprocessor for geometry generation

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 0, 1, 0)
a0 = mapdl.a(k0, k1, k2)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos="xy")

##################################
# Create a simple cube volume.
#
mapdl.clear()  # let's clear first.
mapdl.prep7()  # entering in preprocessor

k0 = mapdl.k("", 0, 0, 0)  # defining a keypoint at (0,0,0) location
k1 = mapdl.k("", 1, 0, 0)  # defining a keypoint at (1,0,0) location
k2 = mapdl.k("", 1, 1, 0)  # etc
k3 = mapdl.k("", 0, 1, 0)
k4 = mapdl.k("", 0, 0, 1)
k5 = mapdl.k("", 1, 0, 1)
k6 = mapdl.k("", 1, 1, 1)
k7 = mapdl.k("", 0, 1, 1)

# defining volume according the kps
v0 = mapdl.v(k0, k1, k2, k3, k4, k5, k6, k7)

mapdl.vplot(show_lines=True)

###################################
# Material definition
# -------------------
#
# You can define materials using the following commands:

# Define a material (nominal steel in SI)
mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

###################################
# At any point you can use help to get information about each
# function
help(mapdl.mp)

#####################################
# Or you can check the online help at
# `mapdl.docs.pyansys.com <https://mapdl.docs.pyansys.com/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.Mapdl.mp.html?highlight=mp#ansys.mapdl.core.Mapdl.mp>`_

########################################
# Element definition
# ------------------
#
# Since MAPDL is a finite element solver,
# the FE element needs to be defined.
# Ansys has an *Element Guide* which contain all the necessary
# information

mapdl.et(1, "SOLID186")

##################################################
# SOLID186 is a 3D hexahedron element, suitable for
# any structural 3D analysis.
#
# There are also ``KEYOPTS`` which allow us to
# configure the elements.
# Also there is the constant sets ``R`` which helps
# us to set the analysis and element configurations.

####################################################
# Meshing
# -------
#
# Meshing is quite easy, once the element and material
# are defined.
mapdl.esize(1 / 10)  # Element size
mapdl.vmesh(v0)

####################################################
# Let's see the result
mapdl.eplot()  # plot elements


###############################################
# Boundary conditions
# -------------------
#
# There are many boundary conditions options, and most of
# them are applied using ``mapdl.d`` (for displacement)
# or ``mapdl.f`` (for force).
#
# Let's setup this example to represent a compression test.
# For that purpose, we need to fix the box bottom surface to have zero
# displacement.
#
# But first, we need to select the corresponding nodes using
# the ``mapdl.nsel`` command:
#

help(mapdl.nsel)

###############################################
#

mapdl.nsel("S", "loc", "z", 0)
mapdl.nplot()  # check the selection

###############################################
# Applying to all selected nodes, displacement in Z direction equals to zero.
mapdl.d("all", "UZ", 0)

# Let's check the result
mapdl.nplot(plot_bc=True)

##############################################
# Let's apply the rest of the boundary conditions.
#

# Let's fix the box edge XZ to not move except along Y.
mapdl.nsel("s", "loc", "z", 0)
# "r" is to reselect the nodes, from the previous "S" selection
mapdl.nsel("r", "loc", "x", 0)

mapdl.d("all", "UZ", 0)
mapdl.d("all", "UX", 0)

# we will do the same with the line YZ, but not move along X direction.
mapdl.nsel("s", "loc", "z", 0)
mapdl.nsel("r", "loc", "Y", 0)

mapdl.d("all", "UZ", 0)
mapdl.d("all", "UY", 0)

########################################################################
# Finally let's fix one node in the directions:
#
mapdl.nsel("s", "loc", "x", 0)
mapdl.nsel("r", "loc", "y", 0)
mapdl.nsel("r", "loc", "z", 0)

mapdl.d("all", "all", 0)

# this code is redundant, because the nodal displacements do not overwrite each other
# if they are not in the same direction.
# This node was included in the previous lines selections, hence its
# boundary conditions are already defined.

#####################################################################
# Let's check the final result
mapdl.nsel("s", "loc", "z", 0)

mapdl.nplot(plot_bc=True)

################################################
# Now let's apply a displacement at the box top at each node.
# We could apply a force instead if we wish.
mapdl.nsel("s", "loc", "z", 1)
# mapdl.f("all", "FZ", 1E9)
mapdl.d("all", "UZ", 0.01)

################################################
# Analysis setup
# --------------
#
# Let's do a simple static analysis
#
mapdl.slashsolu()
mapdl.allsel()  # making sure all nodes and elements are selected.
mapdl.antype("STATIC")
output = mapdl.solve()
print(output)

###############################################
# Post-Processing
# ---------------
#
# Let's what we got. Let's see the displacements:
mapdl.post_processing.nodal_displacement("all")

###################################################
# Let's plot them
mapdl.post_processing.plot_nodal_displacement("Z")

################################################
# We can store the displacements as an array and
# use them for our calculations. For example:

nodal_disp = mapdl.post_processing.nodal_displacement("all")

print(f"The maximum displacement is {nodal_disp.max():0.3f}")

############################################
#  Oh! By the way, you can format strings as this way, they are very powerful.
# This type of string is called f-string. The 0.3f after the colon (:) is the format for the number.

# First column is X displacement
print(f"The maximum X displacement is {nodal_disp[:, 0].max():0.3f}")

print(f"The average Z displacement is {nodal_disp[:, 2].mean():0.3f}")

###############################################
# Closing session
# ---------------
#
# This is all for today. We hope you enjoyed this talk, as much as we enjoyed preparing it!
#
# Closing PyMAPDL session
mapdl.exit()

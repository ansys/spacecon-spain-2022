"""
.. _ref_pymapdl_tutorial

==================================
PyMAPDL Tutorial for SpaceCon 2022
==================================

In this tutorial, we will introduce some of the capabilities of
PyMAPDL applied to Aerospace students and advocates.

Content
=======

# To be added

* (Very) short introduction to Python
* (Very) short introduction to PyAnsys and PyMAPDL
* (Veeery) Short example on PyMAPDL.

"""

################################
#
# But first...
#

#################################
#
# What is PyMAPDL?
# ~~~~~~~~~~~~~~~~
#
# PyMAPDL is the pythonic interface for Ansys MAPDL product.
#


#################################
# **What does this mean?**
#
# It means that you can call Ansys products (Solvers, Post processing tools, etc)
# using Python programming language.
#

################################
# What is python?
# ~~~~~~~~~~~~~~~
#
# Python is #TODO: TO FILL

#################################
# Introduction to Python
# ~~~~~~~~~~~~~~~~~~~~~~
#
# Storing variables.
#

mystring = "text"
myotherstring = "text"
myfloat = 2.2
myint = 2
mybool = (
    True  # True and False are reserved keywords. As well as for, in, as and some more.
)

#####################################
# There are functions such as ``print`` or ``help`` which can be called as:

print("Hello Madrid!")  # You can call functions using parenthesis

help(print)

#####################################
# There are other more complex structures such as list, tuples, dicts, etc

mylist = [1, 2.2, "asdf"]
print(mylist[0])  # Python is zero based indexing!

mytuple = (1, 2.5, "qwer")
print(mytuple[2])  # Indexing in python is done using square brackets `[]`

#########################################
# This is a dict which does a mapping between its
# keys and values.
mydict = {"a": 1, "b": 2, "c": 3}
# keys are the leters, but it could be anything
# values are the numbers, but it could be anything!

print(mydict["c"])


#####################################
# Control flow in Python
# ~~~~~~~~~~~~~~~~~~~~~~
#
# You can do conditionals (``if``) as the following:
my_int = 2

if myint > 5:
    print("My int is bigger than 5!")
elif myint > 2:
    print("My int is bigger than 2!")
else:
    print("Any other case")

if mybool:
    print("Because 'mybool' is True, I'm showing you this.")

if mystring == myotherstring:  # "text" == 'text'
    print("Although we used different quotes, they are the same!")

#####################################################
# Loops in python
# ~~~~~~~~~~~~~~~
#
# Loops in Python can be done as:
#
for i in [1, 2, 3]:
    print(i)

#######################################################
# or
for i in range(0, 5):
    print(i)

########################################################
# there is also 'while' loops
i = 0
while i < 5:
    print(i)
    i = i + 1

#######################################################
# You can "break" loops using the keyword ``break``

i = 0
j = 0
while i < 10:
    print(i, j)
    i += 1  # Convenient way to express: i = i + 1
    j += 2

    if j > 5:  # early exit
        print("Exiting early!")
        break

###################################
# Importing other libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# You can also import other libraries that expand Python functionalities by
# providing more data structures, functions and/or classes.

import os  # for Operative system operations related

print(os.name)  # OS name: nt or linux

#######################################
# You can also import modules/functions from libraries
from os.path import exists

exists("myfile.txt")  # Check if file 'myfile.txt' exists or not. Should show False

###########################################
# You can import a library giving it another name
import math as mm  # Built in math library

print(mm.sqrt(2))

####################################################
# Numpy and Matplotlib
# ~~~~~~~~~~~~~~~~~~~~
#
# Some of the most used Python libraries are: Numpy and Matplotlib.
# The first one is for numerical calculations and the second is
# for plotting.

import numpy as np

my_array = np.array(
    [1, 2, 3]
)  # Arrays are a very convenient and powefull data structure.

print(my_array * 2)  # element wise operations

print(my_array.T)  # Transpose

# It doesn't need to be a vector
my_matrix = np.array([[1, 3, 4], [4, 5, 6]])  # You store arrays of any shape

#########################################
# You can index elements using square brackets:
my_matrix[0, 0]  # 1
my_matrix[1, 1]  # 5
my_matrix[0, :]  # [1, 3, 4]
my_matrix[:, 0]  # [1, 4]

###################################################################
# for plotting you can use matplotlib
from matplotlib import pyplot as plt

plt.plot(my_array, my_matrix[1, :], "r")
plt.title("My plot!")
plt.show()


#################################################################
# You can do multiple lines at once.
#
plt.plot(my_array, my_matrix[0, :], "r", label="My red line")
plt.plot(my_array, my_matrix[1, :], "b", label="My blue line")
plt.title("My fancy plot")
plt.legend()
plt.show()

#################################################################
#

##################################################################
# Plotting a NACA airfoil
# ~~~~~~~~~~~~~~~~~~~~~~~
# *"Those plots looks rather simple plots...."*
#
# Ok, let me show you:
#
# Reference: https://en.wikipedia.org/wiki/NACA_airfoil#Equation_for_a_cambered_4-digit_NACA_airfoil
#

# First let define some helper functions.
def camber_line(x, m, p, c):
    return np.where(
        (x >= 0) & (x <= (c * p)),
        m * (x / np.power(p, 2)) * (2.0 * p - (x / c)),
        m * ((c - x) / np.power(1 - p, 2)) * (1.0 + (x / c) - 2.0 * p),
    )


def dyc_over_dx(x, m, p, c):
    return np.where(
        (x >= 0) & (x <= (c * p)),
        ((2.0 * m) / np.power(p, 2)) * (p - x / c),
        ((2.0 * m) / np.power(1 - p, 2)) * (p - x / c),
    )


def thickness(x, t, c):
    term1 = 0.2969 * (np.sqrt(x / c))
    term2 = -0.1260 * (x / c)
    term3 = -0.3516 * np.power(x / c, 2)
    term4 = 0.2843 * np.power(x / c, 3)
    term5 = -0.1015 * np.power(x / c, 4)
    return 5 * t * c * (term1 + term2 + term3 + term4 + term5)


def naca4(x, m, p, t, c=1):
    dyc_dx = dyc_over_dx(x, m, p, c)
    th = np.arctan(dyc_dx)
    yt = thickness(x, t, c)
    yc = camber_line(x, m, p, c)
    return (
        (x - yt * np.sin(th), yc + yt * np.cos(th)),
        (x + yt * np.sin(th), yc - yt * np.cos(th)),
    )


# NACA Parameters
# naca2412
m = 0.02
p = 0.4
t = 0.12
c = 1.0

x = np.linspace(0, 1, 200)
for item in naca4(x, m, p, t, c):
    plt.plot(item[0], item[1], "b")

plt.plot(x, camber_line(x, m, p, c), "r")
plt.axis("equal")
_ = plt.xlim((-0.05, 1.05))  # Store dummy values as '_'.


# From: https://stackoverflow.com/questions/31815041/plotting-a-naca-4-series-airfoil

#####################################################
# **Cool stuff uh?**

#####################################################
# Brief Python classes concept
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# **What is a class?**
#
# A class is an object in a programming language which
# .... #TODO: TO BE FILLED.
#
#
# In Python everything is objects, and hence they have some methods.
# For example strings have:
mystring.startswith("t")  # True
mystring.split("e")  # Break the string in a list ["T", "xt"]

######################################################
# You can list the methods of an object using ``dir``:
print(dir(mystring))  # yes, '__add__' is a string method!

###################################################
# You can create your own class and inheritate from them.
#
# PyMAPDL provides you a class which gives you access to all MAPDL
# commands and more.

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

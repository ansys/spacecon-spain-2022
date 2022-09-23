"""
.. _ref_pymapdl_tutorial

==================================
PyMAPDL Tutorial for SpaceCon 2022
==================================

In this tutorial, we will introduce some of the capabilities of
PyMAPDL applied to Aerospace students and advocates.

Content
=======


"""
# sphinx_gallery_thumbnail_number = 3

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
# *What does this mean?*
#
# It means that you can call Ansys products (Solvers, Post processing tools, etc)
# using Python programming language.
#

################################
# What is python?
#
# Python is

#################################
# Common operations in python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

# There are functions such as ``print`` or ``help`` which can be called as:

print("Hello Madrid!")  # You can call functions using parenthesis

print(help(mystring))

#####################################
# There are other more complex structures such as list, tuples, dicts, etc

mylist = [1, 2.2, "asdf"]
print(mylist[0])  # Python is zero based indexing!

mytuple = (1, 2.5, "qwer")
print(mytuple[2])  # Indexing in python is done using square brackets `[]`

# This is a dict which does a mapping between its
# keys and values.
mydict = {"a": 1, "b": 2, "c": 3}
# keys are the leters, but it could be anything
# values are the numbers, but it could be anything!

print(mydict["a"])


#####################################
# Control flow in Python
# ~~~~~~~~~~~~~~~~~~~~~~
#
# You can do conditionals (if) as the following:

if myint > 5:
    print("My int is bigger than 5!")
elif myint > 2:
    print("My int is bigger than 2!")
else:
    print("Any other case")

if mybool:
    print("Because mybool is True, I'm showing you this.")

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

for i in range(0, 5):
    print(i)

i = 0
while i < 5:
    print(i)
    i += 1  # Convenient way to express: i = i + 1


###################################
# Importing other libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# You can also import other libraries that expand Python functionalities by
# providing more data structures, functions and/or classes.

import os  # for Operative system operations related

print(os.name)  # OS name: nt or linux

# You can also import modules/functions from libraries
from os.path import exists

exists("myfile.txt")  # Check if file 'myfile.txt' exists or not. Should show False

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

my_matrix = np.array([[1, 3, 4], [4, 5, 6]])  # You store arrays of any shape

# You can index using square brackets:
my_matrix[0, 0]  # 1
my_matrix[1, 1]  # 5
my_matrix[0, :]  # [1, 3, 4]
my_matrix[:, 0]  # [1, 4]


my_rand_array = np.random.randint(
    0, 10, (2, 3)
)  # random integers between 0 and 10, with shape (2,3)

print(my_rand_array)
print(my_rand_array.shape)

my_matrix.reshape((1, -1))  # and reshape them as you wish.
# Negative means to accommodate this number to fit the other dimension (1). So it will be (1, 6)

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
# *"Those looks rather simple plots...."*
#
# Ok, let me show you:
#

##################################################################
# Plotting a NACA airfoil
# ~~~~~~~~~~~~~~~~~~~~~~~
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
plt.xlim((-0.05, 1.05))

# From: https://stackoverflow.com/questions/31815041/plotting-a-naca-4-series-airfoil

# Cool uh?

#####################################################
# Brief Python classes concept
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# What is a class?
# A class is an object in a programming language which
# .... #TODO: TO BE FILLED.
#

# In Python everything is objects, and hence they have some methods.
# For example strings have:
mystring.startswith("t")  # True
mystring.split("e")  # Break the string in a list ["T", "xt"]


# You can list the methods of an object using ``dir``:
print(dir(mystring))

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
# which exposes MAPDL (Ansys Structural solvers)
#

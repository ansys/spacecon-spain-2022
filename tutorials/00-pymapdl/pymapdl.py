"""
.. _ref_pymapdl_tutorial

==================================
PyMAPDL Tutorial for SpaceCon 2022
==================================

In this tutorial, we will introduce some of the capabilities of
PyMAPDL applied to Aerospace students and advocates.

"""
# sphinx_gallery_thumbnail_number = 3

################################
#
# But first...
#

#################################
#
# What is PyMAPDL?
# ================
#
# PyMAPDL is the pythonic interface for Ansys MAPDL product.
#


#################################
# *What does this mean?*
#
# It means that you can call Ansys products (Solvers, Post processing tools, etc)
# using Python programming language.
#

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()


print(mapdl)
print(mapdl.directory)

###############################################
# Hi
# ==
#
# hi
#

mapdl.exit()

"""
.. _ref_example:

======================
A full PyMAPDL example
======================

Let's see a full PyMAPDL example!

We will reuse some of the code we used to plot the section of a NACA airfoil.
With this section we will create a simple and straight wing where we will apply
some constrains and loads.

The idea is you can have an idea on how to use PyMAPDL together with other
Python libraries for your own purposes (TFG? TFM? PhD?)

"""

##########################################################
# Setting up the environment
# ==========================
# First, let's do some imports
#

from matplotlib import pyplot as plt
import numpy as np

from ansys.mapdl.core import launch_mapdl

###########################################################
# and let's launch PyMAPDL.

mapdl = launch_mapdl()
mapdl.prep7()

############################################################
# Geometry definition
# ===================
#
# In the previous part of the talk we showed how to use some
# Python functions to plot a NACA airfoil.
# Here we will reuse those functions to generate the same
# section inside PyMAPDL.
#

# Helper functions
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

    # We are tuning a bit the output of this function to facilitate later processing.
    x = x - yt * np.sin(th)
    x = np.concatenate((x, x + yt * np.sin(th)), axis=0)

    y = yc + yt * np.cos(th)
    y = np.concatenate((y, yc - yt * np.cos(th)), axis=0)
    return x, y


#########################################################################
# NACA Parameters for naca2412
#
m = 0.02
p = 0.4
t = 0.12
c = 1.0

#########################################################################
# Generating NACA points for the section.
#
npoints = 50  # Increase this number to increase smoothness.
x_ = np.linspace(0, 1, npoints)
x, y = naca4(x_, m, p, t, c)


##########################################################################
# Generating keypoints
# --------------------
#
mapdl.clear()
mapdl.prep7()

for each_x, each_y in zip(x, y):
    mapdl.k("", each_x, each_y)

#########################################################################
# Checking results
#

mapdl.kplot()

############################################################################
# Generate lines from the points
# ------------------------------
# Because of the helper functions give us two points per x-coordenate,
# we need to join those points in two times:

half = len(mapdl.geometry.knum) // 2

# Upper half points
for kp in mapdl.geometry.knum[: half - 1]:
    mapdl.l(kp, kp + 1)

# Lower half points
for kp in mapdl.geometry.knum[half + 1 : -1]:
    mapdl.l(kp, kp + 1)

################################################################################
# Closing the section
mapdl.l(1, half + 2)
mapdl.l(half, mapdl.geometry.knum[-1])

mapdl.nummrg("kp", 0.1)  # Remove duplicate keypoints if any

###############################################################################
# Let's check the results
mapdl.lplot()

###############################################################################
# Create section area
# -------------------
# Let's create an area from those lines:
#
mapdl.lsel("all")
mapdl.al("all")

###############################################################################
# Create volume from extruding the area
# -------------------------------------
#
# We are going to use the command ``mapdl.vdrag`` to create a volume by dragging
# an area along a line.
help(mapdl.vdrag)

#################################################################################
# First, let's define the lince we are going to use to drag the area along.
lenght_wing = 4  # [m] MAPDL is unit agnostic.

k0 = mapdl.k("", 0, 0, 0)
kz = mapdl.k("", 0, 0, lenght_wing)

ldrag = mapdl.l(k0, kz)

#################################################################################
# Create the volume
vol0 = mapdl.vdrag("all", nlp1=ldrag)

#################################################################################
# Let's check the results
mapdl.vplot()


#################################################################################
# Finite element definition
# =========================
#
# As you all know, finite element approaches split the domains into "finite elements"
# where you solve your equations in their quadrature points.
# Therefore, we need to define how that domain split is going to be perform, aka
# "choosing element type".
#

# Defining element type
mapdl.et(1, "SOLID187")

##################################################################################
# Here we could also define other element options using the ``mapdl.keyopt``
# command.


#################################################################################
# Material definition
# ===================
#
# Let's define the material our wing is made off. We are going to choose steel
# in its simplest configuration (elastic linear material). But you could define
# other parameters (plasticity, fatige, viscoelasticity, etc).
#

# Define a material (nominal steel in SI)
mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

#################################################################################
# Mesh Generation
# ===============
#
# Let's finally split the domain:
maximum_element_size = 1 / 20
mapdl.esize(maximum_element_size)

mapdl.vmesh("all")  # Mesh

#################################################################################
# Let's check the results:
mapdl.eplot()


#################################################################################
# Boundary Conditions Definition
# ==============================
#
# Let's fix the nodes at the origin to not move.

mapdl.nsel("s", "loc", "z", 0)
mapdl.d("all", "all", 0)

##################################################################################
# Wind Excitation
# ---------------
#
# Let's apply a wind excitation.
#
# However, we don't really know what wind apply, so let's pull some online data first.
# Use
#
# From: https://power.larc.nasa.gov/data-access-viewer/
#

import json

import pandas as pd
import requests

latitude, longitude = (40.447488, -3.691763)
parameters = ["T2M_MAX", "T2M_MIN"]

base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={parameters}&community=RE&longitude={longitude}&latitude={latitude}&start=20200101&end=20210305&format=JSON"
api_request_url = base_url.format(
    longitude=longitude, latitude=latitude, parameters=",".join(parameters)
)  # Another way to format f-strings!

response = requests.get(url=api_request_url, verify=True, timeout=30.00)

content = json.loads(response.content.decode("utf-8"))
df = pd.DataFrame(content["properties"]["parameter"])

df = df.set_index(
    pd.to_datetime(df.index, format="%Y%m%d")
)  # Formatting dataframe index as date.
#######################################################
# Let's see the data
df.head()

######################################################
# and describe it...
df.describe()

######################################################
# Let's plot it...
df.plot(title="Wind speed per day")

Total_time_sample = 60  # [s]
Amplitude = [10]  # 30, 80, 200]
frequencies = [10, 16, 27, 34]
phase = np.random.random(size=len(frequencies)) * 2 * np.pi


def wind_speed(t):
    # https://www.jstage.jst.go.jp/article/jsmeb/47/2/47_2_378/_pdf
    sum_ = 0
    for each_amp, each_w, each_phase in zip(Amplitude, frequencies, phase):
        sum_ = sum_ + np.sqrt((2 * each_amp) / Total_time_sample) * np.cos(
            each_w * t + each_phase
        )
    return sum_


t = np.arange(0, 60, 0.1)

plt.plot(t, wind_speed(t))
plt.show()

mapdl.nsel("s", "loc", "z", 4)
mapdl.d("all", "ux", 0.01)


#################################################################################
# Model solution
# ==============

mapdl.slashsolu()
mapdl.allsel()  # making sure all nodes and elements are selected.
mapdl.antype("STATIC")
output = mapdl.solve()
print(output)

#################################################################################
# Post-processing
# ===============
#
# Let's see what we got. Let's print the displacements:
mapdl.post_processing.nodal_displacement("all")

######################################################
# and let's plot them
#
mapdl.post_processing.plot_nodal_displacement("x")

#################################################################################
#

#################################################################################
# Closing session
# ===============
#
# Thank you all for your time and attention!
#
mapdl.exit()

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

pl = mapdl.kplot(return_plotter=True)
pl.view_xy()
pl.show()


############################################################################
# Generate lines from the points
# ------------------------------
# Because the helper functions give us two points per x-coordinate,
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

mapdl.nummrg("all", 0.05)  # Remove duplicated entities if any

###############################################################################
# Let's check the results
pl = mapdl.lplot(return_plotter=True)
pl.view_xy()
pl.show()
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
# First, let's define the length we are going to use to drag the area along.
lenght_wing = 1.5  # [m] MAPDL is unit agnostic.

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
# Therefore, we need to define how that domain split is going to be performed, aka
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
maximum_element_size = 1 / 10
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
# Let's apply an excitation to our wing. However, we don't really know what wind
# speed to apply, so let's pull some online data first.
#
# We are going to retrieve some data from NASA regarding the wind speed at
# Ansys Madrid office in Paseo de la Castellana.
#
# .. figure:: ../images/office1.jpg
#     :align: center
#     :alt: Madrid office
#     :figclass: align-center
#
#     Paseo de la Castellana Ansys office (Madrid).
#     Yes, we love coffee.
#
#
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

df.columns = ["MAX", "MIN"]  # renaming columns
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
# We see there are negative wind speed, probably because of the direction,
# since we are not interested in direction, only magnitude,
# let's use the absolute value then.
#
df = df.abs()

######################################################
# Let's plot it...
_ = df.plot(title="Wind speed per day")

########################################################
# As we can see, the most frequent maximum speeds are:
_ = df["MAX"].hist(bins=20)

########################################################
# As we can see, we could stablish there are two main peaks,
# one at 15 m/s and another at 33 m/s.
#
# Let's generate some random wind signal with those speeds.
# We are going to do a superposition of harmonics:
#

amplitude = [15, 33]
frequencies = (
    np.array([10, 16]) * 2 * np.pi
)  # Typical wind frequencies range between 2 and 20 Hz
phase = np.random.random(size=len(frequencies)) * 2 * np.pi


def wind_speed(t):
    sum_ = 0
    for each_amp, each_w, each_phase in zip(amplitude, frequencies, phase):
        sum_ = sum_ + each_amp * np.cos(each_w * t + each_phase)
    return sum_


t = np.arange(0, 1, 0.01)

plt.plot(t, wind_speed(t))
plt.show()


#############################################################
# To apply these velocities, we are going instead to convert it to acceleration
# using the following equation:
#
# .. math::
#
#    a = \omega * v
#
# where:
#
# * ``a`` is acceleration
# * ``w`` is frequency
# * ``v`` is velocity
#


def acceleration(t):
    sum_ = 0
    for each_amp, each_w, each_phase in zip(amplitude, frequencies, phase):
        sum_ = sum_ + each_amp * each_w * np.cos(each_w * t + each_phase)
    return sum_


plt.plot(t, acceleration(t))
plt.show()

################################################################################
# Now let's use that in our analysis
# We are going to apply a global acceleration using ``mapdl.acce``.

help(mapdl.acel)

#################################################################################
# Model solution
# ==============

mapdl.slashsolu()
mapdl.allsel()  # making sure all nodes and elements are selected.
mapdl.antype("TRANS")
mapdl.nsubst(carry="ON")

accelerations = acceleration(t)

for each_time, each_acceleration in zip(t[1:], accelerations):
    mapdl.time(each_time)
    mapdl.acel(acel_y=each_acceleration)
    mapdl.solve()


#################################################################################
# Post-processing
# ===============
#
# Let's see what we got. Let's print the displacements for the first step.
mapdl.post1()
mapdl.set(1, 1)
mapdl.post_processing.nodal_displacement("all")

######################################################
# and let's plot them
#
mapdl.post_processing.plot_nodal_displacement("y")

################################################################################
# We can follow this approach to get the results at each step
#
# For example let's get the maximum principal stresses and where it happens:

i = 0
max_stress_per_step = []
elem_max_stress_per_step = []

for step in mapdl.post_processing.time_values:
    i += 1
    mapdl.set(i)
    stresses = mapdl.post_processing.element_stress("1")  # First principal stresses
    max_stress_per_step.append(stresses.max())
    elem_max_stress_per_step.append(stresses.argmax())

max_stress_per_step = np.array(max_stress_per_step)
elem_max_stress_per_step = np.array(elem_max_stress_per_step)

elem_ = mapdl.mesh.enum[elem_max_stress_per_step[max_stress_per_step.argmax()]]
time_ = mapdl.post_processing.time_values[max_stress_per_step.argmax()]

print(
    f"The maximum principal stress\n\tValue: {max_stress_per_step.max():0.2f} Pascals."
)
print(f"\tAt the element {elem_}.")
print(f"\tAt the time {time_}.")


#################################################################################
# Post-processing time dependent results
# --------------------------------------
# Let's now check the displacement across time for a node in the tip
#
# We can get the nodes max and min coordenates as:
mapdl.post26()

nod_max = mapdl.mesh.nodes.max(axis=0)
nod_min = mapdl.mesh.nodes.min(axis=0)

coord_node = (nod_max[0] + nod_min[0]) / 2, (nod_max[1] + nod_min[1]) / 2, nod_max[2]

node = mapdl.queries.node(*coord_node)

################################################################################
# Getting the displacement at the tip

item = "U"
comp = "Y"
nvar = 9

# node_uy = mapdl.get_nsol(node, item, comp)  # Available in 0.62.3
mapdl.nsol(nvar, node, item, comp)
mapdl.vget("temp_", nvar)

node_uy = mapdl.parameters["temp_"]
time = mapdl.post_processing.time_values

plt.plot(time, node_uy)
plt.title("Displacement across time at the tip")
plt.show()

################################################################################


#################################################################################
# Closing session
# ===============
#
# Thank you all for your time and attention!
#
mapdl.exit()

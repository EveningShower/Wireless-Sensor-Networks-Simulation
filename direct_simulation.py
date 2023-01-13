#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import random
# Network Establishment Parameters

# Area of Operation
# Field Dimensions in meters
xm = 100
ym = 100

# Number of Nodes in the field
n = 100

# Number of Dead Nodes in the beginning
dead_nodes = 0

# Coordinates of the Sink (location is predetermined in this simulation)
sinkx = 0
sinky = -100

# Energy Values
# Initial Energy of a Node (in Joules)
Eo = 0.5  # units in Joules

# Energy required to run circuity (both for transmitter and receiver)
Eelec = 50 * 10 ** (-9)  # units in Joules/bit

# Transmit Amplifier Types
Eamp = 100 * 10 ** (-12)  # units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)


# Size of data package
k = 2000  # units in bits

# Round of Operation
rnd = 0

# Current Number of operating Nodes
operating_nodes = n
total_energy = 0
direct_operating_nodes = []
# Create the Wireless Sensor Network

# Initialize the properties of the node

nodes_property = np.array([
    (i, random.randint(0, xm), random.randint(0, ym), Eo, 
     1, 0, np.sqrt((random.randint(0, xm)-sinkx)**2 + (random.randint(0, ym)-sinky)**2))
    for i in range(1, n+1)
], dtype=[
    ('id', int),  # ID of the node
    ('x', int),   # x-coordinate of the node
    ('y', int),   # y-coordinate of the node
    ('E', float), # Initial energy of the node
    ('cond', int), # Condition of the node, 0 for dead, 1 for alive
    ('rop', int), # Round of operation
    ('dts', float) # Distance to sink
])

# Main Loop of the Direct Protocol

while operating_nodes > 0:
    for i in range(0, n):
        # check if node is still operating
        if nodes_property[i]["E"] > 0 and nodes_property[i]["cond"] == 1:
            # calculate energy dissipated by node i
            energy_spent = (Eelec + Eamp * nodes_property[i]["dts"]**2) * k
            nodes_property[i]["E"] -= energy_spent
            nodes_property[i]["rop"] += 1
            total_energy += energy_spent
            if nodes_property[i]["E"] <= 0:
                nodes_property[i]["cond"] = 0
                operating_nodes -= 1
    direct_operating_nodes.append((rnd, operating_nodes))
    rnd += 1
print(direct_operating_nodes)


# In[ ]:





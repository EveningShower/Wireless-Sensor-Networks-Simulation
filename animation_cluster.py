#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

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

# Suggested percentage of cluster head
p = 0.05  # a 5 percent of the total amount of nodes used in the network is proposed to give good results

# Set of nodes that haven't been cluster heads in the last 1/P rounds
G = set(range(0, n))

# Round of Operation
rnd = 0

# Current Number of operating Nodes
operating_nodes = n
transmissions = 0
total_energy = 0
# Create the Wireless Sensor Network

# Initialize the properties of the node

nodes_property = np.array([
    (i, random.randint(0, xm), random.randint(0, ym), Eo, 0, 0, 1, 0, 
     np.sqrt((random.randint(0, xm)-sinkx)**2 + (random.randint(0, ym)-sinky)**2), 0)
    for i in range(1, n+1)
], dtype=[
    ('id', int),  # ID of the node
    ('x', int),   # x-coordinate of the node
    ('y', int),   # y-coordinate of the node
    ('E', float), # Initial energy of the node
    ('role', int), # Role of the node, 0 for normal, 1 for cluster head
    ('cluster', int), # ID of the cluster the node belongs to
    ('cond', int), # Condition of the node, 0 for dead, 1 for alive
    ('rop', int), # Round of operation
    ('dts', float), # Distance to sink
    ('tel', int)  # Number of times the node was a cluster head
])

# Create a list to store the cluster history
cluster_history = []

# Append the initial cluster assignments to the history
cluster_history.append((0, nodes_property['cluster']))

# Main Loop of the LEACH Protocol

while operating_nodes > 0:
    nodes_property["role"] = 0
    nodes_property["dts"] = np.sqrt((random.randint(0, xm)-sinkx)**2 + (random.randint(0, ym)-sinky)**2)
    
    if G == set():
        G = set(range(0, n))

    # Determine the roles of the nodes (normal or cluster head) based on their energy levels and a probability value
    for i in range(0, n):
        if nodes_property[i]["E"] > 0 and nodes_property[i]["cond"] == 1:
            # Calculate the threshold value for node i
            if i in G:
                T = p / (1 - (p * (rnd % int(1/p))))
            else:
                T = 0
            # Compare the threshold value to a random number between 0 and 1
            if random.uniform(0,1) <= T:
                # Node i becomes a cluster head
                nodes_property[i]["role"] = 1
                nodes_property[i]["tel"] += 1
                G.remove(i)
    # Broadcast the advertisement of the cluster heads
    cluster_heads = nodes_property[nodes_property["role"] == 1]
    if len(cluster_heads) == 0: 
            # skip this iteration, as there are no cluster heads to join
            
            cluster_heads = nodes_property[nodes_property["role"] == 0]
        
    # assume symmetric propagation channels, 
    received_signal_strength = cluster_heads["E"] * (1 / cluster_heads["dts"])
    # Assign cluster ID to each node
    nodes_property["cluster"] = nodes_property["id"]
    for i in range(n):
        if nodes_property[i]['role'] == 0:
            # choose best cluster head to join 
            best_cluster = cluster_heads[np.argmax(received_signal_strength*(1/np.sqrt(((cluster_heads["x"] - nodes_property[i]["x"]) ** 2) + ((cluster_heads["y"] - nodes_property[i]["y"]) ** 2))))]["id"]

            # Assign cluster ID 
            nodes_property[i]["cluster"] = best_cluster

    # Data transmission phase
    for i in range(n):
        # Calculate the distance between each node and its cluster head
        if nodes_property[i]['role'] == 0 and nodes_property[i]["cond"] == 1:
            cluster_head_id = nodes_property[i]['cluster']
            cluster_head_index = np.where(nodes_property['id'] == cluster_head_id)[0][0]
            cluster_head_x = nodes_property[cluster_head_index]['x']
            cluster_head_y = nodes_property[cluster_head_index]['y']
            nodes_property[i]['dts'] = math.sqrt((cluster_head_x - nodes_property[i]['x'])**2 + (cluster_head_y - nodes_property[i]['y'])**2)

            # Calculate the energy dissipated by each node
            # Energy for transmission
            ETx = (Eelec * k + Eamp * nodes_property[i]['dts']**2 * k)
            nodes_property[i]['E'] -= ETx
            total_energy += ETx
            # if node i's energy depletes with transmission
            if nodes_property[i]["E"] <= 0: 
                nodes_property[i]["cond"] = 0
                nodes_property[i]["rop"] = rnd
                dead_nodes += 1
                operating_nodes -= 1
            # check if the cluster head of the node is operating
            if nodes_property[nodes_property[i]["cluster"]-1]["cond"] == 1:
                # calculate energy dissipated by the cluster head for reception
                nodes_property[nodes_property[i]["cluster"]-1]['E'] -= (Eelec) * k
                if nodes_property[nodes_property[i]["cluster"]-1]["E"] <= 0: 
                    nodes_property[nodes_property[i]["cluster"]-1]["cond"] = 0
                    nodes_property[nodes_property[i]["cluster"]-1]["rop"] = rnd
                    dead_nodes += 1
                    operating_nodes -= 1
        if nodes_property[i]["role"] == 1 and nodes_property[i]["cond"] == 1:
            # Calculate the energy required to transmit the data to the sink
            ETx = k * Eelec + k*Eamp*(nodes_property[i]["dts"]**2)
            # Calculate the energy required for data reception
            ERx = k * Eelec
            total_energy += ETx + ERx
            nodes_property[i]["E"] -= (ETx + ERx)
            if nodes_property[i]["E"] > 0:
                # Update the number of transmissions
                transmissions += 1
            else:
                nodes_property[i]["cond"] = 0
                nodes_property[i]["rop"] = rnd
                dead_nodes += 1
                operating_nodes -= 1
    # Increment the round of operation
    rnd += 1            
    # create new array with round number and cluster ID for each node
    round_clusters = np.array([rnd, np.copy(nodes_property["cluster"])])
    # append new array to cluster_history
    cluster_history.append(round_clusters)

cluster_history = cluster_history[:100]
def update(i):
    round_num, clusters= cluster_history[i]
    scat = plt.scatter(nodes_property['x'], nodes_property['y'], c=clusters, cmap='rainbow', s=100)
    plt.title(f"Round {round_num}")
    return scat,

fig, ax = plt.subplots(figsize=(1920/100, 1080/100))
ani = animation.FuncAnimation(fig, update, frames=len(cluster_history), interval=500, blit=True)
ani.save('animation.mp4', writer='ffmpeg')
plt.show()


# In[ ]:





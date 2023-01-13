#Wireless-Sensor-Networks-Simulation
This repository contains the simulation of the energy-efficient communication protocol for wireless microsensor networks presented in the paper "Energy-Efficient Communication Protocol for Wireless Microsensor Networks" by W. R. Heinzelman, A. Chandrakasan, and H. Balakrishnan.

#Included in this repository
Code for simulating the LEACH protocol
Code for simulating the Direct protocol
Code for animating the progress of clusters and how they change each round
Code for animating comparison between the lifetime of LEACH vs Direct protocols
#Requirements
Python3
NumPy
Matplotlib
#How to run the simulation
To run the simulation, simply run the leach.py file for the LEACH protocol or the direct.py file for the Direct protocol.
To run the animation of clusters progression, run the animation_cluster.py
To run the animation of lifetime comparison, run the animation_comparison.py
#Notes
The simulation and animations are set to run for a specific number of rounds, you can change it by changing the value in the while loop in the main function
The code uses random values for the initial position of nodes and energy, so the results may vary on each run
The code also uses random values for determining the cluster head, so the results may also vary on each run
#Output
The output of the simulation will be the number of operating nodes per round and total system energy dissipated
The output of the animation will be a visual representation of the progression of clusters and comparison between the lifetime of LEACH vs Direct protocols

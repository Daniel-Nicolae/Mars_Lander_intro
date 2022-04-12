# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import time

# Start the execution time count
start = time.time()

# mass, spring constant, initial position and velocity
m = 1
k = 1
x = 0
v = 1

# simulation time
t_max = 100
dt = 0.01
t_array = np.arange(0, t_max, dt)

# initialise empty lists to record trajectories
x_list = []
v_list = []

# First step of Verlet integration is still Euler
x_list.append(x)    # x[0]
v_list.append(v)    # v[0]
x = x + v*dt
x_list.append(x)    # x[1]

# Verlet integration
for t in t_array[1:]:

    # Find next position value
    x = 2*x-x_list[-2]-dt*dt*k*x/m
    x_list.append(x)    # x[i+1]

    # Find current velocity value
    v = (x-x_list[-3])/2/dt
    v_list.append(v)    #v[i]

# For the last i we still computed x[i+1], which is out of range so it's deleted
del x_list[-1]

# convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
x_array = np.array(x_list)
v_array = np.array(v_list)

# Execution time end, plot is not taken into account in order to compare with C++ time
end = time.time()
print("Execution time:", end-start)

# plot the position-time graph
plt.figure(1)
plt.clf()
plt.xlabel('time (s)')
plt.grid()
plt.plot(t_array, x_array, label='x (m)')
plt.plot(t_array, v_array, label='v (m/s)')
plt.legend()
plt.show()

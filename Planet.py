import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Select between an animated plot or a static one
# 0 = static 2D, 1 = animated 2D, 2 = static 3D
plot_type = 2
anim_speed = 100


# Select initial distance in km, initial speed in terms of the circular speed, number of steps and t_max in terms of the circular period
r0 = 10000
v = 0.8
T = 2         # for v<1, T=1 is more than one period, for v in (1, sqrt(2)), T=1 is less than one period
N = 10000      # bigger N and smaller T will give a more accurate plot. Careful, insability can cause the satellite to escape!

# Select unit vectors for the direction of the initial position and velocity
r_uv = [1, 0, 0]
v_uv = [0, 1, 0.3]


# Normalise the vectors
r_uv/=np.sqrt(np.sum(np.square(r_uv)))
v_uv/=np.sqrt(np.sum(np.square(v_uv)))


# Constants
M = 6.42*10**23
G = 6.67*10**(-11)

# Adjust values and simulate time
r0*=1000
v_circ = np.sqrt(G*M/r0)
t_max = 2*np.pi*np.sqrt(r0**3/G/M)*T
dt = t_max/N
t = np.arange(0, t_max, dt)


# Plot initialisation
if plot_type < 2 and v:
    plt.figure(1)
    plt.clf()
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.grid()
    plt.axis('equal')


# Coordinates arrays initialisation
position = np.zeros((N,3))
velocity = np.zeros((N,3))

# Initial position and velocity
position[0, :] = r0*r_uv
velocity[0, :] = v*v_circ*v_uv

# Verlet simulation
# Initial step is still semi-implicit Euler

# Find acceleration
r = np.sum(np.square(position[0, :]))
a = G*M*position[0, :]/np.power(r, 1.5)

# Update the first step
velocity[1, :] = velocity[0, :] - a*dt
position[1, :] = position[0, :] + velocity[1, :]*dt


for i in range(2,N):

    # For each next step find acceleration
    r = np.sum(np.square(position[i-1, :]))
    a = G*M*position[i-1, :]/np.power(r, 1.5)

    # Verlet integrator
    position[i, :] = 2*position[i-1, :] - position[i-2, :] - a*dt*dt    

    # Animation
    if plot_type == 1 and i % anim_speed == 0 and v:
        plt.cla()
        plt.grid()
        plt.plot(position[:i+1, 0], position[:i+1, 1], "c")
        plt.plot(position[0, 0], position[0, 1], "go")
        plt.plot(0, 0, "ro")
        plt.plot(position[i, 0], position[i, 1], "cd")
        plt.pause(0.000001)

# Static plot 2D
if plot_type == 0 and v:
    plt.plot(position[:, 0], position[:, 1], "c")
    plt.plot(position[0, 0], position[0, 1], "go")
    plt.plot(0, 0, "ro")
    plt.show()

# Static plot 3D
elif plot_type == 2 and v:
    fig = plt.figure()
    ax = plt.axes(projection ='3d')



    # This line should set the aspect ratio to equal
    X = position[:, 0]
    Y = position[:, 1]
    Z = position[:, 2]
    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')



    ax.plot(position[:, 0], position[:, 1], position[:, 2], color ='green')
    ax.plot(0, 0, 0, "ro")
    ax.plot(position[0, 0], position[0, 1], position[0, 2], "go")
    plt.show()

if not v:
    r_plot = []
    print(np.sqrt(np.sum(np.square(position[0, :]))))
    for i in range(len(t)):
        r_plot.append(np.sqrt(np.sum(np.square(position[i, :]))))
        
        if r_plot[-1] < 500000:
            break
    plt.plot(t[:len(r_plot)],r_plot)
    plt.xlabel('t (s)')
    plt.ylabel('altitude (m)')
    plt.grid()
    plt.show()






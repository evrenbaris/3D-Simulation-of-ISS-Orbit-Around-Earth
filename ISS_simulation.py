from skyfield.api import load
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from google.colab import files

# Load TLE data from CelesTrak
tle_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
satellites = load.tle_file(tle_url)
print(f"Loaded {len(satellites)} satellites")

# Select a satellite (Example: ISS)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']

# Create a time range
ts = load.timescale()
times = ts.utc(2024, 12, 29, range(0, 120, 5))  # More granular time steps

# Calculate satellite positions in 3D space
positions = [satellite.at(t).position.km for t in times]
x_coords = [pos[0] for pos in positions]
y_coords = [pos[1] for pos in positions]
z_coords = [pos[2] for pos in positions]

# Create a 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot Earth as a sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
earth_x = 6371 * np.outer(np.cos(u), np.sin(v))
earth_y = 6371 * np.outer(np.sin(u), np.sin(v))
earth_z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(earth_x, earth_y, earth_z, color='blue', alpha=0.6, edgecolor='black')

# Initialize the satellite's position
satellite_dot, = ax.plot([], [], [], 'ro', label='ISS')

# Labels and title
ax.set_title('3D Animation: ISS Orbit Around Earth')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
ax.legend()

# Animation function
def update(frame):
    satellite_dot.set_data([x_coords[frame]], [y_coords[frame]])
    satellite_dot.set_3d_properties([z_coords[frame]])
    return satellite_dot,

# Create animation
def init():
    satellite_dot.set_data([], [])
    satellite_dot.set_3d_properties([])
    return satellite_dot,

anim = FuncAnimation(fig, update, frames=len(x_coords), init_func=init, interval=100)

# Save animation as GIF
anim.save('simulation.gif', writer='pillow')

# Display the animation
HTML(anim.to_jshtml())

# Download the GIF
files.download('simulation.gif')

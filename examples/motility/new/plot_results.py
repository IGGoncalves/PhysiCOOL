import matplotlib.pyplot as plt

from physicool.processing import get_cell_data

variables = ["ID", "position_x", "position_y", "position_z"]
data = get_cell_data(timestep=0, variables=variables, output_path="temp")

print(data)

x_coordinates = [x for x in data["position_x"]]
z_coordinates = [y for y in data["position_y"]]
y_coordinates = [z for z in data["position_z"]]


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(z_coordinates, z_coordinates, z_coordinates, marker="o")
ax.set_xlim(-500,500)
ax.set_ylim(-500,500)
plt.show()
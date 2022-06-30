import matplotlib.pyplot as plt
import pandas as pd

from physicool.processing import get_cell_data

variables = ["ID", "position_x", "position_y", "position_z"]

values = []
for time in range(7):
    data = get_cell_data(timestep=time, variables=variables, output_path="temp")
    values.append(data)

new_data = pd.concat(values)

trajectories = [new_data[new_data["ID"] == cell_id][["position_x", "position_y", "position_z"]]
                for cell_id in new_data["ID"].unique()]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for cell in trajectories:
    ax.plot(cell["position_x"].values,
            cell["position_y"].values,
            cell["position_z"].values)

    ax.scatter(cell["position_x"].values[-1],
               cell["position_y"].values[-1],
               cell["position_z"].values[-1], marker="o")

ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
plt.show()

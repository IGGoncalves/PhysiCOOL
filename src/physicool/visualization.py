import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d
import seaborn as sns

def plot_heatmap(self, z_level):
    fig, axes = plt.subplots(2, 2, figsize=(8, 12))
    axes = axes.flatten()

    z_index = np.where(self.mesh[2] == z_level)

    for sub_index, ax in enumerate(axes):
        data = self.data[self.substances[sub_index]][z_index][0]
        max_value = data.max()
        sns.heatmap(
            data,
            ax=axes[sub_index],
            xticklabels=False,
            yticklabels=False,
            vmin=0,
            vmax=max_value,
            square=True,
            cmap="YlGnBu_r",
        )

        ax.set_title(f"Substance: {self.substances[sub_index]}")

    return fig, axes

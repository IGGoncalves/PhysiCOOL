import numpy as np

coords = np.asarray([[x, -450, 0, 0] for x in np.arange(-450, 450+1, 50)])
np.savetxt("config/cells.csv", coords, delimiter=",")
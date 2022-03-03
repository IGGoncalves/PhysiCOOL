# Multilevel parameter sweeps

PhysiCOOL implements a multilevel parameter sweep class that is aimed at identifying the parameters that best fit a target data set. The parameter sweep considers two PhysiCell parameters, and the user should provide an initial value for each of them. At each level, `MultiSweep` creates a search grid based on these two values, the number of points per direction and the percentage per direction. These values should be configured by the user.

The results for each simulation are compared to the target data and the error between both datasets is computed and stored. At the end of the level, the parameters that provided the minimum error value are selected as the center of the parameter exploration grid for the next level and the parameter bounds are updated accordingly. The number of levels can be defined by the user.

## Defining the MultiSweep class

```python
from physicool.optimization import MultiSweep

# Select the data to fit the model
target_data = ...

# Create our multisweep pipeline
number_of_levels = 2
points_per_direction = 5
percent_per_direction = 0.7

ms = MultiSweep(my_model, target_data,         
                n_levels=number_of_levels, 
                npdir=points_per_direction, 
                ppdir=percent_per_direction)

# Select initial value for the parameter sweep
ms.set_fit_value(2.0, 0.6)
ms.set_param_bounds((0, None), (0, 1))

# Run multisweep and get optimal parameters
x, y = ms.run_sweep()

print(f'Optimal value found: {x}; {y}')
```

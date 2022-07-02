# Multilevel parameter sweeps

PhysiCOOL implements a multilevel parameter sweep class that is aimed at identifying the parameters that best fit a target data set. The parameter sweep considers two PhysiCell parameters, and the user should provide an initial value for each of them. At each level, `MultiLevelSweep` creates a search grid based on these two values, the number of points per direction and the percentage per direction. These values should be configured by the user.

The results for each simulation are compared to the target data and the error between both datasets is computed and stored. At the end of the level, the parameters that provided the minimum error value are selected as the center of the parameter exploration grid for the next level and the parameter bounds are updated accordingly. The number of levels can be defined by the user.

## Defining the MultiSweep class

```python
from physicool.optimization import MultiLevelSweep

# Select the data to fit the model
target_data = ...
black_box = ...

# Create our multilevel sweep pipeline
number_of_levels = 2
points_per_direction = 5
percent_per_direction = 0.7

ms = MultiLevelSweep(black_box=black_box, target_data=target_data,         
                     n_levels=number_of_levels, 
                     points_dir=points_per_direction, 
                     percentage_dir=percent_per_direction,
                     parameters=["speed", "migration_bias"])

# Select parameter bounds for speed and bias, respectively
ms.set_param_bounds((0, None), (0, 1))

# Run multilevel sweep for initial point (speed=2.0, bias=0.6)
# Get optimal parameters
x, y = ms.run_sweep((2.0, 0.6))

print(f'Optimal value found: {x}; {y}')
```

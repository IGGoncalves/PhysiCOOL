# Using third-party libraries

Too cool for PhysiCOOL? Don't want to use our parameter sweep functions? We can still help you 😎

`PhysiCellBlackBox` will give you the black box you need to link pretty much any library you want to use to run parameter studies/calibration with PhysiCell through Python. The only thing you need to assure is that the input and output formats match!

## Example

Let's say you like using `psweep` and want to use it to call PhysiCell. `psweep` will takes as input some parameter values, which will be used to build a search grid, and a function that will be run for each parameter set. It also returns an output metric for each cell of the parameter grid. Thus, a `PhysiCellBlackBox` instance can be used to create an interface between `psweep` and `PhysiCell`.

```python
from physicool. optimization import PhysiCellBlackBox

# Create the black box model
PARAMS_UPDATER = ...
OUTPUT_PROCESSOR = ...
PC_MODEL = PhysiCellBlackBox(PARAMS_UPDATER,
                             OUTPUT_PROCESSOR)

def func(pset): 
    """
    Runs the black box model with the values selected by psweep.
    """
    metric = PC_MODEL.run(pset["bias"], pset["migration_bias"])
    return {'result': metric}

# Choose parameters
# (Creates a grid [["speed": 1.0, "bias": 0.2],
#                  ["speed": 1.0, "bias": 0.6]])
a = ps.plist('bias', [0.2, 0.6])
b = ps.plist('speed', [1.0])
params = ps.pgrid(a,b)

# Get a DataFrame with all the simulation results
# psweep will run func() with each pair of the params grid
df = ps.run_local(func, params)
df.head()
```

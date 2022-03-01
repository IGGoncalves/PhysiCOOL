# Using third-party libraries

Too cool for PhysiCOOL? Don't want to use our parameter sweep? We can still help you 😎

`PhysiCellBlackBox` will give you the black box you need to link pretty much any library you want to use to run parameter studies/calibration with PhysiCell through Python. The only thing you need to assure is that the input and output formats match!

Let's try an example for the motility study.

Let's say you like using `psweep` and want to use it to call PhysiCell. You have to consider that psweet will accept any type of output, but requires a specific type of input. It is basically a dictionary with not only the parameters we define at the start, but also a bunch of data such as the time at which the run happened, the savings directory,... We don't need all that!

So, we must create a new dictionary. It's pretty easy: just remove all the keys and values you don't need.

```python
def func(pset): 
    """Builds a parameter dictionary and runs the OptModel model with it."""
    
    params = {key: value
              for key, value in pset.items()
              if key in ['cell/speed', 'cell/migration_bias']}

    metric = my_model(params)
    return {'result': metric}

# Choose parameters
a = ps.plist('cell/speed', [1.0])
b = ps.plist('cell/migration_bias', [0.2, 0.6])
params = ps.pgrid(a,b)

# Define 
df = ps.run_local(func, params)
df.head()
```

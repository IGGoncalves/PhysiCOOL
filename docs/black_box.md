# Black-box models

PhysiCOOL allows users to create a black-box model with three main components:

- (i) A function that updates the PhysiCell configuration file with new input parameters values;
- (ii) The PhysiCell model;
- (iii) A function that reads the model outputs and computes the desired output metric.

These black-box models are modular in the sense that the users can select what functions to use to (i) update the 
configuration file and (ii) to process the results. For instance, users can decide to change the cells' motility 
parameters 
and evaluate the effect on the distance traveled by cells over time. Alternatively, the cell cycling rates could be 
varied to analyze the evolution of the number of cells.

It is not essential that both (i) and (iii) are defined in the black-box. Likewise, users can also  to create models 
composed only of the PhysiCell executable.

## Running PhysiCell models by themselves

The `PhysiCellBlackBox` can be run with just a PhysiCell executable, for example, to run multiple simulations and 
save the results to a tmp folder. To do this, the user should define the number of replicates to be run and if the
output files should be stored.

```python
from physicool.optimization import PhysiCellBlackBox

my_model = PhysiCellBlackBox(project_name="project")
my_model.run(number_of_replicates=3, keep_files=True)
```

## Configuration file updater functions

`PhysiCellBlackBox` can accept instances of the `ParamUpdater` class which read teh XML file, update some numerical 
values and then write the new values to the file. 
PhysiCOOL offers some built-in parameter updater functions to make things 
easier for users. For instance, if users want to update the cell motility data, they can create a `CellUpdater` that
reads the data from a given cell definition and, in this case, will use the `update_motility_values` function to update
the motility values and write them to the file. Alternatively, users could choose other updater functions, 
such as `update_volume_values`.

```python
from physicool.updaters import CellUpdater, update_motility_values

# Define motility parameters to be changed by update_motility_values
# (speed, persistence time and migration bias)
motility_updater = CellUpdater(config_path="output/PhysiCell_settings.xml",
                               updater_function=update_motility_values,
                               cell_definition_name="default")
```

Once the `CellUpdater` object is created, it can be passed to the `PhysiCellBlackBox`. Then, when we want to run our
model with updated values, we should pass in a dictionary with the new values we want to test.

```python
from physicool.optimization import PhysiCellBlackBox

motility_params = {"speed": 5.0, "persistence_time": 20.0, "migration_bias": 0.5}

my_model = PhysiCellBlackBox(project_name="project", updater=motility_updater)
my_model.run(params=motility_params, number_of_replicates=1, keep_files=True)
```

## Results processing functions

The results processing function should take in the path where the output files are stored and return either a 
NumPy array (e.g., the number of cells over time) or a float (e.g., the mean travelled distance by cells). In 
the example below, a processing function is defined to return the y-coordinates at a given time point.

```python
from physicool.processing import get_number_of_cells

my_model = PhysiCellBlackBox(processor=get_number_of_cells,
                             project_name="project")

number_of_cells = my_model.run()
```

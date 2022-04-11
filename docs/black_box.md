# Black-box models

## Configuration file updater functions

The configuration file updater should receive a list of parameter values and update the PhysiCell configuration accordingly. Thus, the user should define how these values are dealt with. The code below shows an example that takes in the first value from the passed list and assigns it to the cell speed parameter, and that takes in the second value and assigns it to the motility bias. The function should also write these values to the XML file.

```python
from physicool.config import ConfigFileParser

def params_updater(new_values):
    """
    Updates the cell speed and the migration bias.

    Parameters
    ----------
    new_values: list[float]
        The parameter values for (1) the cell speed,
        and (2) the migration bias.
    """
    cell_definition_name = "cancer"

    # Read the data from the file
    xml_parser = ConfigFileParser()
    cell_data = xml_parser.read_cell_data(cell_definition_name)

    # Update values
    cell_data.motility.speed = new_values[0]
    cell_data.motility.bias = new_values[1]
    xml_parser.update_params(cell_definition_name, cell_data)
```

## Results processing functions

The results processing function should take in the path where the output files are stored and return either a NumPy array (e.g., the number of cells through time) or a float (e.g., the mean travelled distance by cells). In the example below, a processing function is defined to return the y-coordinates at a given time point.

```python
import numpy as np
from physicool.processing import Cells


def output_processor(output_path):
    """
    Reads the output files and returns the y coordinates at a time point.

    Parameters
    ----------
    output_path: pathlib.Path
        The folder where the output files are stored.
    """
    # Get a reader for the cell data and extract the coordinates
    cells = Cells(time=10.0, storage_path=output_path)
    coordinates = cells.get_cell_positions()
    
    return np.array([coord[1] for coord in coordinates])
```

## Running the black box model

At this point, the black box model is ready to be built and run, which can be done with the `PhysiCellBlackBox` class. This class takes in as input the two functions previously described. The model can be run with the method `run`, that takes in as input the list of parameter values to study.

```python
from physicool.optimization import PhysiCellBlackBox

my_model = PhysiCellBlackBox(params_updater, output_processor)
my_model.run(params=[3.0, 0.5])
```

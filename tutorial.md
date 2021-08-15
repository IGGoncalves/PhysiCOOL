# Integrating PhysiCell into a Python parameter exploration pipeline

## Running a PhysiCell compiled file

It is possible to run shell commands through Python, using `subprocess`.

```python
import subprocess
command = './{project_name}'             # Linux/Mac
# command = '{project_name}.exe'         # Windows
subprocess.run(command, shell=True) 
```

This will allow you to run your project. However, you can also run more complex commands.

### Compiling files

```python
import subprocess
commands = '''
make {project_name}
make
./{project_name}
'''
subprocess.run(commands, shell=True) 
```

*Note: Be sure to change `./{project_name}` if you use Windows.*

### Running replicates

```python
import subprocess
number_of_replicates = 3
for _ in range(number_of_replicates):
    subprocess.run('./{project_name}', shell=True) 
```

*Note: Be sure to change `./{project_name}` if you use Windows.*

At this point, you will probably want to save your data to a new folder at each iteration so that it does not get overwritten.

### Storing output data

As a simple approach, after running a simulation, you can create a new directory and move all your data to that directory.

```python
import subprocess
commands = '''
mkdir new_dir
cp config/PhysiCell_settings.xml new_dir
mv output/* new_dir
'''
subprocess.run(commands, shell=True) 
```

Currently, PhysiCell does not save the initial parameter values into the output files. 
Thus, if you are modifying input parameters it is a good idea to save the `PhysiCell_settings.xml` file into each new directory.

However, this can lead to having a lot of folders with a large amount of data.

## Modifying the XML file

You will need to:

- Specify the value you want to change;
- Open the XML file;
- Search for the node that defines the parameter you want to vary;
- Write the value and saves the file.

As an example, let's assume we want to change the initial condition of a microenvironment substance. 

```python
from xml.etree import ElementTree as ET

attribute_value = '4.0'

# Variable definition
folder_name = "config/"
file_name = "PhysiCell_settings.xml"
substance_node = "microenvironment_setup/variable[@name='collagen']"
attribute_to_modify = substance_node + "/initial_condition"

# Read and update file
tree = ET.parse(folder_name + file_name)
tree.find(attribute_to_modify).text = attribute_value
tree.write(folder_name + file_name)
```

Of course, you can modify our Python file to adapt to any of the possible parameters. 

```python
me_variables = "microenvironment_setup/variable[@name='...']/..."
cell_variables = "cell_definitions/cell_definition[@name=...]/phenotype/..."
```

To simplify this process, use `pcxml`.

## Processing output data

To load variables into Python, you can use PhysiCell's Python loader, which loads all variables, or check `physipy.py`, to load some of the variables.

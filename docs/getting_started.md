# Getting started

This guide will help you install the system requirements to work with PhysiCOOL, which include [PhysiCell](http://physicell.org/) and Python. Besides, it will show you how to install PhysiCOOL and guide you through some of its use cases so that you can confirm that this package is working properly and learn some of its capabilities.

## System requirements

### Getting PhysiCell

PhysiCOOL is a Python library built to work with PhysiCell, an open-source, agent-based modelling framework for 3-D multicellular simulations. It is recommended that you use the latest PhysiCell version but older versions are supported.

You can clone or download the PhysiCell repository from [GitHub](https://github.com/MathCancer/PhysiCell). It may be necessary to install some additional software depending on the your OS. Video tutorials from the PhysiCell 2022 Workshop are available to set up PhysiCell for both Windows and MacOS:

- [Windows users](https://www.youtube.com/watch?v=hIP4JUrViRA)
- [MacOS users](https://www.youtube.com/watch?v=Sq9nfKS5U0E)

In these tutorials, two options are offered: the "minimal" and the "traditional" setups. PhysiCOOL only requires the minimal setup. However, if you are new to PhysiCell it is recommended with the "traditional" setup and watch the PhysiCell 2022 Workshop video tutorials.

Although these tutorials recommend users to install Python on their system by installing Anaconda, a more minimal available is available through Miniconda (see the following section for more details).

PDF versions of the setup process instructions can be found on [GitHub](https://github.com/physicell-training/ws2022/tree/main/setup) as well.

### Installing Python

Python can be installed by itself (follow the instructions [here](https://www.python.org/downloads/). Be sure to use a version supported by PhysiCOOL, i.e., `>=3.8` and `<3.11`).

However it is generally easier to install a Python distribution, such as Anaconda, which already includes tools and libraries that make it easier to get started coding in Python. A minimal version of Anaconda is also available, which does not include as many libraries as Anaconda, but is sufficient to work with PhysiCOOL.

- Getting [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
- Getting [Miniconda](https://docs.conda.io/en/main/miniconda.html)

Check out this [comparison between Anconda and Miniconda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/download.html#anaconda-or-miniconda) if you are unsure about which distribution to use.

#### Installing Jupyter (optional)

Jupyter notebooks are applications that contain both **code** that can be modified and executed and **text** elements. Therefore, they are commonly used to share reproduceable code and include detailed descriptions of how that code was implemented.

PhysiCOOL does not need to be run in Jupyter Notebooks and it can be used in Python (`.py`) scripts. Thus, it is not mandatory to install Jupyter in order to use this library. However, PhysiCOOL examples are available as Jupyter Notebooks that aim to explain the library's main use cases while allowing users to change the code and run it to see the impact of their changes. To run these examples locally, you will need to install Jupyter.

Anaconda already includes Jupyter, so if you installed Anaconda you are all set. However, if you installed Python by itself or used Miniconda, you need to install `jupyter`, which can be done using `pip`, the Python package installer. You can do this by running the following command:

```bash
pip install jupyter
```

## Installing PhysiCOOL

PhysiCOOL is available through pip using the following command:

```sh
pip install physicool
```

### Testing your PhysiCOOL installation

> Before testing PhysiCOOL, make sure that you are able to compile and run PhysiCell models in your local machine.

Now that PhysiCOOL is installed in your local machine, you can try some of its functionalities, including editing PhysiCell configuration files, running PhysiCell models and reading output data. 

#### Changing parameter values in the configuration file

- Open a terminal and navigate (`cd`) to your PhysiCell repository;
- Populate the PhysiCell folder with a sample model by calling `make template`;
- Open the `PhysiCell_settings.xml` file found in the `config` folder and check the values for the `persistence_time` and `use_2d` (check the `<motility>` data). (These values should be `1` and `true`, respectively, as of PhysiCell version 1.10.4);
- Create a script in the PhysiCell folder called `update_config.py` containing the code below. It will update the motility values of the PhysiCell configuration file;

```python
# Updates the motility speed and status values in the PhysiCell_settings.xml file.
from physicool.config import ConfigFileParser

if __name__ == "__main__":
    # Parse the data from the config file
    xml_data = ConfigFileParser()
    cell_data = xml_data.read_cell_data(name="default")
    # Update and write the new parameters to the config file
    cell_data.motility.speed = 20.0
    cell_data.motility.use_2d = False

    xml_data.write_motility_params(name="default", motility=cell_data.motility)
```

- Run the Python script by calling `python update_config.py` from your PhysiCell folder;
- Open the `PhysiCell_settings.xml` file and confirm that the `persistence_time` and `use_2d` values changed to `20` and `false`.

#### Compiling and running PhysiCell code

- Follow the instructions for the previous test;
- Create a script in the PhysiCell folder called `run_model.py` containing the code below. It will compile the PhysiCell code and run it.

```python
# Compiles the project, creates a black box object for it and runs it.
from physicool import optimization as opt

if __name__ == "__main__":
    opt.compile_project()
    my_model = opt.PhysiCellBlackBox(project_name="project")
    my_model.run()
```

- Run the Python script by calling `python run_model.py` from your PhysiCell folder;
- Open the `output` folder that it contains the output files for the simulation.

#### Reading results

- Follow the instructions for the previous test;
- Open the `PhysiCell_settings.xml` file found in the `config` folder and check the values for the `number_of_cells` (check the `<user_parameters>` data). (This value should be `5` as of PhysiCell version 1.10.4);
- Create a script in the PhysiCell folder called `read_cell_numbers.py` containing the code below. It will print the number of cells in each output file. **Warning**: If you are running a PhysiCell version below 1.10.3, change the version number in the code snippet to the version you are using.

```python
# Reads the number of cells in each output file and prints them.
from physicool.processing import get_cell_numbers_over_time

if __name__ == "__main__":
    cells = get_cell_numbers_over_time(version="1.10.4")
    print(cells)
```

- Run the Python script by calling `python read_cell_numbers.py` from your PhysiCell folder;
- Confirm that the first value is the same as the initial number of cells in the configuration file.

# PhysiCOOL: A generalized framework for model Calibration and Optimization Of modeLing projects

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/physicool)
![GitHub](https://img.shields.io/github/license/iggoncalves/PhysiCOOL)
[![Documentation Status](https://readthedocs.org/projects/physicool/badge/?version=latest)](https://physicool.readthedocs.io/en/latest/?badge=latest)
![Codecov](https://img.shields.io/codecov/c/gh/IGGoncalves/PhysiCOOL)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

**Latest tested PhysiCell version: 1.10.4**

PhysiCOOL is a Python library tailored to perform model calibration studies with [PhysiCell](https://github.com/MathCancer/PhysiCell). Using the PhysiCOOL package, PhysiCell projects can be converted into black-box models to characterize how simulation outputs change in response to variations in input values. PhysiCOOL takes advantage of Python's popularity and simplicity which makes PhysiCell models more accessible and enables users to integrate Python-based calibration tools with their PhysiCell workflows.

Although PhysiCOOL was designed to create full model calibration worfflows, its components can be used independently according to the users' needs. For instance,this novel package implements a file parser that enables users to read and write data to the PhysiCell XML configuration file using simple Python commands. Data validation is performed when new information is written to the files, assuring that the new values are consistent with PhysiCell's requirements and assumptions. Furthermore, PhysiCOOL also provides new functions to process and visualize simulation outputs which can be used for both parameter exploration and model calibration.

PhysiCOOL is available through pip using the following command:

```sh
pip install physicool
```


## Usage

- [Getting started](getting_started.md)
- [Configuration file parser](xml_update.ipynb)
- [Black box models](black_box.md)
- [Multilevel parameter sweep](multi_level.md)
- [Connecting to third-party packages](external_libs.md)
- [Examples](examples.md)


## Getting help

For usage questions, bug reports and suggested improvements, please open a new issue through the [GitHub "Issues" tab](https://github.com/IGGoncalves/PhysiCOOL/issues).


## Credits

`PhysiCOOL` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).


```{toctree}
:maxdepth: 1
:hidden:

getting_started.md
xml_update.ipynb
black_box.md
multi_level.md
external_libs.md
examples.md
changelog.md
autoapi/index
```

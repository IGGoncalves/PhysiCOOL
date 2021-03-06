# PhysiCOOL: A generalized framework for model Calibration and Optimization Of modeLing projects

![GitHub](https://img.shields.io/github/license/iggoncalves/PhysiCOOL)
[![Documentation Status](https://readthedocs.org/projects/physicool/badge/?version=latest)](https://physicool.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IGGoncalves/PhysiCOOL/HEAD?urlpath=%2Ftree%2Fexamples)

## Overview

PhysiCOOL is a Python library tailored to perform model calibration studies with [PhysiCell](https://github.com/MathCancer/PhysiCell). Using the PhysiCOOL package, PhysiCell projects can be converted into black-box models to characterize how simulation outputs change in response to variations in input values. PhysiCOOL takes advantage of Python's popularity and simplicity which makes PhysiCell models more accessible and enables users to integrate Python-based calibration tools with their PhysiCell workflows.

Although PhysiCOOL was designed to create full model calibration worfflows, its components can be used independently according to the users' needs. For instance,this novel package implements a file parser that enables users to read and write data to the PhysiCell XML configuration file using simple Python commands. Data validation is performed when new information is written to the files, assuring that the new values are consistent with PhysiCell's requirements and assumptions. Furthermore, PhysiCOOL also provides new functions to process and visualize simulation outputs which can be used for both parameter exploration and model calibration.

Check our [documentation](https://physicool.readthedocs.io) for some examples.

## Instalation

PhysiCOOL is available through pip using the following command:

```sh
pip install physicool
```

This package works with PhysiCell models up to and including PhysiCell v1.9.

## Usage

- [Configuration file parser](xml_update.ipynb)
- [Black box models](black_box.md)
- [Multilevel parameter sweep](multi_level.md)
- [Connecting to third-party packages](external_libs.md)

## Running examples

We currently offer an example that uses PhysiCOOL to study cell motility and the chemotactic response to oxygen gradients. All the files required to compile this PhysiCell model are available on our [GitHub repository](https://github.com/IGGoncalves/PhysiCOOL/tree/main/examples/motility). To run this analysis in a local machine, these files should be downloaded and physicool should be installed (through pip). Don't forget to make sure that Jupyter is also installed.

## Team

Tool developed by In??s Gon??alves, David Hormuth, Caleb Phillips, Sandhya Prabhakaran. Runner-up team of the "Best Tool" prize at [PhysiCell 2021 Workshop & Hackaton](http://physicell.org/ws2021/#apply). GO TEAM 7!

## Credits

`PhysiCOOL` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).


```{toctree}
:maxdepth: 1
:hidden:

xml_update.ipynb
black_box.md
multi_level.md
external_libs.md
changelog.md
autoapi/index
```

![GitHub](https://img.shields.io/github/license/iggoncalves/PhysiCOOL)
[![Documentation Status](https://readthedocs.org/projects/physicool/badge/?version=latest)](https://physicool.readthedocs.io/en/latest/?badge=latest)

# PhysiCOOL: A generalized framework for model Calibration and Optimization Of modeLing projects

PhysiCOOL aims to be a generalized framework for **model calibration in PhysiCell**. PhysiCell projects can be used a **black-box** to characterize how the model outputs change in response to variations in the input values. With this in mind, PhysiCOOL introduces a **model-agnostic calibration workflow** that easily integrates with PhysiCell models, and that allows users to **find the best set of parameters for their study**. 

PhysiCOOL provides new functions that allow users to easily specify the parameters to vary, as well as the metrics to be quantified (i.g., number of cells through time, total traveled distance,...). Currently, our algorithm relies on the existence of some target data, provided by the user, which will be used to fit the model. 

## Instalation
PhysiCOOL is available through pip. You can download it with the following command:

```sh
pip install physicool
```

## Usage
The `PhysiCellBlackBox` class creates a black-box function for your PhysiCell project. `PhysiCellBlackBox` **takes in a set of parameters**, **runs a PhysiCell simulation** with the updated parameter values and then **computes the metric you select** when initializing the model. It outputs an array with the values for the metric you choose.


## TBA: PhysiCOOL's multilevel parameter sweep

The `MultiSweep` class will let you run a **multilevel parameter sweep in which the parameter bounds are iteratively adapted based on the minimum value found at each level**. To create it, you must **select the model you want to run at each level** (our `OptModel` blackbox), as well as the **target data** you want to use.

Additionally, you can tune the **number of levels**, and the **number of points and ranges to explore at each level**. Additionally, you can define parameter bounds.

## Examples
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IGGoncalves/PhysiCOOL/docs?labpath=%2Ftree%2Fexamples)

You can run our examples on Binder! 

- **ODE toy model:**
Guides you through a simple example of logistic growth to showcase how the multilevel sweep works. (test it on Binder!)

- **Single-cell motility:**
Studies the effect of the migration bias and migration speed in the presence of a chemotactic gradient.

- **Cell growth:**
Studies the effect of the cell cycling rates on population growth. It also introduces gradient-based approaches.

- **Data analysis and visualization:**
TBA

## Team

Tool developed by Inês Gonçalves, David Hormuth, Caleb Phillips, Sandhya Prabhakaran. Runner-up team of the "Best Tool" prize at [PhysiCell 2021 Workshop & Hackaton](http://physicell.org/ws2021/#apply). GO TEAM 7!

## Credits
`PhysiCOOL` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
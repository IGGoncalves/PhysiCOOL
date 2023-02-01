# Parameter study with a third-party library (psweep)

## Goal

Use `PhysiCOOL` to connect `PhysiCell` and [psweep](https://github.com/elcorto/psweep), a Python library built to run parameter studies. 

This example showcases how PhysiCOOL can be used to create optimization pipelines through the use of other third-party libraries that may include features not yet implemented in PhysiCOOL.

## Setup

The model used in this example is the same as that defined in the `motility` example. Please, see the `motility` folder for more information on the model implementation.

PhysiCell version 1.10.4 was used to write this example.

## Instructions

- If working on your local machine, make sure that your setup matches the system requirements to work with PhysiCOOL (more information can be found in the project [docs](https://physicool.readthedocs.io/en/latest/getting_started.html).

- Open and run the `third_party.ipynb` notebook. It will generate the executable file to run the project and populate a new `calc` folder with the psweep data and a `temp` folder with the model outputs.

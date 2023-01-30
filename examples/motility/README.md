# Single-cell motility optimization (considering chemotaxis)

## Goal

Predict the role of the **cell migration speed** and the **migration bias** to model single-cell chemotaxis.

## Setup

We define an **oxygen gradient** by setting a boundary condition with high oxygen levels at the top of the domain, 
and defining lower oxygen levels at the rest of the domain through the initial conditions. Thus, it is expected 
that **cells with a low migration bias will migrate randomly** (as shown in the image on the left), and **cells 
with higher migration bias will follow the generated gradient** (right image).

### Files needed to compile the PhysiCell project

The files found in this folder can be used to compile the PhysiCell project. The `custom` and `config` files specify the model described in the previous section while the remaining files are PhysiCell files needed to compile the project.

This project was written with Physicell v1.9.1.

### Notebooks

- `black_box.ipynb` Goes through how we can set up a PhysiCOOL black box to test this model;
- `optimization.ipynb` Implements a multilevel parameter sweep to find the parameter values that best replicate some
specific model initial conditions.

## Instructions

- If working on your local machine, make sure that your setup matches the system requirements to work with PhysiCOOL (more information can be found in the project [docs](https://physicool.readthedocs.io/en/latest/getting_started.html).

- Open the `black_box.ipynb` notebook and run it. It should compile your code and create an executable file called `project` in this folder. In addition, it should create a `temp` folder with the model results.

- Open and run the `sweeper.ipynb` notebook. It will generate some target data and then use the executable file created before to try and replicate this data by finding the best parameter values in an optimization routine.

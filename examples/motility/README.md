# Single-cell motility optimization (considering chemotaxis)

## Goal
Predict the role of the **cell migration speed** and the **migration bias** to model single-cell chemotaxis.

## Setup
We define an **oxygen gradient** by setting a boundary condition with high oxygen levels at the top of the domain, 
and defining lower oxygen levels at the rest of the domain through the initial conditions. Thus, it is expected 
that **cells with a low migration bias will migrate randomly** (as shown in the image on the left), and **cells 
with higher migration bias will follow the generated gradient** (right image).

## Files needed to compile the PhysiCell project
The `custom` files found in this repository can be used to compile the PhysiCell project. The `config` files should be 
used to run the simulations.

## Notebooks

- `black_box.ipynb` Goes through how we can set up a PhysiCOOL black box to test this model;
- `optimization.ipynb` Implements a multilevel parameter sweep to find the parameter values that best replicate some
specific model initial conditions.
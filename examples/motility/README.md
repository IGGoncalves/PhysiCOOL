# Single-cell motility optimization (considering chemotaxis)

## Goal
Predict the role of the **cell migration speed** and the **migration bias** to model single-cell chemotaxis.

## Setup
We define a oxygen gradient by setting a boundary condition with high oxygen levels at the top of the domain, and defining lower oxygen levels at the rest of the domain through the initial conditions.
We consider a set of 2D replicates inside of each simulation. Each cell is placed at a defined height value inside of a 3D domain domain, but only 2D migration and 2D are enabled.

## Files needed to compile the PhysiCell project
The `custom` files found in this repository can be used to compile the PhysiCell project. The `config` file should be used to run the simulations.
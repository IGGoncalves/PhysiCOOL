# Getting started

## System requirements

PhysiCOOL is a Python library built to work with [PhysiCell](https://github.com/MathCancer/PhysiCell), an open-source, agent-based modelling framework for 3-D multicellular simulations. Accordingly, users must have Python installed on their local machine and download PhysiCell. Instructions on how to do this are provided below.

### Getting PhysiCell

PhysiCell is available online on [GitHub](https://github.com/MathCancer/PhysiCell). Users can clone or download the repository, but it may be necessary to additionally install some software depending on the user's OS. PhysiCell video tutorials are available to set up PhysiCell for both Windows and MacOS:

- [Windows users](https://www.youtube.com/watch?v=hIP4JUrViRA)
- [MacOS users](https://www.youtube.com/watch?v=Sq9nfKS5U0E)

In these tutorials, two options are offered: the "minimal" and the "traditional" setups. PhysiCOOL only requires the minimal setup. In addition, although users can follow these tutorials to install Python on their system by installing Anaconda, a more minimal distribution is available through Miniconda.

PDF versions of the setup process instructions can be found on [GitHub](https://github.com/physicell-training/ws2022/tree/main/setup) as well.

### Installing Python



### Installing Jupyter (optional)

## Installing PhysiCOOL

PhysiCOOL is available through pip using the following command:

```sh
pip install physicool
```

## Running examples

PhysiCOOL provides two main examples of how it can be used to perform calibration studies with PhysiCell:

- **Single-cell motility calibration study:**
Turning a PhysiCell model into a black-box that can be updated through Python + finding the best parameter values to model motility in the presence of a chemotactic gradient.

- **Third-party libraries:**
Using a third-party library ([psweep](https://github.com/elcorto/psweep)) to run parameter studies. Serves as an example of how PhysiCOOL can be integrated into a Python-based workflow to connect PhysiCell and other optimization libraries.

Additional examples:

- **Interactive parameter estimation example:**
A simple example of logistic growth (not written in PhysiCell) to showcase the multilevel sweep feature. Demonstrates the implementation of the `MultiLevelSweep` class so that users can understand how it is defined.

- **Data analysis and visualization:**
Examples of data visualization scripts, including interactive examples with Jupyter Widgets.

- 🏗️ **Cell growth (under development):**
Finding the best parameter values for cell cycling rates to model population growth. It also introduces 
gradient-based approaches. Code is available but this example has not been tested and depends on an older version of PhysiCOOL.

More information on each example can be found in the `README.md` files and their corresponding notebooks.

### Online testing

To test PhysiCOOL without installing any of the required libraries or downloading PhysiCell files, visit the [PhysiCOOL Gitpod environment](https://gitpod.io/##https://github.com/IGGoncalves/PhysiCOOL) and navigate to the `examples` folder.

### Local testing

For testing the examples on a local machine, download the `examples` folder from the PhysiCOOL GitHub repository.

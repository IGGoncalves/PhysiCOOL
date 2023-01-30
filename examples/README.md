# Running examples

PhysiCOOL provides two main examples of how it can be used to perform calibration studies with PhysiCell. All the files required to compile this PhysiCell model are available on our [GitHub repository](https://github.com/IGGoncalves/PhysiCOOL/tree/main/examples/).


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

## Running examples online

Examples can be run on Gitpod with a pre-defined environment that includes all the libraries and system requirements to run the examples available as Jupyter Notebooks. To test PhysiCOOL without installing any of the required libraries or downloading PhysiCell files, visit the [PhysiCOOL Gitpod environment](https://gitpod.io/##https://github.com/IGGoncalves/PhysiCOOL) and navigate to the `examples` folder.

## Running examples locally

> Be sure to install all the system requirements (PhysiCell, Python, PhysiCOOL and Jupyter Notebooks) before running examples locally. See the [Getting Started page](getting_started.md) for more info.

To run the examples on a local machine, download the `examples` folder from the PhysiCOOL GitHub [GitHub repository](https://github.com/IGGoncalves/PhysiCOOL/tree/main/examples/). Subsequently, run the command `jupyter notebook` from that directory to launch Jupyter and you can then run the examples.

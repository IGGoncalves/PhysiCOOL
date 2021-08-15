# Parameter studies with PhysiCell and Python

Once you have a compiled PhysiCell file, you can use it as a **black box** to see how the model changes in response to variations in the input values.

In this repository, we present some Python-based routines that you can apply to your own research. We use publicly available libraries in our examples, but you can change the code to use your preferred tools.

TEAM 7!

## Basic workflow

For simple studies, it is possible to run studies by simply modifying the XML configuration file. 
You will then need to run the compiled PhysiCell file and store your data, which you can use to perform some data analysis.

![flowchart](img.png)

For more information on each of these steps, check out the `tutorial.md` file.

## Examples

### Parameter sweeping with `psweep`

`run_sweep` will show you how you can build a pipeline to run parameter studies using [psweep](https://pypi.org/project/psweep/) and `pcxml`. The workflow can be adapted to use other parameter testing algorithms.

## Using `pcxml`

`pcxml` will help you interact with the XML file. Basically, you won't have to remember the full strings for all the XML elements. 
You can use a simpler representation instead, and `pcxml` will convert it to the format used by the XML config file.

- **cell variables**: `cell/{parameter_name}`
- **microenvironment variables**: `me/{substance}:{parameter_name}`
- **custom variables** : `{parameter_name}`

Strings are fixed, except for the values between {}, which should be chosen to fit the parameters.

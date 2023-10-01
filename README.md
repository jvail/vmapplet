# VMAppleT

Apple tree simulation library using Markov chains based on StocaTree/MAppleT:
A [refactored and enhanced](./CHANGES.md) implementation of StocaTree. Original sources copied and modified from [openalea/incubator](https://github.com/openalea-incubator/MAppleT).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvail/vmapplet/master?urlpath=lab/tree/notebooks/simple_simulation.ipynb)


## Installation

A local conda/miniconda installation is required.
First clone/download the repository. The `mamba` install is optional but recommended.

### Install mamba

```sh
conda install mamba -n base -c conda-forge
```

### Create environment - with a development install of VMappleT

With the development (editable `-e .` see [environment file](binder/environment.yml)) install all changes in the source tree are directly available for execution
without requireing a new install. This is the recommended way to work with, extend and adjust the model.

```sh
mamba env create -f binder/environment.yml
# or
# conda env create -f binder/environment.yml
```

## Usage

### Notebooks

Run examples in Jupyter notebooks:

```sh
conda activate vmapplet
jupyter lab --notebook-dir=notebooks
```

### Terminal

Execute simulation from the command line:

```sh
conda activate vmapplet
python -m vmapplet vmapplet/data/simulation.toml out_folder
```

### Configuration and input data

There are several types of configuration files and inputs in the [data](./vmapplet/data) folder:

1. A simulation [settings file](./vmapplet/data/simulation.toml) in TOML format.
2. [Configuration files](./vmapplet/data/markov) for the parametrization of the Markov model in TOML format.

#### Simulation Options

Running a simulation requires an instance of class [`Options`](./vmapplet/options.py). It can be parameterized from a toml file and/or modified programatically:

```py
import toml
from vmapplet import Options

with io.open('simulation.toml') as file:
    options = Options(**toml.loads(file.read()))
```

An instance of Options contains already all relevant parameters with reasonable defaults that may be altered programatically:

```py
from vmapplet import Options

options = Options()
options.tree.phyllotactic_angle = -144.0
```

For units and defaults take a look the [`Options`](./vmapplet/options.py) class implementation.

#### Simulation

Next to the configuration files the [`Simulation`](./vmapplet/simulation.py) class is the main entry point for any
simulation run. The class is instantiated with a str (an unparsed TOML file) or an Instance of `Options` and an
optional path for any output files:

```py
from vmapplet import Simulation

simulation = Simulation(options=options, output_path='some_path')
```

The simulation is executed by passing the Simulation object to the `vmapplet.run` function:

```py
import vmapplet

vmapplet.run(simulation)
```

In a notebook context it is possibel to pass a second (optional) parameter i.e. an instance of a SceneWidget to render the 3D representation created from the [interpretation.lpy](./vmapplet/lpy/interpretation.lpy) L-System:


```py
from pgljupyter import SceneWidget
import vmapplet

widget = SceneWidget()
display(widget)
vmapplet.run(simulation, scene_widget=widget)
```

#### Output

_todo_
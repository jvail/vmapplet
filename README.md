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

```sh
mamba env create -f binder/environment.yml
# or
# conda env create -f binder/environment.yml
```

## Usage

### Jupyter Lab

```sh
conda activate vmapplet
jupyter lab --notebook-dir=notebooks
```

### Console Script

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

The second important set of files are parametrizations for the [Markov](./vmapplet/markov.py) class with the following (simplified) structure:

```toml
# year relative to the simulation's first year (0)
year = 1
# the length ('MEDIUM' or 'LONG') of a branch
length = 'LONG'

# probabilities per Zone + 1 (see Zone enums.py)
initial_probabilities = [1.0, ...]

# probabilities tabel with Zone + 1 rows and columns
transition_probabilities = [
    [0.0, ...],
]

# distribution tabel with Zone + 1 rows and columns
observation_distributions = [
    [1.0, ..., 0.0],
]

# One description of the occupancy distribution per Zone
[[occupancy_distributions]]
distribution = 'NEGATIVE_BINOMIAL'
parameter = 2.05633
probability = 0.519757
bounds = [4.0, +inf]
```

#### L-System

#### Output

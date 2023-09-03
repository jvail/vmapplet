# VMAppleT

A refactored and enhanced implementation of MAppleT/StocaTree. Original sources copied and modified from [openalea/incubator](https://github.com/openalea-incubator/MAppleT).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvail/vmapplet/master?urlpath=lab/tree/notebooks/simple_simulation.ipynb)


## Major changes compared to MAppleT/StocaTree

* Build system and dependencies: All outdated and unmaintained dependencies have been removed or replaced
* Modularization: The L-Py file has been splitted up into several smaller modules
* Markov: A Python implementation of the semi-hidden Markov chain
* Configuration: An extended simulation and a Markov model configuration file in toml format
* Jupyter integration: Run and visualize simulations in Jupyter lab notebooks

## Install

A local conda/miniconda installation is required.
First clone/download the repository. The `mamba` install is optional but recommended.

#### Install mamba

```sh
conda install mamba -n base -c conda-forge
```

#### Create environment - with a development install of VMappleT

```sh
mamba env create -f binder/environment.yml
# or
# conda env create -f binder/environment.yml
```

## Jupyter

```sh
conda activate vmapplet
jupyter lab --notebook-dir=notebooks
```

## Script

```sh
activate vmapplet
python -m vmapplet vmapplet/data/simulation.toml out_folder
```

# VMAppleT

A refactored implementation and maintenance release of MAppleT. Original sources copied and modified from [openalea/incubator](https://github.com/openalea-incubator/MAppleT).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvail/vmapplet/master?urlpath=lab/tree/notebooks/simple_simulation.ipynb)


## Requirements

A local conda/miniconda installation.

## Install

First clone/download the repository. The `mamba` install is optional but recommended.

#### Install mamba

```sh
conda install mamba -n base -c conda-forge
```

#### Create environment - with a development install of VMappleT

```sh
mamba env create -f binder/environment.yml
```

## Run Jupyter

```sh
activate vmapplet
jupyter lab --notebook-dir=notebooks
```

## Run script

```sh
activate vmapplet
python -m vmapplet vmapplet/data/simulation.toml
```

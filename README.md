# VMAppleT

MAppleT sources and openalea dependencies copied and modified are from openalea/incubator.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvail/vmapplet/master)

## Install

Only tested on debian 10.

#### Create Conda Environment

```sh
conda install mamba -n base -c conda-forge
mamba env create -f binder/environment.yml
```

#### Install

Install mamba

```sh
conda install mamba -n base -c conda-forge
```

Create environment (with a local install of VMappleT)

```sh
mamba env create -f binder/environment.yml
```

## Run Jupyter

```sh
activate vmapplet
jupyter lab --notebook-dir=notebooks
```

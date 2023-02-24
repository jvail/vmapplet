# VMAppleT

A refactored implementation and maintenance release of MAppleT. Original sources copied and modified from [openalea/incubator](https://github.com/openalea-incubator/MAppleT).

Major changes:

- support Python 3 and updated dependencies
- support Jupyter notebooks
- modularized L-Py files
- incorporates all dependencies previously hosted at [openalea/incubator](https://github.com/openalea-incubator)
- redesign of configuration files
- bug fixes, typing and linting

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvail/vmapplet/master)

## Install

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

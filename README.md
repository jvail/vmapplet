# VMAppleT - Test

MAppleT sources and openalea dependencies copied and modified are from openalea/incubator.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvail/vmapplet/master)

## Install

Only tested on debian 10.

#### Create Conda Environment

```sh
conda install mamba -n base -c conda-forge
mamba env create -f environment.yml
conda activate vmapplet
```

#### Install VMAppleT

Only a local dev install will work.

```sh
pip install -e .
```

## Run Jupyter

```sh
jupyter lab --notebook-dir=notebooks
```

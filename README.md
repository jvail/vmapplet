# VMAppleT - Test

MAppleT sources and openalea dependencies copied and modified are from openalea/incubator.


## Install

#### Create Conda Environment

```sh
conda install mamba -n base -c conda-forge
mamba env create -f environment.yml
conda activate vmapplet-test
```

#### Install VMAppleT

```sh
pip install -e .
```

## Run Jupyter

```sh
jupyter lab --notebook-dir=notebooks
```

Then click 'build' if jupyter lab asks for building the pgljupyter plugin ... then wait till done.

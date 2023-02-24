from setuptools import find_packages

from skbuild import setup

setup(
    name='vmapplet',
    version='0.1.0',
    packages=find_packages(),
    cmake_install_dir='vmapplet/tools/structure_analysis'
)

---
title: 'VMappleT : A virtual modeling environment for modular functional-structural simulations of apple trees'
tags:
  - Python
  - biology
  - FSPM
authors:
  - name: Frédéric Boudon
    affiliation: 1
  - name: Jan Vaillant
	  affiliation: 3
  - name: Evelyne Costes
	  affiliation: 2
affiliations:
  - name: CIRAD, UMR AGAP Institut, F-34398 Montpellier, France
    index: 1
  - name: French National Institute for Agriculture, Food, and Environment (INRAE)
    index: 2
  - name: Independent Researcher, France
    index: 3
date: 2 September 2023
bibliography: paper.bib
---

# Summary

VMAppleT is a functional-structural plant model (FSPM) for apple trees based on L-Systems in Python. It is a refactored and modernized implementation of MAppleT [@Costes:2008] with
support for running simulations in Jupyter notebooks. The mechanics, theoretic foundations and the application of MappleT are extensively described in [@Costes:2008].
VMAppleT focuses on improvements in accessibility, extensibility and customization of the model implementation to facilitate future research on apple tree FSPMs:

First of all the source code of MAppleT has been refactored and modernized to support Python 3.10 and to improve its readability and usability by applying both code linting and typing.
The installation procedure has been simplified by removing dependencies on 3rd party libraries and replacing native dependencies with custom Python implementations. Documentation and tests
included in the previous (MAppleT repository)[https://github.com/openalea-incubator/MAppleT] have been ported and extended wherever applicable.

A major shortcoming of MAppleT L-System was its monolithic structure making extensions difficult. This has been addressed by splitting the L-System into several modules. Those may now either be
customized individually, be entirely replaced by custom L-Systems or extended with additional models. The modularization is also helpful to comprehend the overall model mechanics and interaction of its
components.

The configuration and parameterization of a simulation has been simplified and ported to the widely used TOML format and corresponding Python dataclasses which implement the required parameters
and are initialized with reasonable defaults.

Supporting Jupyter notebooks by integrating Jupyter Lab including model visualization was another important goal of the reimplementation. This is particularly useful to provide users a straightforward
access and simple examples that can even be executed and viewed via binder [@Jupyter:2018] without requiring a local installation.

# Acknowledgements

This work was supported by the French National Research Agency under the Investments for the Future Program, referred as ANR-16-CONV-0004

# References

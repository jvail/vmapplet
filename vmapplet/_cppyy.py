import os
import pathlib

import cppyy

# initalize cppyy
cppyy.add_include_path(f'{os.environ["CONDA_PREFIX"]}/include')
cppyy.add_library_path(f'{os.environ["CONDA_PREFIX"]}/lib')
cppyy.include(pathlib.Path(__file__).parent.resolve() / 'optimization.h')
cppyy.load_library('pglmath')

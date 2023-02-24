import os
import cppyy

cppyy.add_include_path(f'{os.environ["CONDA_PREFIX"]}/include')
cppyy.add_library_path(f'{os.environ["CONDA_PREFIX"]}/lib')
cppyy.include(f'{__path__[0]}/optimization.h')
cppyy.load_library('pglmath')


def get_shared_data(path: str):
    return f'{__path__[0]}/data/{path}'


__all__ = [
    'Simulation',
    'Options'
]

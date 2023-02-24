import cppyy

# TODO: Add proper resource path
path = __path__[0]
cppyy.add_include_path(path + '/src')
cppyy.add_library_path(path + '/lib')
cppyy.include(path + '/markov.h')

cppyy.load_library('stat_tool')
cppyy.load_library('sequence_analysis')

from cppyy.gbl import (
    sequence_analysis,
    stat_tool,
    std
)

HiddenSemiMarkov = sequence_analysis.HiddenSemiMarkov
SemiMarkovIterator = sequence_analysis.SemiMarkovIterator
StatError = stat_tool.StatError
srand = std.srand

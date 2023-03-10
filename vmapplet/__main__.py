import sys
import io

from . import (
    Simulation,
    run
)


config_file_path = sys.argv[1]

with io.open(config_file_path) as file:
    simulation = Simulation(file.read())
    run(simulation)

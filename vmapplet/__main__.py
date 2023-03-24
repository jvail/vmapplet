import sys
import io

from . import (
    Simulation,
    run
)


config_file_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) > 2 else None

with io.open(config_file_path) as file:
    simulation = Simulation(file.read(), output_path)
    run(simulation)

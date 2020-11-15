#!/usr/bin/python3
import time

# Import custom modules
from . import pi_io
from .cycles.constants import DEFAULT_CYCLE, DEFAULT_CYCLE_NAME
from .cycles.cycles import exec_cycle
        
def run():
    try:
        print(f'Running with {DEFAULT_CYCLE_NAME} as first cycle.')
        # start the recursive function with a default cycle name
        exec_cycle(DEFAULT_CYCLE)

    except KeyboardInterrupt:
        print('Keyboard interrupt, stopping script.')
    finally:
        pi_io.cleanup()
        print('GPIO cleanup complete.')

    exit()

# Run if package run as script
if __name__ == '__main__':
    run()
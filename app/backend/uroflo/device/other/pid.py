'''
PID

Notes
- 

Documentation
- 

'''

import time
import numpy as np
from simple_pid import PID

pid = PID(1, 0.1, 0.05, setpoint=1)

# Assume we have a system we want to control in controlled_system
v = controlled_system.update(0)

while True:
    # Compute new output from the PID according to the systems current value
    control = pid(v)

    # Feed the PID output to the system and get its current value
    v = controlled_system.update(control)


def PID():
    pass


# PID
'''
use this lol
- https://simple-pid.readthedocs.io/en/latest/index.html

'''




if __name__ == '__main__':
    PID()
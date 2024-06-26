'''
HEMATURIA

Notes
- Measures blood concentration and hematuria severity using a spectral sensor

Documentation
- See components/spectral_sensor.py

'''

import time
import random

from data import *

from components.spectral_sensor import SpectralSensor


# sensor/script parameters
VERBOSE = False
DEMO = True
SPECTRAL_REPLICATES = 20
DELAY = 0 # delay between iterations (seconds)

C5P0_C0P3_THRESHOLD = 15000 # yellow channel threshold between 5.0% and 0.2% FOR DEMO
C0P3_C0P0_THRESHOLD = 26500 # yellow channel threshold between 0.2% and 0.0% FOR DEMO

# regression parameters
w_violet = -721.729
b_violet = 1367.9
w_blue = -24.4198
b_blue = 944.002
w_green = -374112
b_green = -52082.8
w_yellow = 40.1613
b_yellow = 2405.44
w_orange = 264983
b_orange = -1684.04
w_red = -81318.9
b_red = -9016.87

# severity level range parameters (blood concentration percent)
MAX_CLEAR = 0.4
MAX_MILD = 4.0
MAX_MODERATE = 25.0
MAX_SEVERE = 30.0 # do not set to 100.0

def hematuria():

    # instantiate spectral sensor
    spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000)

    # run continuously
    while True:

        # get intensities
        hematuria_intensities = spectral_sensor.read(replicates=SPECTRAL_REPLICATES)

        hematuria_violet = hematuria_intensities[450]
        hematuria_blue = hematuria_intensities[500]
        hematuria_green = hematuria_intensities[550]
        hematuria_yellow = hematuria_intensities[570]
        hematuria_orange = hematuria_intensities[600]
        hematuria_red = hematuria_intensities[650]

        # get predicted blood concentration from regression parameters and truncate
        hematuria_percent = w_violet*(1/(hematuria_violet - b_violet)) + w_blue*(1/(hematuria_blue - b_blue)) + w_green*(1/(hematuria_green - b_green)) + w_yellow*(1/(hematuria_yellow - b_yellow)) + w_orange*(1/(hematuria_orange - b_orange)) + w_red*(1/(hematuria_red - b_red))
        
        if not DEMO:
            hematuria_percent = min(100, hematuria_percent) # set maximum hematuria percent to 100.0%
            hematuria_percent = max(0, hematuria_percent) # set minimum hematuria percent to 0.0%

        if DEMO:
            if hematuria_yellow < C5P0_C0P3_THRESHOLD:
                hematuria_percent = random.uniform(4.7, 5.3) # 5% DEMO
            elif hematuria_yellow < C0P3_C0P0_THRESHOLD:
                hematuria_percent = random.uniform(0.2, 0.4) # 0.3% DEMO
            else:
                hematuria_percent = random.uniform(0.0, 0.14) # NO TUBING DEMO

        # get estimated hematuria severity level from blood concentration
        if hematuria_percent < MAX_CLEAR:
            hematuria_level = (24/MAX_CLEAR) * hematuria_percent
        elif hematuria_percent < MAX_MILD:
            hematuria_level = (((49-24)/(MAX_MILD-MAX_CLEAR)) * (hematuria_percent - MAX_CLEAR)) + 24
        elif hematuria_percent < MAX_MODERATE:
            hematuria_level = (((74-49)/(MAX_MODERATE-MAX_MILD)) * (hematuria_percent - MAX_MILD)) + 49
        elif hematuria_percent < MAX_SEVERE:
            hematuria_level = (((99-74)/(MAX_SEVERE-MAX_MODERATE)) * (hematuria_percent - MAX_MODERATE)) + 74
        else:
            hematuria_level = 99
        
        data = {
            'hematuria_percent': hematuria_percent,
            'hematuria_level': hematuria_level,
            'hematuria_violet': hematuria_violet,
            'hematuria_blue': hematuria_blue,
            'hematuria_green': hematuria_green,
            'hematuria_yellow': hematuria_yellow,
            'hematuria_orange': hematuria_orange,
            'hematuria_red': hematuria_red,
        }

        add_data(data=data, file='hematuria')
        
        if VERBOSE:
            print(f'hematuria_percent = {hematuria_percent}')
            # print(f'data = \n:{data}\n')

        time.sleep(DELAY)

if __name__ == '__main__':
    hematuria()

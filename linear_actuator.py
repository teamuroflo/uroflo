'''
LINEAR ACTUATOR

Notes
- For inflow rate control

- L298N driver
- 12 V linear actuator (2 in stroke, 0.4 in/s, 1460 N / 330 lb)

- Recommend PWM freq = 1000

- Pin allocation:
  PIN 19 (GPIO 10), PIN 21 (GPIO 9), PIN 23 (GPIO 11), PIN 25 (Ground)

Documentation
- Guide: https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

'''

import time
import RPi.GPIO as GPIO
import os


class LinearActuator():
    def __init__(self, en_pin, in1_pin, in2_pin, freq=1000, verbose=False):
        self.en_pin = en_pin # GPIO enable pin (BCM)
        self.in1_pin = in1_pin # GPIO input pin 1 (BCM)
        self.in2_pin = in2_pin # GPIO input pin 2 (BCM)

        self.FREQ = freq # PWM frequency

        self.verbose = verbose # toggles printing of information to terminal

        self.setup()

    def setup(self):
        print("LinearActuator: setup")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # BCM mode

        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)

        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

        self.pwm = GPIO.PWM(self.en_pin, self.FREQ) # start PWM
        self.pwm.start(100)
    
    # stop movement
    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

    # extend/move forward
    def extend(self, duty_cycle=100, duration=0):
        if self.verbose:
            print(f"LinearActuator: extend (duty_cycle = {duty_cycle}, duration = {duration})")

        if (duty_cycle < 20) or (duty_cycle > 100):
            raise Exception("LinearActuator: duty_cycle must be in [20, 100]")
        
        self.pwm.ChangeDutyCycle(duty_cycle) # set speed via duty cycle

        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)

        time.sleep(duration)
        self.stop()

    # retract/move backward
    def retract(self, duty_cycle=100, duration=0):
        if self.verbose:
            print(f"LinearActuator: retract (duty_cycle = {duty_cycle}, duration = {duration})")

        if (duty_cycle < 20) or (duty_cycle > 100):
            raise Exception("LinearActuator: duty_cycle must be in [20, 100]")
        
        self.pwm.ChangeDutyCycle(duty_cycle) # set speed via duty cycle

        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

        time.sleep(duration)
        self.stop()

    def shutdown(self):
        print(f"LinearActuator: shutdown")
        self.stop()
        GPIO.cleanup()


# example implementation
if __name__ == '__main__':
    os.chdir('..') # change current directory
    
    linear_actuator = LinearActuator(en_pin=10, in1_pin=9, in2_pin=11, freq=1000, verbose=True) # use pin numbering (BCM) (NOT GPIO numbering)
    time.sleep(2) # wait for setup

    linear_actuator.retract(duty_cycle=100, duration=4)
    linear_actuator.extend(duty_cycle=100, duration=8)
    
    print("FULLY OCCLUDED")
    time.sleep(4)

    for i in range(1000):
        input("PRESS ENTER TO INCREASE FLOW")
        print(f"COUNT = {i+1}")
        linear_actuator.retract(duty_cycle=100, duration=0.01)
        time.sleep(0.5)
    
    linear_actuator.shutdown()

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
import curses
import sys
import termios
import tty


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


def user_input(prompt):
    stdscr = curses.initscr()
    # curses.noecho()
    stdscr.keypad(True)

    try:
        # stdscr.addstr(prompt)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP:
                return 'up'
            elif key == curses.KEY_DOWN:
                return 'down'
            
    finally:
        curses.endwin()

def get_single_char_input(prompt):
    print(prompt, end='', flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    single_char = get_single_char_input("Enter a single character: ")
    print("\nYou entered:", single_char)

# example implementation
if __name__ == '__main__':
    main()
    os.chdir('..') # change current directory
    user_input = input("Enter something: ")
    print("You entered:", user_input)

    linear_actuator = LinearActuator(en_pin=10, in1_pin=9, in2_pin=11, freq=1000, verbose=True) # use GPIO numbering (BCM) (NOT pin numbering)
    time.sleep(2) # wait for setup

    # occlude tubing
    linear_actuator.retract(duty_cycle=100, duration=4)
    linear_actuator.extend(duty_cycle=100, duration=8)
    print("NOTE: fully occluded")
    
    # adjust compression
    INCREMENT_SIZE = 0.01 # can try 0.005 or 0.001
    print(f"INCREMENT_SIZE = {INCREMENT_SIZE}")
    up = 0
    down = 0

    while True:
        input = user_input(f"INPUT: press UP or DOWN")
        if input == 'up':
            up += 1
            print(f"up count = {up}")
            print(f"down count = {down}")
            linear_actuator.retract(duty_cycle=100, duration=INCREMENT_SIZE)
        elif input == 'down':
            down += 1
            print(f"up count = {up}")
            print(f"down count = {down}")
            linear_actuator.extend(duty_cycle=100, duration=INCREMENT_SIZE)
        elif input == 'esc':
            break
        else:
            print("ERROR: invalid input")
        time.sleep(0.5)
    
    linear_actuator.shutdown()

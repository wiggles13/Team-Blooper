#setup
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

A1in = 22
A2in = 10 
B1in = 9 
B2in = 11

GPIO.setup(A1in, GPIO.OUT)
GPIO.setup(A2in, GPIO.OUT)
GPIO.setup(B1in, GPIO.OUT)
GPIO.setup(B2in, GPIO.OUT)

#dispenses ice- takes string as argument to determing amount of ice
def dispense():
    pass
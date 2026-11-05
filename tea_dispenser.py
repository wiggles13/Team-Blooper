import RPi.GPIO as GPIO
from time import sleep

pin = 1 #placeholder GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

#dispenses tea - if we have multiple pumps will take string flavor as argument
#takes an argument time as int
def dispense(time):
    GPIO.output(pin, GPIO.HIGH)
    sleep(time)
    GPIO.output(pin, GPIO.LOW)
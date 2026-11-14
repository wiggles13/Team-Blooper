import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#dispenses tea - if we have multiple pumps will take string flavor as argument
#takes an argument time as int
def dispense(time, pump):
    if pump == 1:
        pin = 13
    if pump == 2:
        pin = 19
    if pump == 3:
        pin = 26
    GPIO.output(pin, GPIO.HIGH)
    sleep(time)
    GPIO.output(pin, GPIO.LOW)
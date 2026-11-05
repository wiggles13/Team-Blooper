#setup
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

time_for_rotation = 2 #adjust time, in seconds
A1in = 1 #placeholder GPIO pins
A2in = 2 #placeholder GPIO pins
B1in = 3 #placeholder GPIO pins
B2in = 4 #placeholder GPIO pins

GPIO.setup(A1in, GPIO.OUT)
GPIO.setup(A2in, GPIO.OUT)
GPIO.setup(B1in, GPIO.OUT)
GPIO.setup(B2in, GPIO.OUT)

def set_coil(a1, b1, a2, b2):
    GPIO.output(A1in, a1)
    GPIO.output(A2in, a2)
    GPIO.output(B1in, b1)
    GPIO.output(B2in, b2)
#intial values do not change steps_per_rev, direction 1=clockwise -1=counterclocwise
steps_per_rev = 400
revs = .25
rpm = 1/(time_for_rotation*4/60)
direction = 1

#calculations
delay = 60/(steps_per_rev*rpm)
total_steps = revs*steps_per_rev

#rotates 90 degrees clockwise
def rotate():
    state = 0
    set_coil(1, 0, 0, 0)
    for i in range(total_steps):
        state = (state+direction)%8
        if state == 0:
            set_coil(1, 0, 0, 0)
        if state == 1:
            set_coil(1, 1, 0, 0)
        if state == 2:
            set_coil(0, 1, 0, 0)
        if state == 3:
            set_coil(0, 1, 1, 0)
        if state == 4:
            set_coil(0, 0, 1, 0)
        if state == 5:
            set_coil(0, 0, 1, 1)
        if state == 6:
            set_coil(0, 0, 0, 1)
        if state == 7:
            set_coil(1, 0, 0, 1)
        time.sleep(delay)
    set_coil(0, 0, 0, 0)
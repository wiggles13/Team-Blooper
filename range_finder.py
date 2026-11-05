import time
import RPi.GPIO as GPIO


Trig = 1    #placeholder GPIO pins
Echo = 2    #placeholder GPIO pins
dist_min = 3 #placeholder min distance a cup should be detected at (cm)
dist_max = 4 #placeholder max distance a cup should be detected at (cm)
Max_Echo = .025    #max reliable data point

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo, GPIO.IN)

#only returns when range finder detects something within the specified range
#must pass three checks to prevent random error from giving a false positive
#returns error if 10 seconds pass detecting a cup.
def detect_range():
    count = 0
    start = time.perf_counter()
    while count<3:
        time_dist = echo_time()
        if time_dist is not None:
            dist = time_dist*34300/2
            if dist>dist_min and dist<dist_max:
                count+=1
        if (time.perf_counter-start)>10:
            raise Exception("cup not found in 10 seconds") 

        

#sends pulse and returns time until it returns or none if bad data
def echo_time():
    if GPIO.input(Echo) == 1:
        return None
    GPIO.output(Trig, GPIO.HIGH)
    time.sleep(10e-6)
    GPIO.output(Trig, GPIO.LOW)
    t_trig = time.perf_counter()
    start = t_trig
    end = t_trig
    while GPIO.input(Echo) == 0:
        pass
    start = time.perf_counter()
    while GPIO.input(Echo) == 1: 
        pass
    end = time.perf_counter()
    width = end-start
    if width <=0 or width>Max_Echo:
        return None #bad data
    return width
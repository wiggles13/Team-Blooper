import time
import RPi.GPIO as GPIO


Trig = 14    #placeholder GPIO pins
Echo = 15    #placeholder GPIO pins
dist_min = 3 #placeholder min distance a cup should be detected at (cm)
dist_max = 5 #placeholder max distance a cup should be detected at (cm)
Max_Echo = .025    #max reliable data point


#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo, GPIO.IN)

#only returns when range finder detects something within the specified range
#returns error if 10 seconds pass detecting a cup.
def detect_range():
    count = 0
    start = time.perf_counter()
    while count<1:
        time_dist = echo_time()
        if time_dist is not None:
            dist = time_dist*34300/2
            if dist>dist_min and dist<dist_max:
                count+=1
        if (time.perf_counter()-start)>20:
            raise Exception("cup not found in 20 seconds")
        time.sleep(.5)

        

#sends pulse and returns time until it returns or none if bad data
def echo_time():
    if GPIO.input(Echo) == 1:
        return None
    GPIO.output(Trig, GPIO.HIGH)
    time.sleep(10e-6)
    GPIO.output(Trig, GPIO.LOW)
    err = time.perf_counter()
    while GPIO.input(Echo) == 0:
        if time.perf_counter()- err>.04:
            return None
    start = time.perf_counter()
    while GPIO.input(Echo) == 1: 
        pass
    end = time.perf_counter()
    width = end-start
    if width <=0 or width>Max_Echo:
        return None #bad data
    return width

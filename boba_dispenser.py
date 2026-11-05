


import time
import RPi.GPIO as GPIO

servo_pin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, 50) # 50 Hz signal

start_duty_cycle = 12.125 #ref angle = 0

#dispenses boba - will take string as argument for amount of boba
def dispense():
    pass


try:
    servo.start(start_duty_cycle)
    time.sleep(1)
    servo.stop()

    user_input = input("Enter angle of rotation (degrees): ")
    angle = float(user_input)

    duty_cycle = 0.05261168101530792 * angle + 7.390025114627762
    
    servo.start(duty_cycle)
    time.sleep(1)
    servo.stop()
    print("Servo moved to ", angle, "degrees")

finally:
    servo.stop()
    GPIO.cleanup()
    print("Servo PWM stopped.")
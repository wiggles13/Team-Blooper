#different files for all of the parts
import range_finder
import lazy_susan
from time import sleep
import threading

print(range_finder.echo_time()*34300/2)
lazy_susan.rotate()
sleep(.2)
lazy_susan.rotate()
sleep(.2)
lazy_susan.rotate()
sleep(.2)
#rotates back to start
motor_thread = threading.Thread(target=lazy_susan.reset_pos)
sensor_thread = threading.Thread(target=range_finder.stop_rotate)

motor_thread.start()
sensor_thread.start()

motor_thread.join()

print("done")


#different files for all of the parts
import rgb_sensor
import range_finder
import LED_strip
import lazy_susan
import boba_dispenser
import tea_dispenser
import ice_dispenser
from time import sleep

def payment():
    LED_strip.change_color()
    #try to detect a color
    try: 
        color = rgb_sensor.detect_color()
    except:
        LED_strip.clear()
        return 1 #a invalid color was detected
    return 0

def main(ice, boba, flavor):
    LED_strip.change_color()

    #try to detect presence of cup
    try: 
        range_finder.detect_range()
    except:
        LED_strip.clear()
        return 2 # a cup wasn't detected in 20 seconds

    LED_strip.change_color()

    #rotates then dispenses boba
    lazy_susan.rotate()
    boba_dispenser.dispense(boba)

    LED_strip.change_color()

    #rotates then dispenses tea
    lazy_susan.rotate()
    tea_dispenser.dispense(flavor)

    LED_strip.change_color()

    #rotates then dispenses ice
    lazy_susan.rotate()
    ice_dispenser.dispense(ice)

    LED_strip.change_color()

    #rotates back to start
    lazy_susan.rotate()

    LED_strip.rainbow()
    LED_strip.clear()
    return 0 # working as normal
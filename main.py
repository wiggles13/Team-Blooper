#different files for all of the parts
import rgb_sensor
import range_finder
import LED_strip
import lazy_susan
import boba_dispenser
import tea_dispenser
import ice_dispenser


#try to detect a color
try: 
    color = rgb_sensor.detect_color()
except:
    print("nonvalid color detected")
    quit()

LED_strip.change_color()

#try to detect presence of cup
try: 
    range_finder.detect_range()
except:
    print("cup not detected")
    quit()

LED_strip.change_color()

#rotates then dispenses boba
lazy_susan.rotate()
boba_dispenser.dispense()

LED_strip.change_color()

#rotates then dispenses tea
lazy_susan.rotate()
tea_dispenser.dispense()

LED_strip.change_color()

#rotates then dispenses ice
lazy_susan.rotate()
ice_dispenser.dispense()

LED_strip.change_color()

#rotates back to start
lazy_susan.rotate()

LED_strip.change_color()
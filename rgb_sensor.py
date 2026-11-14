import apds9960_color as apds

sensor = apds.APDS9960(gain=apds.GAIN_4X)

#uses rgb sensor to detect certain color values
#returns string of the detected color
#gives error if detects a different color than the set colors
def detect_color():
    return apds.name_color(sensor.read_rgb()[0])
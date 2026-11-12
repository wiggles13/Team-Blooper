import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30)

#pixels[led_number] = (0-255 R, 0-255 G, 0-255 B)  
#pixels.show() - makes the change happen
#pixls.fill(c, first, count) c-32 bit color value, first- first pixel, count-number of pixiles if only c will fill entire strip
#pixels.setBrightness)(c) c: 0-255 0 is off 255 is max

#takes a string as an argument
#changes the color depending on the inputed string
def change_color():
    pass

#clears the LED strip
def clear():
    #pixels[0] = (0, 0, 0) clear first pixel
    pixels.show()
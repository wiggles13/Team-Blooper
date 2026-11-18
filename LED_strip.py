import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30, brightness=1)

#pixels[led_number] = (0-255 R, 0-255 G, 0-255 B)  
#pixels.show() - makes the change happen
#pixls.fill(c, first, count) c-32 bit color value, first- first pixel, count-number of pixiles if only c will fill entire strip

#takes a string as an argument
#changes the color depending on the inputed string
def change_color(color):
    if color == "red":
        pixels.fill((255,0,0))
        pixels.show()
    elif color == "blue":
        pixels.fill((0,0,255))
        pixels.show()
    elif color == "green":
        pixels.fill((0,255,0))
        pixels.show()
    elif color == "yellow":
        pixels.fill((255,165,0))
        pixels.show()
    elif color == "orange":
        pixels.fill((245, 80, 0))
        pixels.show()
    elif color == "purple":
        pixels.fill((128, 0 ,128))
        pixels.show()
    elif color == "white":
        pixels.fill((255, 255, 255))
        pixels.show()


#clears the LED strip
def clear():
    pixels.fill((0, 0 ,0))
    pixels.show()

change_color("red")
time.sleep(3)
change_color("blue")
time.sleep(3)
change_color("green")
time.sleep(3)
clear()
#!/usr/bin/python

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time
import random
from dotstar import Adafruit_DotStar

numpixels = 20 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
# datapin   = 23
# clockpin  = 24
# strip     = Adafruit_DotStar(numpixels, datapin, clockpin)

# Alternate ways of declaring strip:
# strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)
strip   = Adafruit_DotStar(numpixels, 32000000) # SPI @ ~32 MHz
# strip   = Adafruit_DotStar()                    # SPI, No pixel buffer
# strip   = Adafruit_DotStar(32000000)            # 32 MHz SPI, no pixel buf
# See image-pov.py for explanation of no-pixel-buffer use.
# Append "order='gbr'" to declaration for proper colors w/older DotStar strips)

strip.begin()           # Initialize pins for output
strip.setBrightness(255) # Limit brightness to ~1/4 duty cycle

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

#colorStart = 0x9DFF00
#colorEnd = 0x00802D
colorStart = 0x9DFF00
colorEnd = 0xFF0000

redBeg = colorStart >> 16
redEnd = colorEnd >> 16
greenBeg = (colorStart >> 8) & 0xFF
greenEnd = (colorEnd >> 8) & 0xFF
blueBeg = colorStart & 0xFF
blueEnd = colorEnd & 0xFF
stepwidthRed = (redEnd - redBeg)/numpixels
stepwidthGreen = (greenEnd - greenBeg)/numpixels
stepwidthBlue = (blueEnd - blueBeg)/numpixels
list = []

colorList = []
for i in range(0, numpixels):
	list.append(i)
	strip.setPixelColor(i, 0)
	color = ((redBeg + i * stepwidthRed) << 16) | ((greenBeg + i * stepwidthGreen) << 8) | (blueBeg + i * stepwidthBlue)
	colorList.append(color)

strip.show()

random.shuffle(list)

for i in list:
	strip.setPixelColor(i, colorList[i]) # Turn on 'head' pixel
	strip.show()                     # Refresh strip
	time.sleep(1.0 / 10)             # Pause 20 milliseconds (~50 fps)

lastPos = 0
pos = 0
reverse = False
while True:
	strip.setPixelColor(lastPos, colorList[lastPos])
	strip.setPixelColor(pos, 0x0000FF)
	strip.show()
	lastPos = pos
	time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)
	if reverse:
		pos -= 1
	else:
		pos += 1
	if pos > 19:
		reverse = True
		pos = 19
	elif pos < 0:
		reverse = False
		pos = 0

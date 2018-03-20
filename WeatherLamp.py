import urllib,json

import RPi.GPIO as GPIO
import time
from  neopixel import *

import sys
import random

class Board:
# LED strip configuration:
    LED_COUNT      = 16      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor$
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
    ring = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP) 
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.ring.begin()
    def setPins(self,pins):
        for i in pins:
            if pins[i] is "OUT":
                GPIO.setup(i,GPIO.OUT)
            else:
                GPIO.setup(i,GPIO.IN)
    def setColor(self,r,g,b,LEDNumbers):
        for i in LEDNumbers:
            self.ring.setPixelColor(i,Color(r,g,b))
            self.ring.show()

class Weather:
    temp = 0
    rain = 0
    cloud = 0
    def __init__(self,t,r,c):
        self.temp=t
        self.rain=r
        self.cloud=c
    def findTotalRain(self,array):
        total = 0
        for x in array:
            total+=x.rain
        return total
    def findHighestCloudPercentage(self,array):
        max = 0
        for x in array:
            if (x.cloud > max):
                max=x.cloud
        return max

    def makeLightning(self,rain):
        if rain >= 2:
            b=Board()
            LEDs = []
            for _ in range(0,8):
                LEDs.append(random.randrange(1,16))
            b.setColor(139,0,139,LEDs)
            time.sleep(random.random())
            b.setColor(0,0,0,LEDs)
            time.sleep(random.random())



    def makeRain(self,rain):
        roundedRain = round(rain)
        dict = {0:0, 1:25, 2:50, 3:75, 4:100}
        rainVal = int((dict[roundedRain]))
        print('rain ', rainVal)
        # GPIO.PWM(7,rainVal)
    def makeClout(self,cloud):
        roundedClout = round(cloud)
        cloutVal = int(roundedClout)
        print('cloud', cloutVal)
        # GPIO.PWM(8,cloutVal)
    def makeTemp(self, temp):
        b=Board()
        LEDs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        minimum = -10.0
        maximum = 100.0
        ratio = ((temp-minimum)/(maximum - minimum))*2
        print(ratio)
        blue = int(max(0,255.0*(1-ratio)))
        red = int(max(0,255.0*(ratio - 1.0)))
        green = 255-red-blue
        print(ratio,red,blue,green)
        b.setColor(red,green,blue,LEDs)




class Data:
    def getData(self):
        key = "cf22c6d3079412ef13ed81f039297bc8"

        url = "http://api.openweathermap.org/data/2.5/forecast?&lat=43.15&lon=-77.62&APPID="+key+"&units=imperial"+"&cnt=4"

        success = False
        while (success==False):
            try:
                response = urllib.urlopen(url)
                success=True
            except:
                time.sleep(0.5)
                success=False

        try:
            dataResponse = json.loads(response.read())
        except:
            dataResponse=""
        return dataResponse

    def filterData(self,d):
        arr = []
        for x in data["list"]:
            temp = x["main"]["temp"]
            try:
                rain = x["rain"]["3h"]
            except:
                rain=0
            cloud = x["clouds"]["all"]
            r = Weather(temp,rain,cloud)
            arr.append(r)
        return arr


d = Data()
data = d.getData()
while data is "":
    data=d.getData()
x = d.filterData(data)
W = Weather(0,0,0)
W.cloud=W.findHighestCloudPercentage(x)
W.rain=W.findTotalRain(x)

W.makeRain(W.rain)
W.makeClout(W.cloud)

# print(W.rain)
# print(W.cloud)



b=Board()
pins = {18:"OUT"}
b.setPins(pins)
W.makeTemp(80.0)
try:
    print("Hello")
        # while True:

                # W.makeLightning(0)
                # time.sleep(random.randint(1,4))
except KeyboardInterrupt:
        print("INTERRUPT")
finally:
        GPIO.cleanup()

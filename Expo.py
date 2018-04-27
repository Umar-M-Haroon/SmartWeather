import urllib,json
import RPi.GPIO as GPIO
import time
from  neopixel import *
import sys
import random
from multiprocessing import Process

class Board:
# LED strip configuration:
    LED_COUNT      = 16      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor$
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
    ring = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    #initialize ring and board when the board class is initialized 
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.ring.begin()
        self.ring.show()
    #Setup pins and check whether they need to be output or input
    def setPins(self,pins):
        for i in pins:
            if pins[i] is "OUT" or pins[i] is "OUTPUT":
                GPIO.setup(i,GPIO.OUT)
            else:
                GPIO.setup(i,GPIO.IN)
    #Set the ring color by RGB and for what LED's in the ring
    def setColor(self,r,g,b,LEDNumbers):
        for i in LEDNumbers:
            self.ring.setPixelColor(i,Color(r,g,b))
            self.ring.show()


class Weather:
    temp = 0
    rain = 0
    cloud = 0
    #Initialize and set values
    def __init__(self,t,r,c):
        self.temp=t
        self.rain=r
        self.cloud=c
        b = Board()
        pins = {18:"OUT",2:"INPUT",4:"OUT",24:"OUT"}
        b.setPins(pins)
    #Find the toal inches of rain
    def findTotalRain(self,array):
        total = 0
        for x in array:
            total+=x.rain
        return total
    #Finds the highest cloud percentage in the data
    def findHighestCloudPercentage(self,array):
        max = 0
        for x in array:
            if (x.cloud > max):
                max=x.cloud
        return max
    
    def makeLightning(self,rain,tR,tG,tB):
        #only make lightning for if the rain is heavy
        if rain >= 2:
            #Setup board and get all 16 LEDs
            b=Board()
            LightningLEDs = []
            allLEDs = [i for i in range(16)]
            #Find 8 LED's to make purple for lightning and make the other 8 the temperature
            for _ in range(0,8):
                i = random.randrange(1,16)
                LightningLEDs.append(i)
                try:
                    allLEDs.remove(i)
                except:
                    continue
            b.setColor(139,0,139,LightningLEDs)
            b.setColor(tR,tG,tB,allLEDs)
            time.sleep(1)


    #Round the rain value so we can map it to the amount of power going through the pump, therefore limiting rain made
    def pumpHumidifierLevels(self,number,pin):
        for x in range (0,300):
            GPIO.output(pin,GPIO.HIGH)
            time.sleep(20*(number/25/3+.2))
            GPIO.output(pin,GPIO.LOW)
            time.sleep(2)

    def makeRain(rain):
        roundedRain = round(rain)
        values = {0:0, 1:25, 2:50, 3:75, 4:100}
        rainVal = int((values[roundedRain]))
        self.pumpHumidifierLevels(rainVal,4)
    #Same as makeRain but with cloud percentage
    def makeClout(cloud):
        roundedClout = round(cloud)
        cloutVal = int(roundedClout)
        self.pumpHumidifierLevels(cloutVal,20)
    def makeTemp(self, temp):
        #initialize board and setup LED array and max/min
        b=Board()
        LightningLEDs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        minimum = 40.0
        maximum = 90.0
        #edge case
        if temp < minimum:
            temp=minimum
        if temp > maximum:
            temp=maximum
        #algorithm to map red blue green. Once set, set color
        ratio = ((temp-minimum)/(maximum - minimum))*2
        blue = int(max(0,255*(1-ratio)))
        red = int(max(0,255*(ratio - 1)))
        green = 255-red-blue
        b.setColor(red,green,blue,LightningLEDs)
        return [red,green,blue]
#FIX BELOW
b=Board()
pins = {18:"OUT",2:"INPUT",4:"OUT",24:"OUT",20:"OUT"}
b.setPins(pins)


Ws=[Weather(20,1,25),Weather(40,2,50),Weather(60,3,75),Weather(90,4,100)]


def mainLoop(amt):
    Weather.makeRain(amt)

def secondLoop(amt):
    Weather.makeClout(amt)
try:
    while True:
        time.sleep(0.1)
        x = GPIO.input(2)
        e = False
        if x is 1:
            e = True
        if e:
            for k in range(4):
                Wi = Ws[k]
                Process(target=mainLoop,args=(Wi.rain,)).start()
                Process(target=secondLoop,args=(Wi.cloud,)).start()
                
                for _ in range(15):
                    temp = Wi.makeTemp(x[k].temp)
                    for j in range(20):
                        W.makeLightning(4,temp[0],temp[1],temp[2])
                        time.sleep(random.random())
                    time.sleep(1) 
except KeyboardInterrupt:
    print("INTERRUPTED")
finally:
    GPIO.cleanup()

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
    LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
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
    def pumpHumidifierLevels(self,number):

        for x in range (0,300):
            GPIO.output(4,GPIO.HIGH)
            time.sleep(number/25/3+.2)
            GPIO.output(4,GPIO.LOW)
            time.sleep(2)

    def makeRain(self,rain):
        roundedRain = round(rain)
        values = {0:0, 1:25, 2:50, 3:75, 4:100}

        rainVal = int((values[roundedRain]))
        self.pumpHumidifierLevels(rainVal)
    #Same as makeRain but with cloud percentage
    def makeClout(self,cloud):
        roundedClout = round(cloud)
        cloutVal = int(roundedClout)
        pumpHumidifierLevels(cloutVal)
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
class Data:
    def getData(self):
        #always run until it opens (This is to check its connected to the internet)
        key = "cf22c6d3079412ef13ed81f039297bc8"
        url = "http://api.openweathermap.org/data/2.5/forecast?q=Boulder&APPID="+key+"&units=imperial"+"&cnt=4"

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
        #Filter out unnecessary data like coordinates
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
#data request and initialize Weather data
d = Data()
data = d.getData()
while data is "":
    data=d.getData()
#initialize Weather class after filtering data so we can use weather functions
x = d.filterData(data)
W = x[0]
W.cloud=W.findHighestCloudPercentage(x)
W.rain=W.findTotalRain(x)



b=Board()
pins = {18:"OUT",2:"INPUT",4:"OUT",24:"OUT"}
b.setPins(pins)

# while True:
#     buttonData = GPIO.input(2)
#     buttonEnabled = False
#     while buttonData:
#         if buttonEnabled:
#             buttonEnabled = False
#         else:
#             buttonEnabled = True
#         time.sleep(2)
#     if buttonEnabled:
def mainLoop():
    while True:
        W.makeRain(4)
        time.sleep(1)
def secondLoop(c):
    while True:
        W.makeLightning(20,c[0],c[1],c[2])
        time.sleep(random.random())
if __name__ == '__main__':
    try:
        while True:
            t = W.makeTemp(40)
            Process(target=mainLoop).start()
            Process(target=secondLoop,args=t).start()
    except KeyboardInterrupt:
        print("INTERRUPTED")
    finally:
        GPIO.cleanup()

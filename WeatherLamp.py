import urllib,json
import RPi.GPIO as GPIO
import time
from  neopixel import *
import sys
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


class Data:
    def getData(self):
        key = "cf22c6d3079412ef13ed81f039297bc8"
        url = "http://api.openweathermap.org/data/2.5/forecast?&lat=43.15&lon=-$
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
print(W.rain)
print(W.cloud)



# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/$
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor$
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering






GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT)
GPIO.output(6,GPIO.HIGH)
ring = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP) 
ring.begin()

def theaterChase(strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
                for q in range(3):
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, 0)

try:
        while True:
                GPIO.output(6,GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(6,GPIO.LOW)
                time.sleep(0.5)
                theaterChase(ring, Color(127, 127, 127))  # White theater chase
                theaterChase(ring, Color(127,   0,   0))  # Red theater chase
                theaterChase(ring, Color(  0,   0, 127))  # Blue theater chase
except KeyboardInterrupt:
        print("INTERRUPT")
finally:
        GPIO.cleanup()

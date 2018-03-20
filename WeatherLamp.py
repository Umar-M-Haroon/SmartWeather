import urllib,json


import time


import sys
import random


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
            print("Rain is greater than 2, lets make lightning")


    def makeRain(self,rain):
        roundedRain = round(rain)
        dict = {0:0, 1:25, 2:50, 3:75, 4:100}
        rainVal = int((dict[roundedRain]))
        print('rain ', rainVal)

    def makeClout(self,cloud):
        roundedClout = round(cloud)
        cloutVal = int(roundedClout)
        print('cloud', cloutVal)

    def makeTemp(self, temp):

        b=Board()
        LEDs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        minimum = 20.0
        maximum = 90.0
        ratio = ((temp-minimum)/(maximum - minimum))*2
        blue = int(max(0,255*(1-ratio)))
        red = int(max(0,255*(ratio - 1)))
        green = 255-red-blue
        b.setColor(red,green,blue,LEDs)






class Data:
    def getData(self):
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
        for x in data["list"]:
            temp = x["main"]["temp"]
            print
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
W = x[0]
W.cloud=W.findHighestCloudPercentage(x)
W.rain=W.findTotalRain(x)

W.makeRain(W.rain)
W.makeClout(W.cloud)

# print(W.rain)
# print(W.cloud)





W.makeTemp(W.temp+30)

b=Board()
pins = {18:"OUT",12:"OUT"}
b.setPins(pins)


try:
    while True:
        # W.makeLightning(20)
        # W.makeTemp(W.temp)
        time.sleep(random.randint(1,4))
        p = GPIO.PWM(12,80000)
        p.start(100)
except KeyboardInterrupt:
        print("INTERRUPT")
finally:
        GPIO.cleanup()


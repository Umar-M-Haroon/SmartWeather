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

        minimum = -10.0
        maximum = 100.0
        ratio = ((temp-minimum)/(maximum - minimum))/2
        print(ratio)
        blue = int(max(0,255*(1-ratio)))
        red = int(max(0,255*(ratio - 1)))
        green = 255-red-blue
        print(ratio,red,blue,green)




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



W.makeTemp(80.0)

import urllib,json
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
        url = "http://api.openweathermap.org/data/2.5/forecast?&lat=43.15&lon=-77.62&APPID="+key+"&units=imperial"+"&cnt=4"
        response = urllib.urlopen(url)
        return json.loads(response.read())
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
x = d.filterData(data)
W = Weather(0,0,0)
W.cloud=W.findHighestCloudPercentage(x)
W.rain=W.findTotalRain(x)
print(W.rain)
print(W.cloud)





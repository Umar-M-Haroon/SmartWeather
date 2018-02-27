import urllib,json

#main.temp_min
#main.temp_max
#clouds.all
#rain.3h Rain volume for the last 3 hours
class Weather:
    def getData(self):
        key = "cf22c6d3079412ef13ed81f039297bc8"
        url = "http://api.openweathermap.org/data/2.5/forecast?q=Bangkok&APPID="+key+"&units=imperial"+"&cnt=4"
        response = urllib.urlopen(url)
        return json.loads(response.read())
    def filterData(self,d):
        hour1 = d["list"][0]
        hour2 = d["list"][1]
        hour3 = d["list"][2]
        hour4 = d["list"][3]
        return [hour1,hour2,hour3,hour4]

w = Weather()
data = w.getData()
print(w.filterData(data)[1])
import urllib,json
key = "cf22c6d3079412ef13ed81f039297bc8"
url = "http://api.openweathermap.org/data/2.5/forecast?q=Bangkok&APPID="+key+"&units=imperial"+"&cnt=4"
response = urllib.urlopen(url)
data = json.loads(response.read())
print url+'\n'+'\n'
print data["list"][0]
print data["list"][0]


#main.temp_min
#main.temp_max
#clouds.all
#rain.3h Rain volume for the last 3 hours

#Script that pulls weather from weather.gov

import sys, urllib, urllib2
import lxml.etree
from BeautifulSoup import BeautifulSoup

if len(sys.argv) < 2:
        print >>sys.stderr, 'usage:\t\tpythonweather.py CITY, STATE\nexample:\tpython weather.py Seattle, WA'
        exit(2)

data = urllib.urlencode({'inputstring': ' '.join(sys.argv[1:])})
info=urllib2.urlopen('http://forecast.weather.gov/zipcity.php', data)
content = info.read()

#print '*******Solution #1 (fail - parsing with xpath too painful)*******'
parser = lxml.etree.HTMLParser(encoding='utf-8')
tree = lxml.etree.fromstring(content, parser)
arr = tree.xpath(".//span[contains(concat(' ', normalize-space(@class), ' '), ' label ')]")

#for i in range(len(arr)):
        #print lxml.etree.tostring(arr[i])
        #prints all the 'label' class lines which is useful - its all the weather info

#humid = tree.xpath('.//span["b=Humidity"]').extract()
#print 'Humidity: ', humid


print '\n*******Weather in ',sys.argv[1], sys.argv.pop(),'*******'
soup = BeautifulSoup(content)
result = soup.findAll('span', {'class' : 'label'})

#print 'Wind speed: ', result[1].nextSibling #hardcoding the array index

import datetime
today=datetime.date.today()
print today.strftime('Today is %A %d, %b, %Y')

hum = [s.nextSibling for s in result if "Humidity" in s]
print 'Humidity: ', hum[0].string       #Find by searching for the keyword.
                                        #Have to read the html in the 'result' array
dew = [s.nextSibling for s in result if "Dewpoint" in s]
print 'Dew Point: ', dew[0].string.replace('&deg;', ' ')

wind = [s.nextSibling for s in result if "Wind Speed" in s]
print 'Wind Speed: ', wind[0].string

vis = [s.nextSibling for s in result if "Visibility" in s]
print 'Visibility: ', vis[0].string

print '\nWeather this week:\n'

for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        day_weather = [s.nextSibling for s in result if day in s]
        if len(day_weather) > 0:
                print day, ':', day_weather[0].string
        else:
                print day, ':', 'No weather data available'

print '\n'

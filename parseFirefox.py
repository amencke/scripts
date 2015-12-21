#This is from a Python book I was reading 
#It prints out details about your downloads, google searches, and history from firefox
#Depending on the version of FF you use it probably won't work

import re
import optparse
import os
import sqlite3

def printDownloads(downloadDB):
        conn = sqlite3.connect(downloadDB)
        c = conn.cursor()
        c.execute('SELECT content, datetime(dateAdded/1000000, \
                \'unixepoch\') FROM moz_annos;')
        print ' --- Files Downloaded ---'
        for row in c:
               print '[*] File: ' + str(row[0]) +\
                        ' on: ' + str(row[1])

def printCookies(cookiesDB):
        try:
               conn = sqlite3.connect(cookiesDB)
               c = conn.cursor()
               c.execute('SELECT host, name, value FROM moz_cookies')
               print '\n[*] -- Found Cookies --'
               for row in c:
                host = str(row[0])
                name = str(row[1])
                value = str(row[2])
                print '[+] Host: ' + host + ', Cookie: ' + name \
                                + ', Value: ' + value
        except Exception, e:
               if 'encrypted' in str(e):
                print '\n[*] Error reading your cookies DB.'
                print '[*] Upgrade you python-sqlite3 library.'

def printHistory(placesDB):
        try:
               conn = sqlite3.connect(placesDB)
               c = conn.cursor()
               c.execute('SELECT url, datetime(visit_date/1000000, \
                        \'unixepoch\') FROM moz_places, moz_historyvisits \
                        where visit_count > 0 and moz_places.id==\
                        moz_historyvisits.id;')
               print '\n[*] -- Found History --'
               for row in c:
                url = str(row[0])
                date = str(row[1])
                print '[+] ' + date + ' - Visited: ' + url
        except Exception, e:
               if 'encrypted' in str(e):
                print '\n[*] Error reading your places DB.'
                print '[*] Upgrade you python-sqlite3 library.'
                exit(0)

def printGoogle(placesDB):
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute('SELECT url, datetime(visit_date/1000000, \
                \'unixepoch\') from moz_places, moz_historyvisits \
                WHERE visit_count > 0 and moz_places.id==\
                moz_historyvisits.place_id;')
        print '\n[*] -- Found Google Searches --'
        for row in c:
               url = str(row[0])
               date = str(row[1])
               if 'google' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                        search = r[0].split('&')[0]
                        search = search.replace('q=', '').replace('+', ' ')
                        if (len(search) > 1):
                                print '[+] '+ date +' - Searched for: ' + search

def main():
        parser = optparse.OptionParser('usage%prog ' +\
                '-p <firefox profile path>')
        parser.add_option('-p', dest='pathName', type='string',\
                help='specify firefox profile path')
        (options, args) = parser.parse_args()
        pathName = options.pathName
        if pathName == None:
               print parser.usage
               exit(1)
        elif os.path.isdir(pathName) == False:
               print '[!] Path does not exist: ' + pathname
               exit(1)
        else:
               downloadDB = os.path.join(pathName, 'places.sqlite')
               if os.path.isfile(downloadDB):
                printDownloads(downloadDB)
               else:
                print 'Downloads DB does not exist: ' + downloadDB

               cookiesDB = os.path.join(pathName, 'cookies.sqlite')
               if os.path.isfile(cookiesDB):
                printCookies(cookiesDB)
               else:
                print '[!] Cookies DB does not exist: ' + cookiesDB

               placesDB = os.path.join(pathName, 'places.sqlite')
               if os.path.isfile(placesDB):
                printHistory(placesDB)
                printGoogle(placesDB)
               else:
                print '[!] PlacesDB does not exist: ' + placesDB
if __name__ == '__main__':
        main()

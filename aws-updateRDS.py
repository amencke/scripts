#Script to see effect of write loop of different cloudwatch metrics

from pprint import pprint
from boto import rds
import pymysql
import pymysql.cursors
import random
import sys

rds_conn = rds.connect_to_region("eu-west-1")
dbinstances = rds_conn.get_all_dbinstances("mysqldb")

print "\n******Database details******"
for dbi in dbinstances:
    print "status:\t\t" + dbi.status
    print "hostname:\t" + dbi.endpoint[0]
    print "port:\t\t" + str(dbi.endpoint[1])
print "****************************\n"

dbconn = pymysql.connect(
        host = dbi.endpoint[0],
        user = 'dbuser',
        password = 'password',
        db = 'mysqlDB',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )

cur = dbconn.cursor()

tableSchema = "CREATE TABLE AWSTestTable (\
id int NOT NULL AUTO_INCREMENT PRIMARY KEY,\
 data1 VARCHAR(255),\
 data2 VARCHAR(255),\
 data3 VARCHAR(255)\
)"

popTable = "INSERT INTO AWSTestTable (data1, data2, data3) VALUES\
 (" + str(random.randint(1,1000000000)) + ",\
 " + str(random.randint(1,1000000000)) + ",\
 " + str(random.randint(1,1000000000)) + "\
)"

if len(sys.argv) > 1:
    if sys.argv[1] == "create":
        try:
            cur.execute(tableSchema)
        except Exception, e:
            print str(e)

    elif sys.argv[1] == "populate":
        count = 0
        while 1:
            try:
                count += 1
                cur.execute(popTable)
                print "Updated DB successfully " + str(count) + " times"
            except Exception, e:
                print str(e)
                continue
    else:
        print 'usage: [ create | populate ] '
else:
    print 'usage: [ create | populate ] '
    

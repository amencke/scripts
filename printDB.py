#Print out the contents of a database and/or its tables
#usage%prog -d <database> [-t <table>]


import optparse
import sqlite3
import os

def printTables(database):
        try:
                conn = sqlite3.connect(database)
                q = conn.cursor()
                q.execute('SELECT tbl_name FROM sqlite_master \
                                WHERE type==\"table\";')
                print '\n[*] Database: ' + database
                for row in q:
                        print '[-] Table: '+str(row)
        except:
                pass

def printTableContents(database, tableName):
        try:
                conn = sqlite3.connect(database)
                q = conn.cursor()
                q.execute('SELECT * FROM '+ tableName +';')
                print '\n[*] Contents of ' + database
                for row in q:
                        print row

        except:
                print '[!] Could not open database'
        conn.close()

def main():
        parser = optparse.OptionParser('usage%prog '+\
                        '-d <database> [-t <table>]')
        parser.add_option('-d', dest='dbname', type='string',\
                        help='specify a database')
        parser.add_option('-t', dest='tableName', type='string',\
                        help='specify a table name')
        (options, args) = parser.parse_args()
        dbname = options.dbname
        tableName = options.tableName
        if dbname == None:
                print parser.usage
                exit(1)
        if not '/' in dbname:
                check = os.path.isfile(dbname)
                if not check:
                        print '[!] Cannot find database in ' + os.getcwd() + ', try absolute directory/filename'
                        exit(1)
        if (dbname != None) and (tableName != None):
                printTableContents(dbname, tableName)
        else:
                printTables(dbname)

if __name__ == '__main__':
        main()

import sys
import os
import ConfigParser
import MySQLdb
import MySQLdb.cursors

class dbHelper:
    def __init__(self,section):
        self.cf = ConfigParser.ConfigParser()
        self.cwd = os.getcwd()
        self.cf.read(self.cwd+"/config.conf")
        conf = self.getConf(section) 
        self.db = MySQLdb.connect(host=conf[0],port=int(conf[1]),user=conf[2],passwd=conf[3],db=conf[4],charset="utf8",cursorclass = MySQLdb.cursors.DictCursor) 
        self.cursor = self.db.cursor()

    def getConf(self,section):
        return (self.cf.get(section,'host'), \
                self.cf.get(section,'port'), \
                self.cf.get(section,'user'), \
                self.cf.get(section,'passwd'), \
                self.cf.get(section,'db'))


    def connDb(self,db_name):
        self.db.select_db(db_name)

    def close(self):
        self.db.close()

    def insert(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    def select(self,sql):
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        self.db.commit()
        return ret


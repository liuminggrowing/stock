import os
import sys
from dbHelper import mydb
reload(sys)
sys.setdefaultencoding('utf8')

def main():
    mdb = mydb("stock")
    for line in open("stock_code.txt"):
        stock = line.strip("\n").split(" ")
        sql="insert ignore into stock(`type`,`stock_id`,`stock_name`) values(\"%s\",\"%s\",\"%s\")" % (stock[0],stock[1],stock[2])
        if stock[0] == "cyb":
            print stock
            print sql
        mdb.insert(sql)


if __name__ == "__main__":
    main()

# -*- coding:utf-8 -*-  
import os
import sys
import redis
from dbHelper import mydb
import urllib2
reload(sys)
sys.setdefaultencoding('utf8')

redish = redis.Redis(host="localhost",port="6379",db=0)
mdb = mydb("stock")

def main():
    targets = {"ha":"sh","hb":"sh","sa":"sz","sb":"sz","zs":"sz","jj":"sh","etf":"sh"}
    stk = mdb.select("select * from stock")
    url = "http://qt.gtimg.cn/"
    for stock in stk:
        if stock["type"] in targets.keys():
            stock_id = str(stock["stock_id"])
            if len(stock_id) < 6 :
                stock_id = "0" * (6 - len(stock_id)) + stock_id
                
            
            rsp = urllib2.urlopen(url+"q="+targets[stock["type"]]+stock_id)
            rsp =  rsp.read().split("=")[1][1:-2].split("~")
            val = stock_id+"_"+stock["stock_name"]
            #print stock["stock_name"],type(stock["stock_name"])
            if len(rsp) != 50:
                continue
            else: 
                redish.zadd("stock::jiage",val,float(rsp[3]))
                redish.zadd("stock::zhangdie",val,float(rsp[31]))
                redish.zadd("stock::shiyinlv",val,float(rsp[46]))
            
def display(desc,lists):
    print desc
    for l in lists:
        print l[0],l[1]

if __name__ == "__main__":
    main()
    res = redish.zrange("stock::jiage",0,10,True,True)
    display("当前价格",res)
    res =  redish.zrevrange("stock::shiyinlv",0,10,True,True)
    display("市盈率",res)
    res =  redish.zrange("stock::zhangdie",0,10,True,True)
    display("涨跌",res)

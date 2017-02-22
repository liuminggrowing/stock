# -*- coding:utf-8 -*-  
import sys
import os
from dbHelper import dbHelper
import ConfigParser
import urllib2
from bs4 import BeautifulSoup
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf8')

mdb = dbHelper("stock")

def getRowTds(tds):
    res = []
    for td in tds:
        res.append(td.get_text().strip())
    return res

def getStockHistory(stock_id,year):
    url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/"+str(stock_id)+".phtml"

    for jd in range (1,5):
        print url+"?year="+str(year)+"&jidu="+str(jd)
        rsp = urllib2.urlopen(url+"?year="+str(year)+"&jidu="+str(jd))
        rsp = rsp.read()
        soup = BeautifulSoup(rsp,"html.parser")
        res = soup.select("#FundHoldSharesTable")
        if res == []:
            return False
        res = res[0].find_all("tr")
        if len(res) <= 2:
            return False
        for tr in res[2:]:
            tds = tr.find_all("td")
            if tds !=[]:
                res =  getRowTds(tds)
                sql = "insert into history(`stock_id`,`date`,`kpj`,`zgj`,`spj`,`zdj`,`jyl`,`jyje`) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" \
                        % (stock_id,res[0],res[1],res[2],res[3],res[4],res[5],res[6])
                mdb.insert(sql)

def is_num(target):
    try:
        int(target)
        return True
    except:
        return False


    
def fillStockId(stock_id):
    if len(stock_id) < 6 :
        stock_id = "0" * (6 - len(stock_id)) + stock_id
    return stock_id

def main():
    stocks = mdb.select("select stock_id from stock")
    conf = ConfigParser.ConfigParser()
    conf.read(os.getcwd()+"/config.conf")
    start = conf.get("history","start")
    end = conf.get("history","end")

    for stock in stocks:
        stock_id = fillStockId(str(stock["stock_id"]))
        for cur in range(int(start),int(end)+1):
            history = getStockHistory(stock_id,cur)


if __name__ == "__main__":
    main()
    

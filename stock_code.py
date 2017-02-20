# -*- coding:utf-8 -*-
import os
import sys
from bs4 import BeautifulSoup
import ConfigParser
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

logHelper = open(os.getcwd()+"/stock_code.txt","a")

def is_num(target):
    try:
        int(target)
        return True
    except:
        return False

def get_stock_code(url,t="ha",p=1):
    try:
        url = url+"&t="+t+"&p="+str(p)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html,"html.parser")
        trs =  soup.find_all('tr')
        for tr in trs:
            tds = tr.find_all("td")
            if tds != [] and len(tds) > 2:
                print tds
                #print t+" "+tds[0].get_text()+" "+tds[1].get_text()
                #tmp = str(tds[1].get_text())
                #print tmp.decode("utf8").encode("utf8")
    #            logHelper.write(t+" "+str(tds[0].get_text())+" "+str(tds[1].get_text())+"\n")
    except Exception as e:
        print e

def main():
    url = "http://app.finance.ifeng.com/list/stock.php?f=chg_pct&o=desc"
    ts = ["ha","hb","sa","sb","zxb","cyb","zs","jj","etf","zq"]
    for t in ts:
        for p in range(1,50):
            get_stock_code(url,t,p)

    

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import sf_getContent as content
import sf_getPreviousPage as previous
from datetime import datetime
import sf_database
import sf_getUrlList as getUrl
import arg_db 

cookies = {'over18':'1'}
runTime = 1 #指定爬取的頁面
pttdb = sf_database.connectTodb(arg_db.databasePath)  # 連結到pttdb

for tableName in arg_db.forumDict.keys():             # 建立表單  
    sf_database.createDbTables(pttdb, tableName)
    for url in arg_db.forumDict.values():
        for i in range(runTime):    
            htmlFile = requests.get(url, cookies= cookies)  # 連結到指定網頁    
            soup = BeautifulSoup(htmlFile.text, 'lxml')     # 解析指定網貝
            articleList = content.getContent(soup)          # 取得該頁的所有資料, 為List中包著字典的資料
            url = previous.getPreviousPage(soup)    # 取得上一頁的網址, 透過迴圈可以不斷往上一頁前進
            sf_database.saveData(pttdb, tableName, articleList)
